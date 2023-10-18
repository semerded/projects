try:
    import pygame
except ImportError:
    raise ImportError("import pygame")
import random, sys

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
                sys.exit()
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
    
class color:
    RED = (255,0,0)
    ORANGE = (255,80,0)
    YELLOW = (255,255,0)
    GREEN = (0,255,0)
    DARKGREEN = (0,150,0)
    TURQUISE = (0,255,255)
    PINK = (255, 0, 100)
    BLUE = (0,0,255)
    LIGHTBLUE = (0, 120, 255)
    PURPLE = (255,0,255)
    WHITE = (255,255,255)
    LESSWHITE = (200,200,200)
    LESSRED = (200, 0, 0)
    LESSGREEN = (0, 200, 0)
    LESSBLUE = (0, 0, 200)
    LIGHTGRAY = LIGHTGREY = (150, 150, 150)
    GRAY = GREY = (100,100,100)
    DARKGRAY = DARKGREY = (50,50,50)
    DARKMODEGRAY = DARKMODEGREY = (30,30,30)
    BLACK = (0,0,0)
    
    def random():
        tuple = []
        for i in range(3):
            tuple.append(random.randint(0, 255))
        return (tuple[0], tuple[1], tuple[2])