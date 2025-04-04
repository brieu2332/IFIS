import pygame
import math

pygame.init()
largura, altura = 800, 600
screen = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()

#varis
pontoReferencia = (505, 578)
espaço_setas = 50  
cor = (255, 255, 255)
espessura = 2 
tamanho_seta = 25  


def desenha_seta(surface, comeco, fim, cor, largura):
   
    vetorX = fim[0] - comeco[0]
    vetorY = fim[1] - comeco[1]
    distan = math.hypot(vetorX, vetorY)
    
    if distan == 0:
        return

    vetorX /= distan
    vetorY /= distan
    
    novoFim = (comeco[0] + vetorX * tamanho_seta,comeco[1] + vetorY * tamanho_seta)
    
    pygame.draw.line(surface, cor, comeco, novoFim, largura)#principal linha
    

    pontas_seta_tam = tamanho_seta * 0.3
    
    
    angle = math.atan2(vetorY, vetorX)
    
    p1 = (novoFim[0] - pontas_seta_tam * math.cos(angle - math.pi/6),novoFim[1] - pontas_seta_tam * math.sin(angle - math.pi/6))
    p2 = (novoFim[0] - pontas_seta_tam * math.cos(angle + math.pi/6),novoFim[1] - pontas_seta_tam * math.sin(angle + math.pi/6))
    
    # Desenha as pontas
    pygame.draw.line(surface, cor, novoFim, p1, largura)
    pygame.draw.line(surface, cor, novoFim, p2, largura)


######### main ###########
running = True
while running:
    screen.fill((0, 0, 0)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for x in range(espaço_setas, largura, espaço_setas):
        for y in range(espaço_setas, altura, espaço_setas):
                #def desenha_seta(surface, comeco, fim, cor, largura):
                desenha_seta(screen, (x, y), pontoReferencia, cor, espessura)

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()