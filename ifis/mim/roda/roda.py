import pygame
import math

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ponto A inicial
A = (250, 450)

# Ponto fixo B
B = (250, 100)

# Ângulo de rotação (fixo)
angle = 30
def draw_arrow(surface, start, end, color, width=2, arrow_size=20):
    """Desenha uma seta da ponta start para a ponta end"""
    pygame.draw.line(surface, color, start, end, width)
    
    # Cálculo da ponta da seta
    angle = math.atan2(end[1]-start[1], end[0]-start[0])
    p1 = (
        end[0] - arrow_size * math.cos(angle - math.pi/6),
        end[1] - arrow_size * math.sin(angle - math.pi/6)
    )
    p2 = (
        end[0] - arrow_size * math.cos(angle + math.pi/6),
        end[1] - arrow_size * math.sin(angle + math.pi/6)
    )
    
    pygame.draw.line(surface, color, end, p1, width)
    pygame.draw.line(surface, color, end, p2, width)


angleAnimacao = 0
vel=2
def rotacao(final,inicial,angle):
    angleRads = math.radians(angle)
    x,y = final
    ix, iy = inicial 

    x2 = ix + (x - ix)* math.cos(angleRads) - (y - iy) * math.sin(angleRads)
    y2 = iy + (x - ix)* math.sin(angleRads) + (y - iy) * math.cos(angleRads)

    return (x2,y2)




# Loop principal
running = True
while running:
    screen.fill((0, 0, 0))  # Fundo preto

    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    angleAnimacao += vel
    if angleAnimacao >= 360:
        angleAnimacao -= 360
    

    a_rotate = rotacao(A,B, angleAnimacao)
    
 # No loop principal, substitua os desenhos por:
    draw_arrow(screen, B, a_rotate, (255, 255, 255))
   

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
