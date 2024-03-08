def run():
    import gFrame, pygame
    
    app = gFrame.AppConstructor("100dw", "100dh")
    currentMode = 0
    flickerSpeed = 0
    while True:
        app.eventHandler(10 + flickerSpeed)
        
        if currentMode == 0: # normal
            app.fill(gFrame.Color.WHITE)
        elif currentMode == 1: # flicker
            if app.appFrameCounter % 2 == 0:
                app.fill(gFrame.Color.WHITE)
            else:
                app.fill(gFrame.Color.BLACK)
        else:
            app.fill(gFrame.Color.BLACK)
        
        if gFrame.Interactions.isKeyClicked(pygame.K_ESCAPE):
            pygame.quit()
            return

        if gFrame.Interactions.isKeyClicked(pygame.K_SPACE):
            currentMode += 1
            if currentMode > 2:
                currentMode = 0
                
        if gFrame.Interactions.isKeyClicked(pygame.K_UP):
            flickerSpeed += 2
            if flickerSpeed > 10:
                flickerSpeed = 10
        
        if gFrame.Interactions.isKeyClicked(pygame.K_DOWN):
            flickerSpeed -= 2
            if flickerSpeed < 0:
                flickerSpeed = 0
                