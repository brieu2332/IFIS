//aqui é onde calcula se as cargas se empurram ou se atraem
//se colocar a carga aqui, o campo eletrico, vai empurrar

#pragma once //me utilizar só uma vez
#include "carga.h" //puxa as informações da carga
#include <cmath>

const float k_e = 8.9875e9; //Constante de Coulomb (N·m²/C²)

//função q retorna o campo elétrico (Ex, Ey) em um ponto (x, y)
std::pair<float, float> calculateFieldAt(float x, float y, const std::vector<Charge>& charges) {
    float Ex = 0.0f, Ey = 0.0f; //começa sem um "vento"
    
    for (const auto& charge : charges) { //para cada carga no projeto..
        float dx = x - charge.x; //distancia em x
        float dy = y - charge.y; //distancia em y
        float r = sqrt(dx*dx + dy*dy); //distancia total(pitágoras)
        if (r < 1e-3) continue; //evita divisão por zero

        float E_magnitude = k_e * charge.q / (r * r); //força desse "vento"
        Ex += E_magnitude * (dx / r); // vento na direção x
        Ey += E_magnitude * (dy / r); // vento na direção y
    }
    return {Ex, Ey}; //retorna total
}