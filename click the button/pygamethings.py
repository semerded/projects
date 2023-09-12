import pygame
import math
import random
pygame.init()
fps_teller = gametijd_teller = 0
donkerkleursetup = False

r = 255
g = 0
b = 0
rplus = True
gplus = bplus = False

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





def schermgrootte(grootte: tuple[int, int] = (500,500)):
    global scherm
    scherm = pygame.display.set_mode(grootte)
    return grootte

def klok_setup():
    global fpsklok
    fpsklok = pygame.time.Clock()
    
def gametijd_counter(fps: int):
    fpsklok.tick(fps)
    global fps_teller, gametijd_teller
    fps_teller += 1
    if fps_teller % fps == 0:
        gametijd_teller += 1


def donkersetup(kleur0: tuple[int,int,int], kleur1: tuple[int,int,int] ):
    """
geef 2 geldige kleurwaardes in\ndeze kunnen verwisseld worden met functie "donkermodus"
    """
    global kleur0_setup, kleur1_setup
    def error():
        print("kleur niet geldig [funcie donkersetup]")
        exit()
    global donkerkleursetup
    donkerkleursetup = True
    if len(kleur0) and len(kleur1) == 3:
        for i in range(3):
            if kleur0[i] > 255 or kleur0[i] < 0 or  kleur1[i] > 255 or kleur1[i] < 0:
                error()
        kleur0_setup = kleur0
        kleur1_setup = kleur1
    else:
        error()

def donkermodus(input: bool):
    """
verandert kleur0 met kleur1 en andersom\n
bv: input = False --> kleur0 = zwart en kleur1 = wit\n
    input = True --> kleur0 = wit en kleur1 = zwart\n
kleuren zijn aanpasbaar met functie "donkersetups"
    """
    if donkerkleursetup:
        if input:
            return kleur1_setup, kleur0_setup
        else:
            return kleur0_setup, kleur1_setup
    else:
        if input:
            return zwart, wit
        else:
            return wit, zwart
        

def fpscounter(fpsgrote: int = 25, xpositie: int = 200, ypositie: int = 950):
    kleinetekst = pygame.font.SysFont(pygame.font.get_default_font(), fpsgrote)
    fps = kleinetekst.render(f"{int(fpsklok.get_fps())}", False, (50, 255, 0))
    scherm.blit(fps, (xpositie, ypositie))

def cirkeldetectie(middencirkel: tuple[int, int], radius: int, activate: bool = True, draw: bool = True, kleurcirkel: tuple[int,int,int] = (0,0,0)):
    """
berekent of de muiscursor zich in de cirkel bevindt --> geeft True terug als dit zo is\n
geef het midden van de cirkel (in een tuple) en de radius in\n
de kleur is standaard zwart
    """
    global incirkel, mouse_pos
    if activate:
        mouse_pos = pygame.mouse.get_pos()
        distance_to_circle = math.sqrt((mouse_pos[0] - middencirkel[0]) ** 2 + (mouse_pos[1] - middencirkel[1]) ** 2)
        if distance_to_circle <= radius:
            incirkel = True
        else:
            incirkel = False
    else:
        incirkel = False
    if draw:
        pygame.draw.circle(scherm, kleurcirkel, middencirkel, radius )
    return incirkel

def vierkantdetectie(xpositie: int, ypositie: int, lengte: int, hoogte: int, kleurvierkant: tuple[int,int,int] = (0,0,0), rand: int = 0, afvlakking: int = -1):
    """
berekent of de muiscursor zich in het vierkant bevindt --> geeft True terug als dit zo is\n
geef de x en y positie van het vierkant en de lengte en hoogte\n
de kleur is standaard zwart
    """
    global inrect, mouse_pos
    rect = pygame.draw.rect(scherm, kleurvierkant, pygame.Rect(xpositie, ypositie, lengte, hoogte), rand, afvlakking)
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        inrect = True
    else:
        inrect = False
    return inrect

def rgb(rgbsnelheid: int = 1):
    """
maakt een rgb kleur\nreturnt een tuple die deze cycle zal volgen
    """
    global r, g, b, gplus, bplus, rplus
    if r >= 250:
        rplus = False
        gplus = True
    if gplus:
        r -= rgbsnelheid
        g += rgbsnelheid
    
    if g >= 250:
        gplus = False
        bplus = True
    if bplus:
        g -= rgbsnelheid
        b += rgbsnelheid

    if b >= 250:
        bplus = False
        rplus = True
    if rplus:
        b -= rgbsnelheid
        r += rgbsnelheid
    
    while r > 255:
        r -= 1
    while g > 255:
        g -= 1
    while b > 255:
        b -= 1
    while r < 0:
        r += 1
    while g < 0:
        g += 1
    while b < 0:
        b += 1
    return (r, g, b)