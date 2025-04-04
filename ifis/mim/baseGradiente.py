import pygame
import math

pygame.init()

# Configurações da tela
larguraTela = 500
alturaTela = 500
tela = pygame.display.set_mode((larguraTela, alturaTela))

# Cores
corPreta = (0, 0, 0)
corBranca = (255, 255, 255)

def desenhaSeta(tela, cor, inicio, fim):
    
    # Desenha a linha principal
    pygame.draw.line(tela, cor, inicio, fim)

    # Calcula o vetor da linha
    vetorX = fim[0] - inicio[0]
    vetorY = fim[1] - inicio[1]

    # Calcula a magnitude do vetor (comprimento da linha)
    magnitude = math.sqrt(vetorX * vetorX + vetorY * vetorY)
   
    # Define o tamanho da ponta da seta
    tamanhoPonta = 0.3 * magnitude

    # Calcula o ângulo da linha
    angulo = math.atan2(vetorY, vetorX)

    # Define os ângulos das pontas da seta
    anguloPonta1 = angulo + math.pi / 6  # 30°
    anguloPonta2 = angulo - math.pi / 6  # -30°

    # Calcula as coordenadas das pontas da seta
    pontaX1 = fim[0] - tamanhoPonta * math.cos(anguloPonta1)
    pontaY1 = fim[1] - tamanhoPonta * math.sin(anguloPonta1)
    pontaX2 = fim[0] - tamanhoPonta * math.cos(anguloPonta2)
    pontaY2 = fim[1] - tamanhoPonta * math.sin(anguloPonta2)

    # Desenha as duas linhas da ponta da seta
    pygame.draw.line(tela, cor, fim, (pontaX1, pontaY1))
    pygame.draw.line(tela, cor, fim, (pontaX2, pontaY2))

# Loop principal
rodando = True
while rodando:
    tela.fill(corPreta)

    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Desenha um grid de setas
    for x in range(50, 500, 50):
        for y in range(50, 500, 50):
            desenhaSeta(tela, corBranca, (x, y), (x + 25, y + 25))

    pygame.display.update()

pygame.quit()
