import json, os, pygame

JSONFILEPATH = "toolbelt setup.json"
if os.path.isfile(JSONFILEPATH) is False:
    raise Exception("File not found")
with open(JSONFILEPATH) as filepath:
    savefile = json.load(filepath)

pygame.init()
disInfo = pygame.display.Info()

display = pygame.display.set_mode((disInfo.current_w, disInfo.current_h))

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

kleuren = [150,175,200,230,255]
kleurNummer = savefile["zaklampkleur"]
timeCounter = 0
zaklampMode = "normal"
flickerSpeed = 0
while True:
    timeCounter += 1
    clock.tick(10 + flickerSpeed)
    if zaklampMode == "normal":
        display.fill((kleuren[kleurNummer], kleuren[kleurNummer], kleuren[kleurNummer]))
    elif zaklampMode == "flicker":
        if timeCounter % 2 == 0:
            display.fill((kleuren[kleurNummer], kleuren[kleurNummer], kleuren[kleurNummer]))
        else:
            display.fill((0,0,0))
    else:
        display.fill((0,0,0))



    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                savefile["zaklampkleur"] = kleurNummer
                with open(JSONFILEPATH, 'w') as json_file:
                    json.dump(savefile, json_file, indent = 4, separators=(',',': '))
                exit()
            if event.key == pygame.K_SPACE:
                kleurNummer += 1
                if kleurNummer > 4:
                    kleurNummer = 0
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                if zaklampMode == "normal":
                    zaklampMode = "flicker"
                elif zaklampMode == "flicker":
                    zaklampMode = "none"
                else:
                    zaklampMode = "normal"
            if event.key == pygame.K_UP and flickerSpeed < 10:
                flickerSpeed += 2
            if event.key == pygame.K_DOWN and flickerSpeed > 0:
                flickerSpeed -= 2
    
    pygame.display.flip()