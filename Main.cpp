#include <iostream>
#include <vector>
#include <cmath>
#include <glad/glad.h>
#include <GLFW/glfw3.h>

const char* vertexShaderSource = R"(
#version 330 core
layout (location = 0) in vec2 aPos;
void main() {
    gl_Position = vec4(aPos, 0.0, 1.0);
}
)";

const char* fragmentShaderSource = R"(
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
)";

void calcula_pontas(float x1, float y1, float x2, float y2, float pontaX[2], float pontaY[2], float tamanhoPonta = 0.02f) {
    float dx = x2 - x1;
    float dy = y2 - y1;
    float magnitude = sqrt(dx * dx + dy * dy);
    if (magnitude == 0) return;

    float angulo = atan2(dy, dx);

    pontaX[0] = x2 - tamanhoPonta * cos(angulo - 3.14 / 6);
    pontaY[0] = y2 - tamanhoPonta * sin(angulo - 3.14 / 6);

    pontaX[1] = x2 - tamanhoPonta * cos(angulo + 3.14 / 6);
    pontaY[1] = y2 - tamanhoPonta * sin(angulo + 3.14 / 6);
}

void cria_seta(float x1, float y1, float dirX, float dirY, float tamanho, float tamanhoPonta, std::vector<float>& vertices) {
    float mag = sqrt(dirX * dirX + dirY * dirY);
    if (mag == 0) mag = 1.0f;
    dirX /= mag;
    dirY /= mag;

    float x2 = x1 + dirX * tamanho;
    float y2 = y1 + dirY * tamanho;

    float pontaX[2], pontaY[2];
    calcula_pontas(x1, y1, x2, y2, pontaX, pontaY, tamanhoPonta);

    // Linha principal
    vertices.push_back(x1); vertices.push_back(y1);
    vertices.push_back(x2); vertices.push_back(y2);

    // Ponta 1
    vertices.push_back(x2); vertices.push_back(y2);
    vertices.push_back(pontaX[0]); vertices.push_back(pontaY[0]);

    // Ponta 2
    vertices.push_back(x2); vertices.push_back(y2);
    vertices.push_back(pontaX[1]); vertices.push_back(pontaY[1]);
}

int main() {
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(800, 800, "Campo Vetorial", NULL, NULL);
    if (!window) {
        std::cout << "Falha ao criar janela GLFW" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    gladLoadGL();

    GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);

    GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
    glCompileShader(fragmentShader);

    GLuint shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    // Parâmetros do campo vetorial
    const int cols = 20;  // colunas
    const int rows = 20;  // linhas
    const float spacing = 2.0f / cols; // espaço entre setas
    const float tamanhoSeta = spacing * 0.4f; // tamanho da seta
    const float tamanhoPonta = tamanhoSeta * 0.3f;

    const float centro_x = 0.0f;
    const float centro_y = 0.0f;

    std::vector<float> vertices;

    for (int i = 0; i < cols; ++i) {
        for (int j = 0; j < rows; ++j) {
            float x = -1.0f + i * spacing + spacing / 2;
            float y = -1.0f + j * spacing + spacing / 2;

            float dirX = centro_x - x;
            float dirY = centro_y - y;

            cria_seta(x, y, dirX, dirY, tamanhoSeta, tamanhoPonta, vertices);
        }
    }

    GLuint VAO, VBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);

    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(float), vertices.data(), GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    glLineWidth(1.5f);

    while (!glfwWindowShouldClose(window)) {
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        glUseProgram(shaderProgram);
        glBindVertexArray(VAO);
        glDrawArrays(GL_LINES, 0, vertices.size() / 2);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteProgram(shaderProgram);
    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}
