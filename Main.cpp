#include <iostream>
#include <vector>
#include <cmath>
#include <functional>
#include <glad/glad.h>
#include <GLFW/glfw3.h>

// Se M_PI não estiver definido:
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

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

// assinatura de função para campo vetorial
using VectorFieldFunction = std::function<std::pair<float, float>(float, float)>;

void calcula_pontas(float x1, float y1,
    float x2, float y2,
    float pontaX[2], float pontaY[2],
    float tamanhoPonta = 0.02f)
{
    float dx = x2 - x1;
    float dy = y2 - y1;
    float magnitude = std::sqrt(dx * dx + dy * dy);
    if (magnitude == 0.0f) return;

    float angulo = std::atan2(dy, dx);

    // cast explícito de double para float
    pontaX[0] = x2 - tamanhoPonta * (float)std::cos(angulo - M_PI / 6.0);
    pontaY[0] = y2 - tamanhoPonta * (float)std::sin(angulo - M_PI / 6.0);

    pontaX[1] = x2 - tamanhoPonta * (float)std::cos(angulo + M_PI / 6.0);
    pontaY[1] = y2 - tamanhoPonta * (float)std::sin(angulo + M_PI / 6.0);
}

void cria_seta(float x1, float y1,
    float dirX, float dirY,
    float tamanho, float tamanhoPonta,
    std::vector<float>& vertices)
{
    float mag = std::sqrt(dirX * dirX + dirY * dirY);
    if (mag == 0.0f) mag = 1.0f;
    dirX /= mag;
    dirY /= mag;

    float x2 = x1 + dirX * tamanho;
    float y2 = y1 + dirY * tamanho;

    float pontaX[2], pontaY[2];
    calcula_pontas(x1, y1, x2, y2, pontaX, pontaY, tamanhoPonta);

    // linha principal
    vertices.push_back(x1); vertices.push_back(y1);
    vertices.push_back(x2); vertices.push_back(y2);

    // ponta 1
    vertices.push_back(x2); vertices.push_back(y2);
    vertices.push_back(pontaX[0]); vertices.push_back(pontaY[0]);

    // ponta 2
    vertices.push_back(x2); vertices.push_back(y2);
    vertices.push_back(pontaX[1]); vertices.push_back(pontaY[1]);
}

void gera_campo_vetorial(VectorFieldFunction func,
    std::vector<float>& vertices,
    int cols, int rows,
    float tamanhoSeta, float tamanhoPonta)
{
    const float spacingX = 2.0f / cols;
    const float spacingY = 2.0f / rows;

    for (int i = 0; i < cols; ++i) {
        for (int j = 0; j < rows; ++j) {
            float x = -1.0f + i * spacingX + spacingX / 2.0f;
            float y = -1.0f + j * spacingY + spacingY / 2.0f;

            // sem structured bindings:
            std::pair<float, float> dir = func(x, y);
            float dirX = dir.first;
            float dirY = dir.second;

            cria_seta(x, y, dirX, dirY, tamanhoSeta, tamanhoPonta, vertices);
        }
    }
}

int main() {
    // inicialização do GLFW
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(800, 800, "Campo Vetorial", NULL, NULL);
    if (!window) {
        std::cerr << "Falha ao criar janela GLFW\n";
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    gladLoadGL();

    // compila os shaders
    GLuint vs = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vs, 1, &vertexShaderSource, NULL);
    glCompileShader(vs);

    GLuint fs = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fs, 1, &fragmentShaderSource, NULL);
    glCompileShader(fs);

    GLuint shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vs);
    glAttachShader(shaderProgram, fs);
    glLinkProgram(shaderProgram);
    glDeleteShader(vs);
    glDeleteShader(fs);

    // define aqui a função do campo vetorial
    VectorFieldFunction campo = [](float x, float y) {
        return std::make_pair(-y + x, x + y);
        };

    const int cols = 20, rows = 20;
    const float tamanhoSeta = 0.04f;
    const float tamanhoPonta = 0.012f;

    std::vector<float> vertices;
    gera_campo_vetorial(campo, vertices, cols, rows, tamanhoSeta, tamanhoPonta);

    // setup VAO/VBO
    GLuint VAO, VBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);

    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);

    // cast explícito para GLsizeiptr
    glBufferData(GL_ARRAY_BUFFER,
        (GLsizeiptr)(vertices.size() * sizeof(float)),
        vertices.data(),
        GL_STATIC_DRAW);

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    glLineWidth(1.5f);

    // loop principal
    while (!glfwWindowShouldClose(window)) {
        glClearColor(0, 0, 0, 1);
        glClear(GL_COLOR_BUFFER_BIT);

        glUseProgram(shaderProgram);
        glBindVertexArray(VAO);
        glDrawArrays(GL_LINES, 0, (GLsizei)(vertices.size() / 2));

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // cleanup
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteProgram(shaderProgram);
    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}
