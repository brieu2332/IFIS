import pygame
from math import cos, sin, pi, atan2

class Seta:
    def __init__(self, cor, ox, oy, r, espessura, destino_x, destino_y):
        self.cor = cor
        self.ox = ox 
        self.oy = oy
        self.r = r
        self.espessura = espessura
        self.destino_x = destino_x  
        self.destino_y = destino_y

    def desenhar(self, tela):
        self.a = atan2(self.oy - self.destino_y, self.ox - self.destino_x)

        x = self.r * cos(self.a)
        y = self.r * sin(self.a)
        b = self.a + 3 * pi / 4
        c = self.a + 5 * pi / 4
        r2 = self.r / 3
        x2 = (r2 * cos(b)) + x
        y2 = (r2 * sin(b)) + y
        x3 = (r2 * cos(c)) + x
        y3 = (r2 * sin(c)) + y

        pygame.draw.line(tela, self.cor, (self.ox, self.oy), (self.ox + x, self.oy + y), self.espessura)
        pygame.draw.line(tela, self.cor, (self.ox + x, self.oy + y), (self.ox + x2, self.oy + y2), self.espessura)
        pygame.draw.line(tela, self.cor, (self.ox + x, self.oy + y), (self.ox + x3, self.oy + y3), self.espessura)

class Jogo:
    def __init__(self, largura=700, altura=700, distancia_entre_etas=53):#self, largura=700, altura=700, distancia_entre_etas=43
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("SETAS")
        self.cor_branca = (250, 250, 250)
        self.fim_jogo = False
        self.setas = []

        dx = largura // 2
        dy = altura // 2

        for x in range(0, largura, distancia_entre_etas):
            for y in range(0, altura, distancia_entre_etas):
                r = 15
                espessura = 1
                self.setas.append(Seta(self.cor_branca, x, y, r, espessura, dx, dy))#onde começa

    def executar(self):
        while not self.fim_jogo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.fim_jogo = True

            self.tela.fill(0)

            for seta in self.setas:
                seta.desenhar(self.tela)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()