import pygame
import sys
import math

# Inicializa o Pygame
pygame.init()

# Configurações da janela
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Linha Perpendicular")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Centro do plano cartesiano (origem)
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

def to_pygame(x, y):
    """Converte coordenadas cartesianas para Pygame."""
    return CENTER_X + x, CENTER_Y - y

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # --- Linha Azul (Vertical) ---
    comeco = to_pygame(-100, 150)
    fim = to_pygame(100, -150)
    pygame.draw.line(screen, BLUE, comeco, fim, 3)

    # --- Linha Vermelha (Perpendicular à Azul) ---
    # Calcula o vetor da linha azul
    vetor_azul_x = fim[0] - comeco[0]
    vetor_azul_y = fim[1] - comeco[1]

    # Vetor perpendicular (90° anti-horário)
    vetor_perp_x = -vetor_azul_y
    vetor_perp_y = vetor_azul_x

    # Normaliza o vetor perpendicular
    comprimento = math.sqrt(vetor_perp_x**2 + vetor_perp_y**2)
    if comprimento > 0:
        vetor_perp_x /= comprimento
        vetor_perp_y /= comprimento

    # Define o comprimento da linha vermelha (metade da azul)
    novo_comprimento = math.sqrt(vetor_azul_x**2 + vetor_azul_y**2) / 2

    # Calcula o ponto final da linha vermelha
    fim_vermelho_x = fim[0] + vetor_perp_x * novo_comprimento
    fim_vermelho_y = fim[1] + vetor_perp_y * novo_comprimento

    # Desenha a linha vermelha
    pygame.draw.line(screen, RED, fim, (fim_vermelho_x, fim_vermelho_y), 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()