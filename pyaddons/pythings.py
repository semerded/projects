import pygame, random, os, pygame_textinput




    


class button:
    """
    make easy buttons in pygame
    standard buttons come with a gray color, specifiy the width and height
    with ```buttonName.place(pygameDisplay, (Xposition, Yposition))```
    add borders and centerd text to your button to truly customise the button
    
    
    """
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
        self.clickedNotInButton = False
        self.mouseButtonDown = False
        self.mouseButtonUp = True
        self.textAvailable = False
        self.borderAvailable = False
        self.highFlankDetection = False
        self.lowFlankDetection = False
        self.events = None
        self.clickedNotInButton = False
        self.releasedNotInButton = False

        
    def __repr__(self) -> str:
        return f"{self._width, self._height}"
        
    
    def text(self, font: pygame.font, color: tuple[int,int,int], text: str):
        self.textMessage = text
        self.textFont = font
        self.textColor = color
        self.textAvailable = True
        
    def border(self, borderWidth: int, borderColor: tuple[int,int,int] = (0,0,0), borderRadius: int = 0, borderLeft: int = 0, borderRight: int = 0, borderTop: int = 0, borderBottom: int = 0):
        self.borderThickness = 0
        self.borderWidth = borderWidth
        self.borderColor = borderColor
        self.borerRadius = borderRadius
        self.borderLeft = borderLeft
        self.borderRight = borderRight
        self.borderTop = borderTop
        self.borderBottom = borderBottom
        self.borderAvailable = True
        self.buttonClicked = False
        
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
        
    def __checkButtonStatus__(self):
        if self.events != None:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseButtonUp = False
                    self.highFlankDetection = True
                    self.mouseButtonDown = True
                    if self.mouseInButton == False:
                        self.clickedNotInButton = True
                    else:
                        self.clickedNotInButton = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouseButtonDown = False
                    self.lowFlankDetection = True
                    self.mouseButtonUp = True
                    if self.mouseInButton == False:
                        self.releasedNotInButton = True
                    else:
                        self.releasedNotInButton = False
                    
        else:
            raise SyntaxError("place the '.place' methode before any '.on~' methods")
        
    def onMouseOver(self, action):
        if self.mouseInButton:
            action()
            
    
    def onHold(self, action = None, holdAfterMouseLeave: bool = False):
        if self.mouseInButton and self.mouseButtonDown and self.clickedNotInButton == False:
            self.buttonClicked = True
            if action != None:
                action()
        else:
            self.buttonClicked = False
        if holdAfterMouseLeave:
            if self.mouseButtonDown and self.clickedNotInButton == False:
                self.buttonClicked = True
            else:
                self.buttonClicked = False
        if self.mouseButtonUp:
            self.buttonClicked = False
            
                
        return self.buttonClicked
            
    
    def onClick(self, action,  actionOnRelease: bool = False): # TODO
        if self.mouseButtonDown and not actionOnRelease: 
            if self.mouseInButton and self.highFlankDetection and self.clickedNotInButton == False:
                action(True)
                self.highFlankDetection = False

        if self.mouseButtonUp and actionOnRelease and self.clickedNotInButton == False:
            if self.mouseInButton and self.lowFlankDetection and self.releasedNotInButton == False:
                action(False)
                self.lowFlankDetection = False
        
        
        
        # for event in events:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if self.mouseInButton == False:
        #             self.mouseButtonDown = True
        #             self.clickedNotInButton = True
        #         else:
        #             self.mouseButtonDown = True
        #             self.clickedNotInButton = False
        #     if event.type == pygame.MOUSEBUTTONUP:
        #         self.clickedNotInButton = False
        #         self.mouseButtonDown = False
                
        # if self.mouseInButton and self.mouseButtonDown and not self.clickedNotInButton and not actionOnRelease:
        #     self.buttonClicked = True
        #     action()
            
        # if self.mouseButtonDown == False or self.mouseInButton == False:
        #     self.buttonClicked = False
        
        # if self.mouseButtonDown and self.mouseInButton == False:
        #     self.clickedNotInButton = True
            
        # return self.buttonClicked
        
    def place(self, display, events, position: tuple[float, float]):
        self.events = events
        self.__checkButtonStatus__()

        # print the border if the user provides a border
        if self.borderAvailable:
            if self.borderWidth <= 0:
                BShift = self.borderWidth / 2
                pygame.draw.rect(display, self.borderColor, pygame.Rect(position[0] - BShift, position[1] - BShift, self._width + self.borderWidth, self._height + self.borderWidth), border_radius=self.borerRadius)

            elif self.borderBottom <= 0 or self.borderTop <= 0 or self.borderLeft <= 0 or self.borderRight <= 0:
                pygame.draw.rect(display, self.borderColor, pygame.Rect(position[0] - self.borderLeft, position[1] - self.borderTop , self._width + self.borderLeft + self.borderRight, self._height + self.borderTop + self.borderBottom), border_radius=self.borerRadius)
           
        # print button
        buttonRect = pygame.draw.rect(display, self.buttonColor, pygame.Rect(position[0], position[1], self._width, self._height), self.borderThickness , self._radius, self.radiusTL, self.radiusTR, self.radiusBL, self.radiusBR)
        
        # print text in the middle of the button if the user provides text
        if self.textAvailable:
            printText = self.textFont.render(self.textMessage, True, self.textColor)
            display.blit(printText, (position[0] + self._width / 2 - printText.get_width() / 2, position[1] + self._height / 2 - printText.get_height() / 2))
    
         
        mouse_pos = pygame.mouse.get_pos()
        if buttonRect.collidepoint(mouse_pos):
            self.mouseInButton = True
            return True
        self.mouseInButton = False
        return False
    
class text():
    def __init__(self, inputText: str):
        self.inputText = inputText
        
    
            
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
    
    test = button(100, 50, color.WHITE, 10)
    test.text(font.H3, color.RED, "button")
    test.border(10, borderRadius=10)
    def hello(test):
        print(test)
    
    while True:
        display.fill(color.GREEN)
        events = pygame.event.get()
        test.place(display, events, (100, 100))
        
        test.onClick(hello, True)
        # print(test.onHold(holdAfterMouseLeave=True))
        
        
        for event in events:
            if event.type == pygame.QUIT:
                exit()
    
        pygame.display.update()
    
