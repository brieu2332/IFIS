import pygame
import math

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Função para rotacionar um ponto ao redor de outro
def rotate_point(px, py, cx, cy, angle):
    angle_rad = math.radians(angle)
    x_new = cx + (px - cx) * math.cos(angle_rad) - (py - cy) * math.sin(angle_rad)
    y_new = cy + (px - cx) * math.sin(angle_rad) + (py - cy) * math.cos(angle_rad)
    return x_new, y_new

# Modifique o cálculo de C e D para encurtar as linhas
arrow_wing_length = 0.3  # Fração do comprimento da linha principal

# Ponto A inicial
A = (250, 450)

# Ponto fixo B
B = (250, 100)

# Pega um ponto intermediário entre A e B para as "penas"
temp_point = (
    B[0] + (A[0] - B[0]) * arrow_wing_length,
    B[1] + (A[1] - B[1]) * arrow_wing_length
)
print(B[1])

# Ângulo de rotação (fixo)
angle = 30

# Calcula o novo ponto C
# Rotaciona o ponto intermediário
C = rotate_point(temp_point[0], temp_point[1], B[0], B[1], angle)
D = rotate_point(temp_point[0], temp_point[1], B[0], B[1], -angle)

# Loop principal
running = True
while running:
    screen.fill((0, 0, 0))  # Fundo preto

    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenha os pontos e vetores
    pygame.draw.line(screen, (255, 255, 255), B, A, 2)  # Vetor BA
    pygame.draw.line(screen, (0, 255, 0), B, C, 2)  # Vetor BC (rotacionado)
    pygame.draw.line(screen, (0, 0, 255), B, D, 2)  # Vetor BC (rotacionado)

   
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
