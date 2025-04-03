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
x = (250,250)
y = (150, 400)

#encontra a direção da linha
vetorX = (y[0] - x[0])
print(vetorX)
vetorY = (y[1] - x[1])
print(vetorY)
    

#pitagoras
magnitude = math.sqrt(vetorX * vetorX + vetorY * vetorY)
print(magnitude)

tamanhoPonta = 0.3 * magnitude

#Usando math.atan2(vetory, vetorx) para encontrar o ângulo (em radianos) que a linha faz com o eixo X
angulo = math.atan2(vetorY, vetorX)
print(angulo)



anguloPrincipal = math.pi/6 #pi = 3,14, angulo 30°
print(anguloPrincipal)

#pontas da seta
pontaX = y[0] - (vetorX * math.cos(anguloPrincipal + angulo))
pontaY = y[1] - (vetorY * math.sin(anguloPrincipal + angulo))


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

    pontaX1 = y[0] - (tamanhoPonta * math.cos(anguloPonta1))
    pontaY1 = y[1] - (tamanhoPonta * math.sin(anguloPonta1))
    pontaX2 = y[0] - (tamanhoPonta * math.cos(anguloPonta2))
    pontaY2 = y[1] - (tamanhoPonta * math.sin(anguloPonta2))

    pygame.draw.line(tela, cor, fim, (pontaX1, pontaY1))
    pygame.draw.line(tela, cor, fim, (pontaX2, pontaY2))




rodando = True
while rodando:
    tela.fill(corPreta)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    desenhaSeta(tela, corBranca, x, y)

    pygame.display.update()
pygame.quit()