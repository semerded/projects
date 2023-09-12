import pygame
from random import randint

pygame.init()
scherm = pygame.display.set_mode((1000, 800))
klok = pygame.time.Clock()

bloktext_size = pygame.font.SysFont(pygame.font.get_default_font(), 40)
grotetext_size = pygame.font.SysFont(pygame.font.get_default_font(), 100)
image = pygame.image.load("yes.jpg")
image = pygame.transform.scale(image, (1000,800))

rol_dobbel = rolblock = plaatsen = geplaatst = yahtzee_gerold = subtotaal_gehaald = punten = setup = False
yahtzee_nietgeplaatst = game_over =  True
gedobbeldewaardes_lijst = []
rol_teller = punt = yahtzee = subtotaal = 0
keuze_plaats = 1
geplaatse_plaats_lijst = []
gesorteerde_dobbelwaardes_lijst = []
vastgezette_stenen = []
not_yahtzee = -1
keuzes = 3

blok_tekst_lijst = ["3 Of A",  "Carré",  " Full" , "  Kl.", "  Gr.",  "Chan"]
blok_tekst2_lijst = [" Kind", "", "House", "Straat", "Straat", "ge..."]   
groottestraat1 = [1, 2, 3, 4, 5]
groottestraat2 = [2, 3, 4, 5, 6]
kleinestraat1 = [1,2,3,4]
kleinestraat2 = [2,3,4,5]
kleinestraat3 = [3,4,5,6]

def invertcolor(invert):
    global kleur0, kleur1
    if invert:
        kleur0 = (0,0,0)
        kleur1 = (155,155,155)
    else:
        kleur0 = (255,255,255)
        kleur1 = (0,0,0)

def groteblock(keuzeblok):
    global size_block, size_circle
    if keuzeblok:
        size_block = 150
        size_circle = 15
    else:
        size_block = 100
        size_circle = 10

def blok(blokkeuze, xblock, yblock, kleur):
    if size_block == 100:
        rand = 20
    else:
        rand = 30
    pygame.draw.rect(scherm, kleur, pygame.Rect(xblock, yblock, size_block, size_block), 0, rand)

    if blokkeuze == 1:
        pygame.draw.circle(scherm, kleur1, (xblock + (50 * size_circle/10), yblock + (50 * size_circle/10)), size_circle)
    elif blokkeuze == 2:
        pygame.draw.circle(scherm, kleur1, (xblock + (75 * size_circle/10), yblock + (25 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (25 * size_circle/10), yblock + (75 * size_circle/10)), size_circle)
    elif blokkeuze == 3:
        pygame.draw.circle(scherm, kleur1, (xblock + (50 * size_circle/10), yblock + (50 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (75 * size_circle/10), yblock + (25 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (25 * size_circle/10), yblock + (75 * size_circle/10)), size_circle)
    elif blokkeuze == 4:
        pygame.draw.circle(scherm, kleur1, (xblock + (25 * size_circle/10), yblock + (25 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (75 * size_circle/10), yblock + (25 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (75 * size_circle/10), yblock + (75 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (25 * size_circle/10), yblock + (75 * size_circle/10)), size_circle)
    elif blokkeuze == 5:
        pygame.draw.circle(scherm, kleur1, (xblock + (50 * size_circle/10), yblock + (50 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (25 * size_circle/10), yblock + (25 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (75 * size_circle/10), yblock + (25 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (75 * size_circle/10), yblock + (75 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (25 * size_circle/10), yblock + (75 * size_circle/10)), size_circle)
    elif blokkeuze == 6:
        pygame.draw.circle(scherm, kleur1, (xblock + (25 * size_circle/10), yblock + (25 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (75 * size_circle/10), yblock + (25 * size_circle/10)), size_circle)  
        pygame.draw.circle(scherm, kleur1, (xblock + (75 * size_circle/10), yblock + (50 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (25 * size_circle/10), yblock + (50 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (75 * size_circle/10), yblock + (75 * size_circle/10)), size_circle)
        pygame.draw.circle(scherm, kleur1, (xblock + (25 * size_circle/10), yblock + (75 * size_circle/10)), size_circle)

def blok_speciaal(xblock, yblock, tekst, tekst2):
    if size_block == 100:
        rand = 20
    else:
        rand = 30
    pygame.draw.rect(scherm, kleur0, pygame.Rect(xblock, yblock, size_block, size_block), 0, rand, rand, rand, rand)
    bloktext = bloktext_size.render(tekst, False, kleur1)
    bloktext2 = bloktext_size.render(tekst2, False, kleur1)
    scherm.blit(bloktext, (xblock + 10, yblock + 25))
    scherm.blit(bloktext2, (xblock + 10, yblock + 60))

def rollen():
    groteblock(True)
    for i in range(5):
        blok(gedobbeldewaardes_lijst[i], 10 + (i * 160), 625, kleur0)  

def vastzetten(nummer):
    if nummer in vastgezette_stenen:
        vastgezette_stenen.remove(nummer)
    else:
        vastgezette_stenen.append(nummer)

def correctie(terug):
    global keuze_plaats
    for i in range(2):
        if terug:
            if yahtzee_gerold or yahtzee_nietgeplaatst:
                if keuze_plaats == 0:
                    keuze_plaats = 13
            else:
                if keuze_plaats == 0:
                    keuze_plaats = 12
            while True:
                if keuze_plaats in geplaatse_plaats_lijst:
                    keuze_plaats -= 1
                else:
                    break
        else:
            if yahtzee_gerold or yahtzee_nietgeplaatst:
                if keuze_plaats == 14:
                    keuze_plaats = 1
            else:
                if keuze_plaats == 13:
                    keuze_plaats = 1
            while True:
                if keuze_plaats in geplaatse_plaats_lijst:
                    keuze_plaats += 1
                else:
                    break

"""setup"""
invertcolor(False)

while True: # game loop
    while game_over:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over = False

        scherm.fill((0,0,0))
        scherm.blit(image, (0,0))
        fadeout = pygame.Surface((1000, 800))
        fadeout.fill((120, 120, 120))  
        fadeout.set_alpha(200)
        scherm.blit(fadeout, (0, 0))

        if punten:
            puntentext = grotetext_size.render(f"punten: {punt}", False, (0,0,0))
            if subtotaal_gehaald:
                subtotaaltext = grotetext_size.render(f"subtotaal: {subtotaal}", False, (0, 255, 0))
            else:
                subtotaaltext = grotetext_size.render(f"subtotaal: {subtotaal}", False, (0,0,0))
            scherm.blit(puntentext, (500 - puntentext.get_width() / 2, 100))
            scherm.blit(subtotaaltext, (500 - puntentext.get_width() / 2, 300))
        drukenter = grotetext_size.render(f"DRUK ENTER", False, (255,0,0))
        scherm.blit(drukenter, (500 - drukenter.get_width() / 2, 650))
            
        if not game_over:
            setup = True
            break
        pygame.display.flip()

    if setup:
        rol_dobbel = rolblock = plaatsen = geplaatst = yahtzee_gerold = game_over = subtotaal_gehaald = False
        yahtzee_nietgeplaatst = True
        gedobbeldewaardes_lijst = []
        rol_teller = punt = yahtzee = subtotaal = 0
        keuze_plaats = 1
        geplaatse_plaats_lijst = []
        gesorteerde_dobbelwaardes_lijst = []
        vastgezette_stenen = []
        not_yahtzee = -1
        keuzes = 3
        punten = True
        setup = False

    while True:
        klok.tick(60)
        vastgezette_stenen.sort()
        if kleur0 == (0, 0, 0):
            scherm.fill((120, 20, 20))
            pygame.draw.rect(scherm, (20,20,120), pygame.Rect(0, 600, 1000, 200))
        else:
            scherm.fill((220, 213, 185))
            pygame.draw.rect(scherm, (20,20,20), pygame.Rect(0, 600, 1000, 200))

        for i in range(5):
            pygame.draw.rect(scherm, kleur0, pygame.Rect(10 + (i * 160), 625, 150, 150), 0, 30, 30, 30, 30)

        """inputs"""
        for i in range(6):
            if gesorteerde_dobbelwaardes_lijst.count(i + 1) == 5:
                yahtzee_gerold = True
                break
            else:
                yahtzee_gerold = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    if kleur0 == (0,0,0):
                        invertcolor(False)
                    else:
                        invertcolor(True) 
                if not rolblock and not keuzes == 0:
                    if event.key == pygame.K_SPACE:
                        rol_dobbel = rolblock = plaatsen = True
                        rol_teller = 0
                        keuzes -= 1
                        keuze_plaats = 1
                        while True:
                            if keuze_plaats in geplaatse_plaats_lijst:
                                keuze_plaats += 1
                            else:
                                break
                if not keuzes == 3:
                    if plaatsen:
                        if event.key == pygame.K_LEFT:
                            keuze_plaats -= 1
                            correctie(True)
                        if event.key == pygame.K_RIGHT:
                            keuze_plaats += 1
                            correctie(False)
                    if event.key == pygame.K_RETURN:
                        geplaatst = rolblock = True
                        plaatsen = False
                        if not keuze_plaats == 13:
                            geplaatse_plaats_lijst.append(keuze_plaats)
                        else:
                            if yahtzee_nietgeplaatst and not yahtzee_gerold:
                                yahtzee_nietgeplaatst = False
                                not_yahtzee = yahtzee
                                yahtzee += 1
                        if len(geplaatse_plaats_lijst) == 12 and not yahtzee_nietgeplaatst:
                            game_over = True

                        vastgezette_stenen = []
                        keuzes = 3
                if event.key == pygame.K_1:
                    vastzetten(0)
                if event.key == pygame.K_2:
                    vastzetten(1)
                if event.key == pygame.K_3:
                    vastzetten(2)
                if event.key == pygame.K_4:
                    vastzetten(3)
                if event.key == pygame.K_5:
                    vastzetten(4)
                        

        if rol_dobbel:
            rol_teller += 1
            if rol_teller < 30:
                hulplijst = gedobbeldewaardes_lijst
                gedobbeldewaardes_lijst = []
                gesorteerde_dobbelwaardes_lijst = []
                for i in range(5):
                    if not i in vastgezette_stenen:
                        gedobbeldewaardes_lijst.append(randint(1,6))
                    else:
                        gedobbeldewaardes_lijst.append(hulplijst[i])
                gesorteerde_dobbelwaardes_lijst = sorted(gedobbeldewaardes_lijst)
            elif rol_teller > 45:
                rolblock = False
            rollen()
        if keuzes == 0:
            plaatsen = True

        for i in range(5):
            if i in vastgezette_stenen:
                blok(gedobbeldewaardes_lijst[i], 10 + (i * 160), 625, (255, 0,0))
        

        if plaatsen:
            if keuze_plaats == 13:
                xplaatser = 770
                if yahtzee > 0:
                    hoogte = 520
                else:
                    hoogte = 465
            elif keuze_plaats <= 6:
                xplaatser = 10 + ((keuze_plaats - 1) * 110)
                hoogte = 175
            else:
                xplaatser = 10 + ((keuze_plaats - 7) * 110)
                hoogte = 465
            pygame.draw.polygon(scherm, (240, 143, 27), ((xplaatser, hoogte), (xplaatser + 100, hoogte), (xplaatser + 50, hoogte - 50)))
        
        """al reeds gekozen stenen tonen"""
        for i in geplaatse_plaats_lijst:
            if i <= 6:
                xgeplaatst = 10 + ((i - 1) * 110)
                ygeplaatst = 125
            else:
                xgeplaatst = 10 + ((i - 7) * 110)
                ygeplaatst = 415
            pygame.draw.rect(scherm, (0, 255, 80), pygame.Rect(xgeplaatst, ygeplaatst, 100, 50), 0, 20, 20, 20, 20)
        
        for i in range(yahtzee):
            if i == not_yahtzee:
                pygame.draw.polygon(scherm, (255, 0, 0), ( (680 + (i * 60), 415), (730 + (i * 60), 415),  (720 + (i * 60), 465), (670 + (i * 60), 465)))
            else:
                pygame.draw.polygon(scherm, (0, 255, 80), ( (680 + (i * 60), 415), (730 + (i * 60), 415),  (720 + (i * 60), 465), (670 + (i * 60), 465)))
        
        groteblock(False)
        for i in range(6):
            blok(i + 1, 10 + (i * 110), 10, kleur0)
            blok_speciaal(10 + (i * 110), 300, blok_tekst_lijst[i], blok_tekst2_lijst[i])
        pygame.draw.rect(scherm, kleur0, pygame.Rect(670, 300, 300, 100), 0, 20, 20, 20, 20)
        bloktext = grotetext_size.render("Hatsjee", False, kleur1)
        scherm.blit(bloktext, (690, 320))

        for i in range(keuzes):
            pygame.draw.polygon(scherm, kleur0, ( (820 + (i * 60), 600), (870 + (i * 60), 600),  (860 + (i * 60), 670), (810 + (i * 60), 670)))


        """punten telling"""
        if geplaatst:
            vorig_punt = punt
            if keuze_plaats == 1: # eenen
                punt += gesorteerde_dobbelwaardes_lijst.count(1)
                subtotaal += (punt - vorig_punt)
                geplaatst = False
            if keuze_plaats == 2: # tweeën
                punt += (gesorteerde_dobbelwaardes_lijst.count(2) * 2)
                subtotaal += (punt - vorig_punt)
                geplaatst = False
            if keuze_plaats == 3: # drieën
                punt += (gesorteerde_dobbelwaardes_lijst.count(3) * 3)
                subtotaal += (punt - vorig_punt)
                geplaatst = False
            if keuze_plaats == 4: # vieren
                punt += (gesorteerde_dobbelwaardes_lijst.count(4) * 4)
                subtotaal += (punt - vorig_punt)
                geplaatst = False
            if keuze_plaats == 5: # vijfen
                punt += (gesorteerde_dobbelwaardes_lijst.count(5) * 5)
                subtotaal += (punt - vorig_punt)
                geplaatst = False
            if keuze_plaats == 6: # zessen
                punt += (gesorteerde_dobbelwaardes_lijst.count(6) * 6)
                subtotaal += (punt - vorig_punt)
                geplaatst = False
            if keuze_plaats == 7: # three of a kind
                for i in range(6): 
                    if gesorteerde_dobbelwaardes_lijst.count(i + 1) >= 3:
                        punt += sum(gesorteerde_dobbelwaardes_lijst)
                geplaatst = False
            if keuze_plaats == 8: # carré
                for i in range(6):
                    if gesorteerde_dobbelwaardes_lijst.count(i + 1) >= 4:
                        punt += sum(gesorteerde_dobbelwaardes_lijst)
                geplaatst = False
            if keuze_plaats == 9: # full house
                if gesorteerde_dobbelwaardes_lijst[0] == gesorteerde_dobbelwaardes_lijst[1] == gesorteerde_dobbelwaardes_lijst[2] and gesorteerde_dobbelwaardes_lijst[3] == gesorteerde_dobbelwaardes_lijst[4]:
                    punt += 25
                elif gesorteerde_dobbelwaardes_lijst[0] == gesorteerde_dobbelwaardes_lijst[1] and gesorteerde_dobbelwaardes_lijst[2] == gesorteerde_dobbelwaardes_lijst[3] == gesorteerde_dobbelwaardes_lijst[4]:
                    punt += 25
                geplaatst = False
            if keuze_plaats == 10: # kleine straat 
                if all(item in gesorteerde_dobbelwaardes_lijst for item in kleinestraat1) or all(item in gesorteerde_dobbelwaardes_lijst for item in kleinestraat2) or all(item in gesorteerde_dobbelwaardes_lijst for item in kleinestraat3):
                    punt += 30
                geplaatst = False
            if keuze_plaats == 11: # grootte straat 
                if gesorteerde_dobbelwaardes_lijst == groottestraat1 or gesorteerde_dobbelwaardes_lijst == groottestraat2:
                        punt += 40
                geplaatst = False
            if keuze_plaats == 12: # change
                punt += sum(gesorteerde_dobbelwaardes_lijst)
                geplaatst = False
            if keuze_plaats == 13:
                for i in range(6):
                    if gesorteerde_dobbelwaardes_lijst.count(i + 1) == 5:
                        yahtzee += 1
                        if yahtzee == 1 and yahtzee_nietgeplaatst:
                            punt += 50
                        elif yahtzee == 2 and not yahtzee_nietgeplaatst:
                            punt += 50
                        else:
                            punt += 100
                geplaatst = False

        if subtotaal >= 63 and not subtotaal_gehaald:
            punt += 35
            subtotaal_gehaald = True
            
        """punten tonen op scherm"""
        puntentext = bloktext_size.render(f"punten: {punt}", False, kleur0)
        if subtotaal_gehaald:
            subtotaaltext = bloktext_size.render(f"subtotaal: {subtotaal}", False, (0, 255, 0))
        else:
            subtotaaltext = bloktext_size.render(f"subtotaal: {subtotaal}", False, kleur0)
        scherm.blit(puntentext, (810, 680))
        scherm.blit(subtotaaltext, (810, 710))

        """kijken of het spel gedaan is"""
        if game_over:
            break

        pygame.display.flip()