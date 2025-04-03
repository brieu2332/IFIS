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

# Ponto x inicial
x = (250, 450)

# Ponto fixo y
y = (250, 100)

# Pega um ponto intermediário entre x e y para as "penas"
temp_point = (
    y[0] + (x[0] - y[0]) * arrow_wing_length,
    y[1] + (x[1] - y[1]) * arrow_wing_length
)
print(y[1])

# Ângulo de rotação (fixo)
angle = 30

# Calcula o novo ponto C
# Rotaciona o ponto intermediário
C = rotate_point(temp_point[0], temp_point[1], y[0], y[1], angle)
D = rotate_point(temp_point[0], temp_point[1], y[0], y[1], -angle)

# Loop principal
running = True
while running:
    screen.fill((0, 0, 0))  # Fundo preto

    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenha os pontos e vetores
    pygame.draw.line(screen, (255, 255, 255), y, x, 2)  # Vetor yx
    pygame.draw.line(screen, (0, 255, 0), y, C, 2)  # Vetor yC (rotacionado)
    pygame.draw.line(screen, (0, 0, 255), y, D, 2)  # Vetor yC (rotacionado)

   
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
