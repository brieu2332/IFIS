//motor físico.h
//vai ser o cérebro da simulação
//armazena todas as estrelas
//calcula as forças gravitacionais entre elas
//atualiza suas posições e velocidades

#pragma once
#include <vector>
#include <iostream>
#include "estrelaNeutron.h"

class MotorFisico {
private:
    std::vector<EstrelaDeNeutron> estrelas;
    const double G = 6.67430e-11;

public:
    void adicionarEstrela(const EstrelaDeNeutron& estrela) {
        estrelas.push_back(estrela);
    }

    void computarForca() {
        for (auto& estrela : estrelas) {
            estrela.aceleracao = Vec3(); // zera antes de somar forças
        }

        for (size_t i = 0; i < estrelas.size(); ++i) {
            for (size_t j = i + 1; j < estrelas.size(); ++j) {
                Vec3 delta = estrelas[j].posicao - estrelas[i].posicao;
                double distancia = delta.comprimento();

                if (distancia < 1e-10) continue;

                double forcaMagnitude = G * estrelas[i].massa * estrelas[j].massa / (distancia * distancia);
                Vec3 forca = delta.normalizado() * forcaMagnitude;

                estrelas[i].aceleracao += forca / estrelas[i].massa;
                estrelas[j].aceleracao -= forca / estrelas[j].massa;
            }
        }
    }

    void atualizar(double dt) {
        for (auto& estrela : estrelas) {
            estrela.atualizar(dt);
        }
    }

    // ✅ Detecta colisão entre pares de estrelas
    bool detectarColisao(double tolerancia = 1e-3) const {
        for (size_t i = 0; i < estrelas.size(); ++i) {
            for (size_t j = i + 1; j < estrelas.size(); ++j) {
                double distancia = (estrelas[i].posicao - estrelas[j].posicao).comprimento();
                double somaRaios = estrelas[i].radius + estrelas[j].radius;

                if (distancia <= somaRaios + tolerancia) {
                    return true; // estão colidindo
                }
            }
        }
        return false;
    }

    const std::vector<EstrelaDeNeutron>& getEstrelas() const {
        return estrelas;
    }

    void imprimirEstado() const {
        for (size_t i = 0; i < estrelas.size(); ++i) {
            const auto& e = estrelas[i];
            std::cout << "Estrela " << i + 1 << ":\n";
            std::cout << "  Posicao: (" << e.posicao.x << ", " << e.posicao.y << ", " << e.posicao.z << ")\n";
            std::cout << "  Velocidade: (" << e.velocidade.x << ", " << e.velocidade.y << ", " << e.velocidade.z << ")\n";
            std::cout << "  Aceleracao: (" << e.aceleracao.x << ", " << e.aceleracao.y << ", " << e.aceleracao.z << ")\n\n";
        }
    }
};
