from pygamethings import *
from pythings import *

geluid = pygame.mixer.music.load("funkytown.wav")


klok = pygame.time.Clock()
scherm_size = schermgrootte((1000, 500))
scherm = pygame.display.set_mode(scherm_size)
kleinetext_size = pygame.font.SysFont(pygame.font.get_default_font(), 50)
grotetext_size = pygame.font.SysFont(pygame.font.get_default_font(), 100)
kleurcirkel = rood
kleurswitch = escape = click = rgbactive = False

pygame.display.set_caption("Try to click the button")

while True:
    klok.tick(1000)
    kleur0, kleur1 = donkermodus(kleurswitch)
    if rgbactive:
        scherm.fill(rgb(5))
    else:
        scherm.fill(kleur0)

    for event in pygame.event.get():
        """kruisje"""
        if event.type == pygame.QUIT:
            kleurswitch = change(kleurswitch)
        """escape"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                escape = True
            else:
                rgbactive = change(rgbactive)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                escape = False
        """muisklik"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
        """minimizen/wegkliken"""
        if event.type == pygame.WINDOWMINIMIZED or event.type == pygame.WINDOWFOCUSLOST:
            pygame.mixer.music.play(-1, 0.0)
        if event.type == pygame.WINDOWMAXIMIZED or event.type == pygame.WINDOWFOCUSGAINED:
            pygame.mixer.music.stop()

    stopgame = cirkeldetectie((800,250), 50, True, True, kleurcirkel)
    cirkel = cirkeldetectie((800,250), 75, True, False)
    if cirkel and not escape:
        pygame.mouse.set_pos((100, 250))
    if stopgame:
        kleurcirkel = groen
        if click:
            exit()
    else:
        kleurcirkel = rood

    pygame.display.flip()