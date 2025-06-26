#pragma once //só chama uma vez
#include <cmath> //pra sqrt(), precisa pra calcular distancias(tamanho dos vetores)

    struct Vec3 {
        //estrutura que vai armazenar 3 números, representa as coordenadas 3d(posição, velocidade, aceleração)
        double x, y, z; //double é pra ter mais precisão que float, na questão do arrendondamento
        //construtor que está criando um vec3 com valores iniciais, se não passar ele mesmo passa, 0, 0, 0
        Vec3(double x = 0, double y = 0, double z = 0) : x(x), y(y), z(z) {}
        
        //permite somar dois vec3 com o operador +. é pra deixar o código mais limpo
        //const aqui é para garantir que esse método não altera o vetor atual.
        //vec3 é o parametro, no caso um vetor 3D, & vai indicar que o parametro é uma referencia(um apelido para a variavel original)
        Vec3 operator+(const Vec3& outro) const {
            return Vec3(x + outro.x, y + outro.y, z + outro.z);
        } 
        //o mesmo só que para subtração
        Vec3 operator-(const Vec3& outro) const {
            return Vec3(x - outro.x, y - outro.y, z - outro.z);
        }
        //vai multiplicar cada componente do vetor por um número escalar, para o redimensionamento de vetores
        Vec3 operator*(double escalar) const {
            return Vec3(x * escalar, y * escalar, z * escalar);

        }
        Vec3 operator/(double escalar) const{
            return Vec3(x / escalar, y / escalar, z / escalar);
        }

          Vec3& operator-=(const Vec3& other) {
        x -= other.x;
        y -= other.y;
        z -= other.z;
        return *this;
        }

           Vec3& operator+=(const Vec3& other) {
        x += other.x;
        y += other.y;
        z += other.z;
        return *this;
        }
        
        //aqui é para calcular o tamanho do módulo do vetor usando o pitagoras 3d, é para saber a distancia da estrela até a origem ou a força gravitacional
        double comprimento() const {
            return std::sqrt(x*x + y*y + z*z);
        }
        //retorna uma versão normalizada do vetor(com o mesmo ângulo, mas tamanho = 1), é melhor para representar direções sem se preocupar com o tamanho
        Vec3 normalizado() const {
            double comp = comprimento();
            return Vec3(x/comp, y/comp, z/comp);
        }


    };
    