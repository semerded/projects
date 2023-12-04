try:
    import pygame
except ImportError:
    raise ImportError("import pygame")
import random, sys
from typing_extensions import TypeAlias, Literal

pygame.init()
pygame.font.init()

screenUnit: TypeAlias = int | str
modifiableFunctions: TypeAlias = Literal[
    "quit"
]

colorValue = tuple[int,int,int]
screenInfo = pygame.display.Info()
userScreenWidth = screenInfo.current_w
userScreenHeight = screenInfo.current_h

class Color:
    #TODO add argb
    RED = (255,0,0)
    LAVARED = (255,40,0)
    ORANGE = (255,80,0)
    YELLOW = (255,255,0)
    GREEN = (0,255,0)
    OLIVEGREEN = (0,150,0)
    DARKGREEN = (0,100,0)
    TURQUISE = (0,255,255)
    PINK = (255,0,100)
    BLUE = (0,0,255)
    LIGHTBLUE = (0,120,255)
    PURPLE = (255,0,255)
    WHITE = (255,255,255)
    LESSWHITE = (200,200,200)
    LESSRED = (200,0,0)
    LESSYELLOW = (200,200,0)
    LESSGREEN = (0,200,0)
    LESSTURQUISE = (0,200,200)
    LESSBLUE = (0,0,200)
    LIGHTGRAY = LIGHTGREY = (150,150,150)
    GRAY = GREY = (100,100,100)
    DARKGRAY = DARKGREY = (50,50,50)
    DARKMODEGRAY = DARKMODEGREY = (30,30,30)
    BLACK = (0,0,0)
    
    def random():
        tuple = []
        for i in range(3):
            tuple.append(random.randint(0, 255))
        return (tuple[0], tuple[1], tuple[2])
    
class Font:
    H1 = pygame.font.SysFont(pygame.font.get_default_font(), 34)
    H2 = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    H3 = pygame.font.SysFont(pygame.font.get_default_font(), 24)
    H4 = pygame.font.SysFont(pygame.font.get_default_font(), 20)
    H5 = pygame.font.SysFont(pygame.font.get_default_font(), 18)
    H6 = pygame.font.SysFont(pygame.font.get_default_font(), 16)
    XXSMALL = pygame.font.SysFont(pygame.font.get_default_font(), 8)
    XSMALL = pygame.font.SysFont(pygame.font.get_default_font(), 12)
    SMALL = pygame.font.SysFont(pygame.font.get_default_font(), 14)
    MEDIUM = pygame.font.SysFont(pygame.font.get_default_font(), 28)
    LARGE = pygame.font.SysFont(pygame.font.get_default_font(), 38)
    XLARGE = pygame.font.SysFont(pygame.font.get_default_font(), 46)
    XXLARGE = pygame.font.SysFont(pygame.font.get_default_font(), 60)
    XXXLARGE = pygame.font.SysFont(pygame.font.get_default_font(), 72)
    FONT50 = pygame.font.SysFont(pygame.font.get_default_font(), 50)
    FONT100 = pygame.font.SysFont(pygame.font.get_default_font(), 100)
    FONT150 = pygame.font.SysFont(pygame.font.get_default_font(), 150)
    
    def customFont(size, font = None):
        if font == None:
            return pygame.font.SysFont(pygame.font.get_default_font(), size)
        else:
            return pygame.font.SysFont(font, size)
        

class AppConstructor():
    def __init__(self, screenWidth, screenHeight, *flags) -> None:
        self.screenWidth = screenInfo.current_w
        self.screenHeight = screenInfo.current_h
        self.APPdisplayFlags = flags
        
        self.minimumScreenWidth = None
        self.minimumScreenHeight = None
        self.modifiedFunctions = {"quit": None}
        
        self.APPdisplay = pygame.display.set_mode((screenWidth, screenHeight) ,*flags)
        
        
    def eventHandler(self, appEvents:pygame.event):
        self.appEvents = appEvents
        for event in self.appEvents:
            if event.type == pygame.QUIT:
                if self.modifiedFunctions["quit"] == None:
                    pygame.quit()
                    sys.exit()
                else:
                    self.modifiedFunctions["quit"]()
                    
            if event.type == pygame.WINDOWRESIZED:
                self._checkForMinimumScreenSizeBreaches()
    
    def resizeAppscreen(self, screenWidth, screenHeight, *flags):
        self.APPdisplayFlags = flags
        self.APPdisplay = pygame.display.set_mode((screenWidth, screenHeight), *flags)    
    
    
    def setModifiableFunctions(self, **kwargs:modifiableFunctions): # TODO
        for modifiedFunction, newFunction in kwargs.items():
            self.modifiedFunctions[modifiedFunction] = newFunction
            
    def setMinimumScreenDimensions(self, minimumScreenWidth:screenUnit = None, minimumScreenHeight:screenUnit = None):
        if minimumScreenWidth != None:
            self.minimumScreenWidth = minimumScreenWidth
        else:
            self.minimumScreenWidth = None
        if minimumScreenHeight != None:
            self.minimumScreenHeight = minimumScreenHeight
        else:
            self.minimumScreenHeight = None
    
    def _checkForMinimumScreenSizeBreaches(self):
        w, h = self.getAppScreenDimensions
        updateScreen = False
        if w < self.minimumScreenWidth:
            w = self.minimumScreenWidth
            updateScreen = True
        if h < self.minimumScreenHeight:
            h = self.minimumScreenHeight
            updateScreen = True
        if updateScreen:
            self.resizeAppscreen(w, h, *self.APPdisplayFlags)
        
        
        
     
    @property
    def setRelativeFullscreen(self):
        self.APPdisplay = pygame.display.set_mode((self.screenWidth, self.screenHeight), *self.APPdisplayFlags)
        self.setModifiableFunctions()
        
    @property
    def getAppScreenDimensions(self):
        displayInfo = pygame.display.Info()
        return displayInfo.current_w, displayInfo.current_h
    
    @property
    def getdisplayDimensions(self):
        return (self.screenWidth, self.screenHeight)

    @property
    def maindisplay(self) -> pygame.surface:
        """pygame main surface"""
        return self.APPdisplay            
    
    
  
class Image:
    def resizeImage(image, size: tuple[int,int]):
        aspectRatio = Image.getAspectRatio(image)
        imageWidth = size[0]
        imageHeight = size[1]
        if aspectRatio < 1:
            imageWidth = int(imageWidth * aspectRatio)
        else:
            imageHeight = int(imageHeight/ aspectRatio)
            
        

    def getAspectRatio(image):
        #TODO get size
        imageWidth, imageHeight = image # getsize
        aspectRatio = imageWidth / imageHeight
        
              
  
class Scroll():
    def __init__(self) -> None:
        pass
    
    @property
    def set_scroll(self):
        self.__scrollActivated = True
        
    @property
    def get_scroll(self):
        return self.__scrollActivated


class ScreenUnit:
    def convert():
        ...
        
    def precent(parentSize, percent):
        return parentSize / 100 * percent
    
    def vw(screenUnit:float) -> float:
        return userScreenWidth / 100 * screenUnit
    
    def vh(screenUint:float) -> float:
        return userScreenHeight / 100 * screenUnit
        

        
        
        
    

class Text:

        pass
        
        def place(self):
            pass


    
class Button:
    def __init__(self,
                 size: tuple[screenUnit,screenUnit],
                 textColor: tuple[int,int,int] = Color.BLACK,
                 bgColor: colorValue = Color.LESSWHITE,
                 borderTickness: int = 2,
                 borderColor: colorValue = Color.BLACK,
                 borderRadius: int = 0,
                 onClick = ...,
                 onHold = ...,
                 onHover = ...,
                 colorOnHover: colorValue = ...,
                 
                 
                 ) -> None:
        print(onClick)

    def __text(self):
        ...
        
    def __border(self):
        ...
    
    def __radius(self):
        ...
        
    def __resize__(self):
        ...
    
    def __recolor__(self):
        ...
        
    def onMouseOver(self):
        ...
        
    def onMouseClick(self):
        ...
        
    def onMouseHold(self):
        ...
    
    def changeColorOnHover(self):
        ...
        
    def place(self):
        ...
        
    
        
    
class text:
    def __init__(self) -> None:
        pass
    
    def centerd(self):
        ...
        
    

class textbox:
    def __init__(self) -> None:
        pass
    
 
    
