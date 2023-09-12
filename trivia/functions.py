import pygame
import math
import random
pygame.init()

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


r = 255
g = 0
b = 0
rplus = True
gplus = bplus = False



def schermgrootte(grootte: tuple[int, int] = (500,500)):
    global scherm, xscherm, yscherm
    scherm = pygame.display.set_mode(grootte)
    xscherm = grootte[0]
    yscherm = grootte[1]
    return grootte

def midden(tekst):
    return (xscherm / 2) - (tekst.get_width() / 2)

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

def change(input: bool):
    """
geeft de ingegeven bool terug in de tegenovergestelde status    
    """
    if input:
        return False
    else:
        return True
    
def truerandom(begingetal: int, eindgetal: int):
    """
geef een getal terug dat zeer random is door het getal een random aantal keer te randomizen    
    """
    getal = 0
    aantal = random.randint(1, random.randint(1,10))
    for i in range(aantal):
        getal = random.randint(begingetal, eindgetal)
    return getal