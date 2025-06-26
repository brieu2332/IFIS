#include <iostream>
#include <chrono>
#include <thread>
#include "vec3.h"
#include "motorfisico.h"

int main() {
    MotorFisico sim;

    //adiciono duas estrelas com dados reais
    sim.adicionarEstrela(EstrelaDeNeutron(Vec3(-1e7, 0, 0), Vec3(0, 1000, 0), 1.0e30, 1e6));
    sim.adicionarEstrela(EstrelaDeNeutron(Vec3(1e7, 0, 0), Vec3(0, -1000, 0), 1.0e30, 1e6));

    const double dt = 0.001; // passos de 1ms 
    const int maxPassos = 10000;

    for (int passo = 0; passo < maxPassos; ++passo) {
        sim.computarForca();
        sim.atualizar(dt);

          if (passo % 1000 == 0) { // imprimir a cada 1000 passos 
        std::cout << "Passo " << passo << "\n";
        sim.imprimirEstado();
    }

    //    std::cout << "Passo " << passo << "\n";
    //    sim.imprimirEstado();

        if (sim.detectarColisao()) {
            std::cout << "💥 COLISÃO DETECTADA! Estrelas se fundiram!\n";
            break;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }

    return 0;
}
