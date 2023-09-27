import pygame
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
counterTextFont = pygame.font.SysFont(pygame.font.get_default_font(), 40)
image = pygame.transform.scale(image, (screenWidth, screenHeight))
counter = 0  
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
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
    # (0, 120, 215)
        
        print(pygame.draw.rect(image, (255, 0, 0), pygame.Rect(0, screenHeight * 0.565, screenWidth, 40)))
        counterText = counterTextFont.render(f"{counter}% complete", False, (255, 255, 255))
        display.blit(counterText, (205, screenHeight * 0.565 + 5))  
        
        # 255 627
        
        
        pygame.display.flip()
    while True:
        counter = 0
        display.fill((0,0,0))
        pygame.display.flip()
        sleep(2)
        break