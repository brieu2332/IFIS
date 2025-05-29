#include <iostream>
using namespace std;

int main() {
    char matriz[5][5];     // Cria uma matriz 5x5 de caracteres
    int x = 2, y = 2;      // Posição da seta: linha 2, coluna 2

    // Preenche a matriz com pontos '.'
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            matriz[i][j] = '.'; // Cada posição recebe um ponto
        }
    }

    matriz[x][y] = '>'; // Coloca a seta apontando para a direita na posição (2, 2)

    // Imprime a matriz na tela
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            cout << matriz[i][j] << " "; // Mostra o valor e um espaço
        }
        cout << endl; // Quebra a linha após cada linha da matriz
    }

    return 0;
}
