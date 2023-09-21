import pygame, random, os, pygame_textinput



    
    


class button:
    def __init__(self, width: float, height: float, color: tuple[int,int,int] = (120,120,120), radius: int = -1, borderThickness: int = -1):
        self._width = width
        self._height = height
        self.buttonColor = color
        self._radius = radius
        
        self.radiusTL = -1
        self.radiusTR = -1
        self.radiusBL = -1
        self.radiusBR = -1
        self.borderThickness = 0
        
        self.mouseInButton = False
        self.textAvailable = False
        self.borderAvailable = False
        
    def __repr__(self) -> str:
        return f"{self._width, self._height}"
        
    
    def text(self, font: pygame.font, color: tuple[int,int,int], text: str):
        self.textMessage = text
        self.textFont = font
        self.textColor = color
        self.textAvailable = True
        
    def border(self, borderWidth: int, borderColor: tuple[int,int,int] = (0,0,0), borderRadius: int = -1, borderLeft: int = -1, borderRight: int = -1, borderTop: int = -1, borderBottom: int = -1):
        self.borderThickness = 0
        self.borderWidth = borderWidth
        self.borderColor = borderColor
        self.borerRadius = borderRadius
        self.borderLeft = borderLeft
        self.borderRight = borderRight
        self.borderTop = borderTop
        self.borderBottom = borderBottom
        self.borderAvailable = True
        
    def radius(self, radiusTopLeft: int = -1, radiusTopRight: int = -1, radiusBottomLeft: int = -1, radiusBottomRight: int = -1):
        self.radiusTL = radiusTopLeft
        self.radiusTR = radiusTopRight
        self.radiusBL = radiusBottomLeft
        self.radiusBR = radiusBottomRight
    
    def reposition(self, width: float, height: float, radius: int = -1):
        self._width = width
        self._height = height
        self._radius = radius
    
    def recolor(self, newColor: tuple[int,int,int]):
        self.buttonColor = newColor
        
    def onMouseOver(self, before, after):
        pass
        
    def place(self, display, position: tuple[float, float]):
        buttonRect = pygame.draw.rect(display, self.buttonColor, pygame.Rect(position[0], position[1], self._width, self._height), self.borderThickness , self._radius, self.radiusTL, self.radiusTR, self.radiusBL, self.radiusBR)
        if self.textAvailable:
            printText = self.textFont.render(self.textMessage, True, self.textColor)
            display.blit(printText, (position[0] + self._width / 2 - printText.get_width() / 2, position[1] + self._height / 2 - printText.get_height() / 2))

            
        if self.borderAvailable:
            borderRect = pygame.draw.rect(display, self.borderColor, pygame.Rect(), border_radius=self.borerRadius)
            
        mouse_pos = pygame.mouse.get_pos()
        if buttonRect.collidepoint(mouse_pos):
            self.mouseInButton = True
            return True
        self.mouseInButton = False
        return False
            
    
class color:
    RED = (255,0,0)
    ORANGE = (255,80,0)
    YELLOW = (255,255,0)
    GREEN = (0,255,0)
    TURQUISE = (0,255,255)
    PINK = (255, 0, 100)
    BLUE = (0,0,255)
    LIGHTBLUE = (0, 120, 255)
    PURPLE = (255,0,255)
    WHITE = (255,255,255)
    LESSWHITE = (200,200,200)
    GRAY = GREY = (100,100,100)
    DARKGRAY = DARKGREY = (50,50,50)
    DARKMODEGRAY = DARKMODEGREY = (30,30,30)
    BLACK = (0,0,0)

class font:
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

    
if __name__ == "__main__":
    pygame.init()
    
    display = pygame.display.set_mode((500, 500))
    
    test = button(50, 50)
    
    
    
    while True:
        display.fill(color.GREEN)
        print(test.place(display, (100, 100)))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
    
        pygame.display.update()
    
