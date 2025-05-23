import pygame
import math

pygame.init()

larguraTela = 800
alturaTela = 800
tela = pygame.display.set_mode((larguraTela, alturaTela))
pygame.display.set_caption("Campo Vetorial 2D Bonito")

corPreta = (0, 0, 0)
corBranca = (255, 255, 255)

def cart_para_tela(x, y):
    x_tela = larguraTela // 2 + int(x)
    y_tela = alturaTela // 2 - int(y)
    return (x_tela, y_tela)

def campo_vetorial(x, y):
    u = x + y
    v = x - y
    m = math.sqrt(u*u + v*v)
    if m == 0:
        m = 1
    return (u/m, v/m)



def desenhaSeta(tela, cor, inicio, fim):
    pygame.draw.line(tela, cor, inicio, fim, 2)

    dx = fim[0] - inicio[0]
    dy = fim[1] - inicio[1]
    magnitude = math.hypot(dx, dy)
    if magnitude == 0:
        return

    tamanhoPonta = 5
    angulo = math.atan2(dy, dx)

    ponta1 = (fim[0] - tamanhoPonta * math.cos(angulo - math.pi / 6),
              fim[1] - tamanhoPonta * math.sin(angulo - math.pi / 6))
    ponta2 = (fim[0] - tamanhoPonta * math.cos(angulo + math.pi / 6),
              fim[1] - tamanhoPonta * math.sin(angulo + math.pi / 6))

    pygame.draw.line(tela, cor, fim, ponta1, 2)
    pygame.draw.line(tela, cor, fim, ponta2, 2)

#INICIAR junto com o arquivo funções.fun.py

rodando = True
while rodando:
    tela.fill(corPreta)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    espacamento = 23
    comprimento = 15

    for x in range(-larguraTela // 2, larguraTela // 2 + 1, espacamento):
        for y in range(-alturaTela // 2, alturaTela // 2 + 1, espacamento):
            u, v = campo_vetorial(x, y)

            modulo = math.hypot(u, v)
            if modulo != 0:
                u = (u / modulo) * comprimento
                v = (v / modulo) * comprimento
            else:
                u, v = 0, 0

            inicio = cart_para_tela(x, y)
            fim = cart_para_tela(x + u, y + v)

            desenhaSeta(tela, corBranca, inicio, fim)

    pygame.display.update()

pygame.quit()
