//estrela de neutron
#pragma once //novamente, para evitar duplicação do código quando o arquivo é incluido multiplas vezes
#include "vec3.h" //traz a definição de vec3 para usar posição velocidade etc

class EstrelaDeNeutron {
public:
    Vec3 posicao; //posição no espaço 3D. onde a estrela está no mapa, x=1.0, y=0.0, z=0.0. em metros
    Vec3 velocidade; //velocidade, como no gps. x=0.0, y=0.5, z=0.0 em m/s
    Vec3 aceleracao; //aceleração, calculada pelas forças. pisar no acelerador/freio m/s²
    double massa; //massa. tipo 2.0e30 kg, como uma estrela real. peso da estrela em kg
    double radius; //tamanho visual na tela

    //construtor
    EstrelaDeNeutron(Vec3 pos, Vec3 vel, double massa, double radius)
        : posicao(pos), velocidade(vel), massa(massa), radius(radius){} //lista de inicialização, é mais eficiente que atribuir valores dentro do corpo do construtor
    //inicializa a estrelas com os valores passados

    void atualizar(double dt){
    //atualiza velocidade e posição (método de euler)
    velocidade = velocidade + aceleracao * dt;
    posicao = posicao + velocidade * dt;
    aceleracao = Vec3(); //zera a aceleração para o próximo frame
    }
};
