import pygame
import math

# Inicializa o pygame
pygame.init()


def draw_arrow(surface, color, start, end):
    # Desenha o corpo da seta
    pygame.draw.line(surface, color, start, end, 3)
    
    # Calcula a direção do vetor da seta (dx, dy)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    



# Configurações da tela
largura = 500
altura = 500
screen = pygame.display.set_mode((largura, altura))
tamanho = 50

# Loop principal
rodando_tela = True
while rodando_tela:
    screen.fill((0, 0, 0))  # Limpa a tela

    # Desenha a seta com a cabeça em ângulo de 30 graus
    draw_arrow(screen, (255, 255, 255), (100, 100), (400, 400))
    

    # Desenha as linhas verticais
    for x in range(0, largura, tamanho):
        pygame.draw.line(screen, (255,255,255), (x, 0), (x, altura), 1)

    # Desenha as linhas horizontais
    for y in range(0, altura, tamanho):
        pygame.draw.line(screen, (255,255,255), (0, y), (largura, y), 1)

    pygame.display.flip()  # Atualiza a tela

    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando_tela = False

pygame.quit()
