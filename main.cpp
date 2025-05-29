//cria as cargas 
//calcula as forças(o "vento" que as move)
//atualiza as posições 

#include "carga.h" //puxa a carga
#include "campoEletrico.h" //puxa o calculo
#include <vector> //usa uma lista de cargas
#include <cstdio>

int main() {
    //se é criado as cargas (tipo imãs num mapa)
    std::vector<Charge> charges;
    charges.push_back({0.0f, 0.0f, 1e-6, 1.0f, 0.0f, 0.0f}); //carga positiva no centro
    charges.push_back({2.0f, 0.0f, -1e-6, 1.0f, 0.0f, 0.0f}); //carga negativa em x=2


    //carga de teste (que se move)
    Charge testCharge = {1.0f, 1.0f, 1e-6, 0.001f, 0.0f, 0.0f}; // q = 1e-6, m = 0.001kg (aumentei a carga e diminui a massa

    // Simulação (passo a passo)
    float deltaTime = 0.016f; // ~60 FPS
    for (int step = 0; step < 1000; ++step) {
        //calcula o campo elétrico na posição da carga de teste
        auto [Ex, Ey] = calculateFieldAt(testCharge.x, testCharge.y, charges);

        //calcula a força (F = q * E) e a aceleração (a = F / m)
        float Fx = testCharge.q * Ex;
        float Fy = testCharge.q * Ey;
        float ax = Fx / testCharge.m;
        float ay = Fy / testCharge.m;

        //atualiza velocidade e posição (Método de Euler)
        testCharge.vx += ax * deltaTime;
        testCharge.vy += ay * deltaTime;
        testCharge.x += testCharge.vx * deltaTime;
        testCharge.y += testCharge.vy * deltaTime;

        //mostra onde a carga está(tipo num gps)
        printf("Step %d: Pos = (%.2f, %.2f)\n", step, testCharge.x, testCharge.y);
    }

    return 0;
}