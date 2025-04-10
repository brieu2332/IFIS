import pygame
import math

pygame.init()

# Configurações da tela
larguraTela = 500
alturaTela = 500
tela = pygame.display.set_mode((larguraTela, alturaTela))
pygame.display.set_caption("Campo Vetorial")

# Cores
corPreta = (0, 0, 0)
corBranca = (255, 255, 255)

# Função para converter coordenadas do plano cartesiano para a tela
def cart_para_tela(x, y):
    """Transforma coordenadas (x, y) do plano cartesiano para coordenadas da tela Pygame."""
    x_tela = larguraTela // 2 + x
    y_tela = alturaTela // 2 - y  # inverte o eixo Y
    return (x_tela, y_tela)

# coordenada x, coordenada y, escala s
def fvet(x, y, s):
    return (-x * s, -0.5 * y * s)

def desenhaSeta(tela, cor, inicio, fim):
    pygame.draw.line(tela, cor, inicio, fim)

    # Calcula o vetor da linha
    vetorX = fim[0] - inicio[0]
    vetorY = fim[1] - inicio[1]
    magnitude = math.hypot(vetorX, vetorY)

    # Tamanho da ponta da seta
    tamanhoPonta = 0.3 * magnitude
    angulo = math.atan2(vetorY, vetorX)

    # Ângulos das pontas
    anguloPonta1 = angulo + math.pi / 6
    anguloPonta2 = angulo - math.pi / 6

    # Coordenadas das pontas
    ponta1 = (fim[0] - tamanhoPonta * math.cos(anguloPonta1),
              fim[1] - tamanhoPonta * math.sin(anguloPonta1))
    ponta2 = (fim[0] - tamanhoPonta * math.cos(anguloPonta2),
              fim[1] - tamanhoPonta * math.sin(anguloPonta2))

    pygame.draw.line(tela, cor, fim, ponta1)
    pygame.draw.line(tela, cor, fim, ponta2)


# Loop principal
rodando = True
while rodando:
    tela.fill(corPreta)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    x=(0,0)
    y=(5,5)

    inicio = cart_para_tela(x, y)
    desenhaSeta(tela, corBranca, inicio, fim)
    # Desenha o campo vetorial
    for x in range(-200, 201, 25):
        for y in range(-200, 201, 25):
            vet = fvet(x, y, 1)
            fim = cart_para_tela(x + vet[0], y + vet[1])

    pygame.display.update()

pygame.quit()
