try:
    import pygame
except ImportError:
    raise ImportError("import pygame")

pygame.init()
screenInfo = pygame.display.Info()


class app:
    def __init__(self, screenWidth, screenHeight, *flags) -> None:
        self.APPdisplay = pygame.display.set_mode((screenWidth, screenHeight) ,*flags)
    def __center__(self):
        pass
        
    def eventHandeler(self, events, keys):
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    keys()
         
    
    def events(self, **kwargs):
        for tesm, keys in kwargs.items():
            return keys
        
        
                
    @property
    def display(self) -> pygame.surface:
        return self.APPdisplay
    class text:
        def __init_subclass__(cls,
                              ) -> None:
            pass
        
        def place(self):
            pass
        
class test:
    def __init__(self) -> None:
        pass