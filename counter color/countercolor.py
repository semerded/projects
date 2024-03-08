import pygame, json, os


# if os.path.isfile('dingen\\handige dingen\\spacebarclick\\spacebar_data.json') is False:
#     raise Exception("File not found")

pygame.init()

klok = pygame.time.Clock()
scherm = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)


rood = (255,0,0)
oranje = (255,80,0)
geel = (255,255,0)
groen = (0,255,0)
turquise = (0,255,255)
blauw = (0,0,255)
paars = (255,0,255)
roze = (255, 0, 100)
wit = (255,255,255)
minderwit = (200,200,200)
grijs = (100,100,100)
zwart = (0,0,0)

zwartteller = shutdownteller = 0
resize = tick = shift = afsluiten = shutdown = delete = escape = False



kleurlijst = [rood, oranje, geel, groen, turquise, blauw, roze, paars, grijs, wit]

with open('counter.json') as fp:
    savefile = json.load(fp)
teller = savefile['nummer']
kleur = savefile['kleur']
if kleur == 1:
    kleur = True
else:
    kleur = False
grootte = savefile['size']
texthoogte = savefile['height']



def sec_to_time(secinput: int):
    dag = secinput // 86400
    uur = (secinput - 86400 * dag ) // 3600
    minuut = (secinput - (86400 * dag) - (uur * 3600)) // 60
    sec = secinput - (86400 * dag) - (uur * 3600) - (minuut * 60)   
    return f"{dag}d {uur}h {minuut}m {sec}s"
    



while True:
    if tick:
        klok.tick(10)
    else:
        klok.tick(100)
    if not kleur:
        scherm.fill(zwart)
    grotetext_size = pygame.font.SysFont(pygame.font.get_default_font(), grootte)
    schermx = scherm.get_width()
    schermy = scherm.get_height()

    if texthoogte > schermy:
        texthoogte = schermy / 2

    teller += 11111
    tellerstring = str(teller)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            afsluiten = True
        if event.type == pygame.WINDOWMAXIMIZED or event.type == pygame.WINDOWSIZECHANGED:
            resize = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT:
                shift = True
            if shift:
                if event.key == pygame.K_t:
                    tick = not tick
                if event.key == pygame.K_k:
                    kleur = not kleur
                if event.key == pygame.K_c:
                    texthoogte = schermy / 2                    
                if event.key == pygame.K_s:
                    if grootte < 250:
                        grootte += 50
                    else:
                        grootte = 50
                if event.key == pygame.K_DELETE:
                    delete = True
                if delete:
                    if event.key == pygame.K_ESCAPE:
                        escape = True
                        

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                shift = False
            if event.key == pygame.K_DELETE:
                delete = False
            if event.key == pygame.K_ESCAPE:
                escape = False
    if shift:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if texthoogte > 10:
                texthoogte -= 10
        if keys[pygame.K_DOWN]:
            if texthoogte + grootte /2 + 30 < schermy:
                texthoogte += 10
                    
    if escape:
        shutdownteller += 1
        if tick:
            if shutdownteller > 5:
                shutdown = True
        else:
            if shutdownteller > 50:
                shutdown = True

    for i in range(len(tellerstring)):
        if kleur:
            kleurteller = int(tellerstring[-i -1])
            pygame.draw.rect(scherm, kleurlijst[kleurteller], pygame.Rect(schermx - ((schermx / 10) * i + (schermx / 10)), 0, schermx / 10, schermy))
        text = grotetext_size.render(f"{tellerstring[-i - 1]}", False, minderwit)

        scherm.blit(text, (schermx - ((schermx / 10) * i ) - (text.get_width() / 2) - (schermx / 20), texthoogte))
        pygame.display.update()

        if resize:
            zwartteller += 1
            if zwartteller < 10:
                scherm.fill(zwart)
                pygame.display.flip()
            else:
                resize = False
                zwartteller = 0

    if teller % 10000 == 0 or afsluiten or shutdown:
        savefile['nummer'] = teller
        if kleur:
            savefile['kleur'] = 1
        else:
            savefile['kleur'] = 0
        savefile['size'] = grootte
        savefile['height'] = texthoogte

        with open('counter.json', 'w') as json_file:
            json.dump(savefile, json_file, indent = 4, separators=(',',': '))
        if afsluiten:
            exit()
        if shutdown:
            shutdown = False
            os.system('shutdown /p')
    pygame.display.set_caption(f"uptime: {sec_to_time(int(teller / 100))}")