//a ficha de identidade de uma carga elétrica
//x, y = onde ela está no mapa 
//q = Se ela é (+)(atrai) ou (-)(empurra).
//m = peso (quanto mais pesada, mais difícil de mover).
//vx, vy = velocidade

#pragma once //aviso de só utilizar uma vez
#include <vector>

struct Charge { 
    float x, y;     //posição no mapa
    float q;        //carga positiva ou negativa
    float m;        //massa
    float vx, vy;   //velocidade (pra onde vai)
};