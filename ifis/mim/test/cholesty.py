import pygame
import math
import numpy as np


pygame.init()

# Configurações da tela
larguraTela = 800
alturaTela = 800
tela = pygame.display.set_mode((larguraTela, alturaTela))

# Cores
corPreta = (0, 0, 0)
corBranca = (255, 255, 255)

# coordenada x, coordenada y, scala s

def desenhaSeta(tela, cor, inicio, fim):
    
    # Desenha a linha principal
    pygame.draw.line(tela, cor, cart_para_cg(inicio), cart_para_cg(fim))

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
    pygame.draw.line(tela, cor, cart_para_cg(fim), cart_para_cg((pontaX1, pontaY1)))
    pygame.draw.line(tela, cor, cart_para_cg(fim), cart_para_cg((pontaX2, pontaY2)))


# x= x, y=y 
def fvet(x, y, s):
    #return (x*s, y*s)
    #return (x * s, math.sin(x)*y*s)
    #return (x*s, -y*s)
    #return (x*s, -0,5*y*s)
    #return (-y*s, x*s)
    u =  (math.sin(x) + math.sin(y))
    v=  (math.sin(x) - math.sin(y)) 
    m = (u**2 + v**2 )**(0.5) 
    if m == 0:
        m = 1

    u = u/m*s 
    v = v/m*s
    return(u,v) 

    

def cart_para_cg(w):
    return (w[0] + larguraTela//2, -w[1] + alturaTela//2)


# Loop principal
rodando = True
while rodando:
    tela.fill(corPreta)

    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

     # Desenha um grid de setas
    for x in np.linspace(-4, +4, 25):
        for y in np.linspace(-4, 4, 25):
            print('bka') 
            vet = fvet(x, y, 10)
            inicio = (x*100, y*100)
            fim = (x*100 + vet[0], y*100 + vet[1])
            desenhaSeta(tela, corBranca, inicio, fim)

    # inicio = ( 0,0)
    # fim = (-100,0)
    # desenhaSeta(tela, corBranca, inicio, fim)
    


    pygame.display.update()

pygame.quit()
