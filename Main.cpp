#include <iostream>
#include <vector>
#include <cmath>
#include <functional>

#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// ---- GLSL Sources ----
const char* vertexShaderSource = R"(
#version 330 core
layout (location = 0) in vec3 aPos;
uniform mat4 uView;
uniform mat4 uProj;
void main() {
    gl_Position = uProj * uView * vec4(aPos, 1.0);
}
)";
const char* fragmentShaderSource = R"(
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0);
}
)";

// ---- GLFW + GLAD init ----
GLFWwindow* initWindow(int w, int h, const char* title) {
    if (!glfwInit()) {
        std::cerr << "Failed to initialize GLFW\n";
        return nullptr;
    }
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    GLFWwindow* win = glfwCreateWindow(w, h, title, nullptr, nullptr);
    if (!win) {
        std::cerr << "Failed to create GLFW window\n";
        glfwTerminate();
        return nullptr;
    }
    glfwMakeContextCurrent(win);
    glfwSetFramebufferSizeCallback(win, [](GLFWwindow*, int width, int height) {
        glViewport(0, 0, width, height);
        });
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cerr << "Failed to initialize GLAD\n";
        return nullptr;
    }
    glEnable(GL_DEPTH_TEST);
    glViewport(0, 0, w, h);
    return win;
}

// ---- Shader compile/link ----
GLuint compileShader(GLenum type, const char* src) {
    GLuint id = glCreateShader(type);
    glShaderSource(id, 1, &src, nullptr);
    glCompileShader(id);
    return id;
}
GLuint createProgram() {
    GLuint vs = compileShader(GL_VERTEX_SHADER, vertexShaderSource);
    GLuint fs = compileShader(GL_FRAGMENT_SHADER, fragmentShaderSource);
    GLuint prog = glCreateProgram();
    glAttachShader(prog, vs);
    glAttachShader(prog, fs);
    glLinkProgram(prog);
    glDeleteShader(vs);
    glDeleteShader(fs);
    return prog;
}

// ---- 3D Arrow with arrowhead ----
void cria_seta_3d(float x, float y, float z,
    float dx, float dy, float dz,
    float shaftLen, float headLen, float headWidth,
    std::vector<float>& verts)
{
    glm::vec3 start{ x,y,z };
    glm::vec3 dir{ dx,dy,dz };
    if (glm::length(dir) < 1e-6f) return;
    dir = glm::normalize(dir);

    // shaft end
    glm::vec3 tipBase = start + dir * shaftLen;
    // actual tip
    glm::vec3 tip = tipBase + dir * headLen;

    // choose up vector not colinear with dir
    glm::vec3 up{ 0,1,0 };
    if (fabs(glm::dot(up, dir)) > 0.9f) up = glm::vec3{ 1,0,0 };

    // two orthogonal vectors perpendicular to dir
    glm::vec3 s1 = glm::normalize(glm::cross(dir, up));
    glm::vec3 s2 = glm::normalize(glm::cross(dir, s1));

    // 1) draw shaft
    verts.insert(verts.end(), {
        start.x, start.y, start.z,
        tipBase.x, tipBase.y, tipBase.z
        });

    // 2) build arrowhead: four edges from tipBase -> corners -> tip
    glm::vec3 offsets[4] = {
        s1 * headWidth + s2 * headWidth,
        s1 * headWidth - s2 * headWidth,
       -s1 * headWidth + s2 * headWidth,
       -s1 * headWidth - s2 * headWidth
    };
    for (int i = 0; i < 4; ++i) {
        glm::vec3 corner = tipBase + offsets[i];
        // edge from base to corner
        verts.insert(verts.end(), {
            tipBase.x, tipBase.y, tipBase.z,
            corner.x,  corner.y,  corner.z
            });
        // edge from corner to tip
        verts.insert(verts.end(), {
            corner.x,  corner.y,  corner.z,
            tip.x,     tip.y,     tip.z
            });
    }
}

// ---- Generate 3D vector field ----
using VectorField3D = std::function<glm::vec3(float, float, float)>;
void gera_campo_3d(VectorField3D f,
    std::vector<float>& verts,
    int cols, int rows,
    float shaftLen, float headLen, float headWidth,
    const std::vector<float>& layersZ)
{
    float dx = 2.0f / cols, dy = 2.0f / rows;
    for (float z : layersZ) {
        for (int i = 0; i < cols; ++i) {
            for (int j = 0; j < rows; ++j) {
                float x = -1.0f + (i + 0.5f) * dx;
                float y = -1.0f + (j + 0.5f) * dy;
                glm::vec3 d = f(x, y, z);
                cria_seta_3d(x, y, z, d.x, d.y, d.z,
                    shaftLen, headLen, headWidth,
                    verts);
            }
        }
    }
}

// ---- Camera ----
struct Camera {
    float r = 5, yaw = 0, pitch = 0;
    float spd = glm::radians(60.0f), lim = glm::radians(89.0f);
};
void processInput(GLFWwindow* w, Camera& c, float dt) {
    if (glfwGetKey(w, GLFW_KEY_LEFT) == GLFW_PRESS) c.yaw += c.spd * dt;
    if (glfwGetKey(w, GLFW_KEY_RIGHT) == GLFW_PRESS) c.yaw -= c.spd * dt;
    if (glfwGetKey(w, GLFW_KEY_UP) == GLFW_PRESS) c.pitch += c.spd * dt;
    if (glfwGetKey(w, GLFW_KEY_DOWN) == GLFW_PRESS) c.pitch -= c.spd * dt;
    if (glfwGetKey(w, GLFW_KEY_KP_ADD) == GLFW_PRESS) c.r -= 2.0f * dt;
    if (glfwGetKey(w, GLFW_KEY_KP_SUBTRACT) == GLFW_PRESS) c.r += 2.0f * dt;
    c.pitch = glm::clamp(c.pitch, -c.lim, c.lim);
    c.r = glm::clamp(c.r, 0.5f, 20.0f);
}
glm::mat4 computeView(const Camera& c) {
    float x = c.r * cos(c.pitch) * sin(c.yaw);
    float y = c.r * sin(c.pitch);
    float z = c.r * cos(c.pitch) * cos(c.yaw);
    return glm::lookAt(glm::vec3{ x,y,z }, glm::vec3{ 0 }, glm::vec3{ 0,1,0 });
}

int main() {
    GLFWwindow* win = initWindow(800, 600, "Campo Vetorial 3D");
    if (!win) return -1;

    GLuint prog = createProgram();
    glUseProgram(prog);
    GLint viewLoc = glGetUniformLocation(prog, "uView");
    GLint projLoc = glGetUniformLocation(prog, "uProj");

    glm::mat4 proj = glm::perspective(glm::radians(45.0f),
        800.0f / 600.0f,
        0.1f, 100.0f);
    glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm::value_ptr(proj));

    std::vector<float> verts;
    VectorField3D campo3d = [](float x, float y, float z) {
        float wz = std::sin(2.0f * M_PI * x * y);
        return glm::normalize(glm::vec3(y, -x, wz));//função1
        };
    std::vector<float> layersZ = { -1.0f,-0.5f, 0.0f, 0.5f, 1.0f };
    gera_campo_3d(campo3d, verts,
        30, 30,
        0.2f, // shaft length
        0.05f, // head length
        0.02f, // head width
        layersZ);

    // VAO/VBO
    GLuint VAO, VBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER,
        verts.size() * sizeof(float),
        verts.data(),
        GL_STATIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
        3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glBindVertexArray(0);

    Camera cam;
    float last = (float)glfwGetTime();
    while (!glfwWindowShouldClose(win)) {
        float now = (float)glfwGetTime(), dt = now - last;
        last = now;
        processInput(win, cam, dt);
        if (glfwGetKey(win, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(win, 1);

        glm::mat4 view = computeView(cam);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glUseProgram(prog);
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm::value_ptr(view));
        glBindVertexArray(VAO);
        glLineWidth(2.0f);
        glDrawArrays(GL_LINES, 0, (GLsizei)(verts.size() / 3));
        glfwSwapBuffers(win);
        glfwPollEvents();
    }

    glDeleteBuffers(1, &VBO);
    glDeleteVertexArrays(1, &VAO);
    glDeleteProgram(prog);
    glfwTerminate();    
    return 0;
}
