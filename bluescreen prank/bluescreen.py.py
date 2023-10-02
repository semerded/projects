import pygame, keyboard
from os import environ
from random import randint
from time import sleep

environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

image = pygame.image.load("bluescreen.png")

clock = pygame.time.Clock()
info = pygame.display.Info()
screenWidth, screenHeight = info.current_w, info.current_h
print(screenWidth, screenHeight)
display = pygame.display.set_mode((screenWidth, screenHeight))
# display = pygame.display.set_mode((300, 300))

counterTextFont = pygame.font.SysFont("Segoe UI", 36)
image = pygame.transform.scale(image, (screenWidth, screenHeight))
counter = uCounter= 0 
keyF = keyU = keyC = keyK = fuck = False
# print(keyboard._canonical_names.canonical_names)
# exit()

while True:
    while True:
        clock.tick(60)
        
        pygame.mouse.set_visible(False)

        
        
        display.fill((0,0,0))
        
        display.blit(image, (0,0))
        
        if randint(0, 200) == 69:
            if counter == 100:
                break
            counter += randint(3, 20)
        if counter > 100:
            counter = 100
        keyboard.block_key("alt")
        keyboard.block_key("tab")
        keyboard.block_key("delete")
        keyboard.block_key("control")
        keyboard.block_key("Win")
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    keyF = True
                if event.key == pygame.K_u:
                    if fuck:
                        uCounter += 1
                    else:
                        keyU = True
                if event.key == pygame.K_c:
                    keyC = True
                if event.key == pygame.K_k:
                    keyK = True
             
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    keyF = False
                if event.key == pygame.K_u:
                    if not fuck:
                        keyU = False
                if event.key == pygame.K_c:
                    keyC = False
                if event.key == pygame.K_k:
                    keyK = False
            if keyF and keyU and keyC and keyK:
                fuck = True
            else:
                fuck = False
                uCounter = 0
            if uCounter >= 10:
                exit()
    # (0, 120, 215)
        
        pygame.draw.rect(image, (0, 120, 215), pygame.Rect(0, screenHeight * 0.565, screenWidth, 40))
        counterText = counterTextFont.render(f"{counter}% complete", False, (255, 255, 255))
        display.blit(counterText, (165, screenHeight * 0.555))  
        
        # 255 627
        
        
        pygame.display.flip()
    while True:
        counter = 0
        display.fill((0,0,0))
        pygame.display.flip()
        sleep(2)
        break