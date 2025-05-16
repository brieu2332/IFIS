import pygame
import math

pygame.init()

larguraTela = 500
alturaTela = 500
tela = pygame.display.set_mode((larguraTela, alturaTela))

corPreta = (0,0,0)
corBranca = (255,255,255)
corSLA = (0,225,0)

#posição de inicio e fim da linha
inicio = (250,250)
fim = (150, 400)


def desenhaSeta(tela, cor, inicio, fim):
    pygame.draw.line(tela, cor, inicio, fim)
    
    vetorX = (fim[0] - inicio[0])
    vetorY = (fim[1] - inicio[1])

    magnitude = math.sqrt(vetorX * vetorX + vetorY * vetorY)

    if magnitude == 0:
         return

    tamanhoPonta = 0.3 * magnitude

    angulo = math.atan2(vetorY, vetorX)

    anguloPonta1 = angulo + math.pi/6
    anguloPonta2 = angulo - math.pi/6

    pontaX1 = fim[0] - (tamanhoPonta * math.cos(anguloPonta1))
    pontaY1 = fim[1] - (tamanhoPonta * math.sin(anguloPonta1))
    
    pontaX2 = fim[0] - (tamanhoPonta * math.cos(anguloPonta2))
    pontaY2 = fim[1] - (tamanhoPonta * math.sin(anguloPonta2))

    pygame.draw.line(tela, cor, fim, (pontaX1, pontaY1))
    pygame.draw.line(tela, cor, fim, (pontaX2, pontaY2))




rodando = True
while rodando:
    tela.fill(corPreta)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    desenhaSeta(tela, corBranca, inicio, fim)

    pygame.display.update()
pygame.quit()