import pygame
import math
#import line from setas  # Importa a classe Seta do arquivo line.py

pygame.init()
largura, altura = 1100, 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulação IFIS: Sol e Terra")
clock = pygame.time.Clock()



class Seta:
    def __init__(self, cor, ox, oy, r, espessura, destino_x, destino_y):
        self.cor = cor
        self.ox = ox
        self.oy = oy
        self.r = r
        self.espessura = espessura
        self.a = 0
        self.destino_x = destino_x 
        self.destino_y = destino_y

    def desenhar(self, tela):
        # retorna o ângulo (em radianos) cujo seno e cosseno correspondem às coordenadas y e x. Ela é usada para calcular o ângulo de rotação entre dois pontos no plano cartesiano.
        self.a = math.atan2(self.destino_y - self.oy, self.destino_x - self.ox)
        
        x = self.r * math.cos(self.a)
        y = self.r * math.sin(self.a)

        b = self.a  + 3 * math.pi / 4
        c = self.a + 5 * math.pi / 4
        r2 = self.r / 3

        x2 = (r2 * math.cos(b)) + x
        x3 = (r2 * math.cos(c)) + x
        y3 = (r2 * math.sin(c)) + y
        y2 = (r2 * math.sin(b)) + y

        pygame.draw.line(tela, self.cor, (self.ox, self.oy), (self.ox + x, self.oy + y), self.espessura)
        pygame.draw.line(tela, self.cor, (self.ox + x, self.oy + y), (self.ox + x2, self.oy + y2), self.espessura)
        pygame.draw.line(tela, self.cor, (self.ox + x, self.oy + y), (self.ox + x3, self.oy + y3), self.espessura)

     

# Classe mãe para corpos celestes
class CorpoCeleste:
    def __init__(self, posicao, vel, massa, cor, raio_desenho, raio_influencia, raio_poco):
        self.posicao = pygame.Vector2(posicao)
        self.vel = pygame.Vector2(vel)
        self.massa = massa
        self.cor = cor
        self.raio_desenho = raio_desenho
        self.raio_influencia = raio_influencia
        self.raio_poco = raio_poco

    def update(self, forca, tempoDecorrido):
        acel = forca / self.massa  # a = F / m
        self.vel += acel * tempoDecorrido  
        self.posicao += self.vel * tempoDecorrido  

    def draw(self, surface):
        pygame.draw.circle(surface, self.cor, (int(self.posicao.x), int(self.posicao.y)), self.raio_desenho)
        pygame.draw.circle(surface, self.cor, (int(self.posicao.x), int(self.posicao.y)), self.raio_influencia, 1)
        pygame.draw.circle(surface, self.cor, (int(self.posicao.x), int(self.posicao.y)), self.raio_poco, 1)

# Classes filha sol
class Sol(CorpoCeleste):
    def __init__(self, posicao):
        super().__init__(posicao, vel=(0, 0), massa=10000, cor=(255, 255, 255),
                         raio_desenho=10, raio_influencia=150, raio_poco=30)

# Classes filha terra
class Terra(CorpoCeleste):
    def __init__(self, posicao):
        super().__init__(posicao, vel=(2, 2), massa=10, cor=(255, 255, 255),
                         raio_desenho=5, raio_influencia=100, raio_poco=20)

def calcular_forca(corpo1, corpo2):
    G = 1  #constante apenas para simulação
    direcao = corpo1.posicao - corpo2.posicao
    distancia = direcao.length()
    if distancia == 0:
        return pygame.Vector2(0, 0)
    forca_magnitude = G * corpo1.massa * corpo2.massa / (distancia ** 2) # formuula da gravitação universal
    return direcao.normalize() * forca_magnitude

# Instancia os corpos celestes
sol = Sol(posicao=(largura - 300, altura / 2))
terra = Terra(posicao=(150, altura / 1.5))

# Cria uma grade de setas (usando a classe Seta do line.py)
setas = [Seta((255, 255, 255), x, y, 15, 2, 0, 0) 
         for x in range(0, largura, 39) 
         for y in range(0, altura, 39)]

dt = 0.1  
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Calcula a força gravitacional entre o Sol e a Terra e atualiza a Terra
    forca = calcular_forca(sol, terra)
    terra.update(forca, dt)

    # Verifica colisão (quando a Terra entra no poço gravitacional do Sol)
    if (terra.posicao - sol.posicao).length() < sol.raio_poco:
        print("Colisão")
        rodando = False

    tela.fill((0, 0, 0))
    sol.draw(tela)
    terra.draw(tela)

    # Atualiza e desenha as setas: cada seta aponta para a direção resultante da influência dos corpos
    for seta in setas:
        pos_seta = pygame.Vector2(seta.ox, seta.oy)
        forca_total = pygame.Vector2(0, 0)
        for corpo in [sol, terra]:
            direcao = corpo.posicao - pos_seta
            distancia = direcao.length()
            if distancia != 0:
                # Influência simplificada: proporcional à massa e inversamente proporcional ao quadrado da distância
                f_mag = corpo.massa / (distancia ** 5)
                forca_total += direcao.normalize() * f_mag
        # Fator de escala para visualização
        fator = 100
        destino_x = seta.ox + forca_total.x * fator
        destino_y = seta.oy + forca_total.y * fator
        
        seta.destino_x = destino_x
        seta.destino_y = destino_y
        seta.desenhar(tela)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
