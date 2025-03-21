import pygame

pygame.init()

altura = 500
larguta = 500
tela = pygame.display.set_mode(larguta, altura)

tela_ligada = True
while tela_ligada:
    tela.fill(250, 250, 250)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tela_ligada = False

pygame.quit()
    