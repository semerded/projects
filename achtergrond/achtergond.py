import pygame
import random

pygame.init()

scherm = pygame.display.set_mode((1920 ,1080))
klok = pygame.time.Clock()

rood = (255,0,0)
oranje = (255,80,0)
geel = (255,255,0)
groen = (0,255,0)
turquise = (0,255,255)
blauw = (0,0,255)
paars = (255,0,255)
wit = (255,255,255)
minderwit = (200,200,200)
grijs = (100,100,100)
donkergrijs = (50,50,50)
zwart = (0,0,0)

shift = stop = rij = False
kleur = groen
grootte = 15
teller = 0

def display(i):
    string = ""
    for j in range(30 * grootte):
        getal = random.randint(0,1)
        string += str(getal)
    tekst = font.render(string, False, kleur)
    scherm.blit(tekst, (0, i * grootte))


while True:
    font = pygame.font.SysFont(pygame.font.get_default_font(), grootte)

    if rij:
        scherm.fill(zwart)
    klok.tick(10)


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT:
                shift = True
            if shift:
                
                if event.key == pygame.K_1:
                    kleur = groen
                if event.key == pygame.K_2:
                    kleur = rood
                if event.key == pygame.K_3:
                    kleur = blauw
                if event.key == pygame.K_4:
                    kleur = oranje
                if event.key == pygame.K_5:
                    kleur = paars
                if event.key == pygame.K_6:
                    kleur = geel
                if event.key == pygame.K_7:
                    kleur = turquise
                if event.key == pygame.K_8:
                    kleur = grijs
                if event.key == pygame.K_9:
                    kleur = wit
                if event.key == pygame.K_0:
                    stop = not stop
                if event.key == pygame.K_UP:
                    if grootte < 30:
                        grootte += 1
                if event.key == pygame.K_DOWN:
                    if grootte > 5:
                        grootte -= 1
                if event.key == pygame.K_MINUS:
                    rij = not rij
                

        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F9:
                shift = False

    if not stop:
        if rij:
            for i in range(10 * grootte):
                display(i)
        else:
            if teller < 7 * grootte:
                teller += 1
            else:
                teller = 0
            display(teller)

        
    pygame.display.flip()