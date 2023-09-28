from typing import overload
import pygame, random, os, pygame_textinput





    


class button:
    """
    make easy buttons in pygame\n
    standard buttons come with a gray color, specifiy the width and height
    with ```buttonName.place(pygameDisplay, pygame.eventhandeler, (Xposition, Yposition))```\n
    add borders and centerd text to your button to truly customise the button\n\n
    >>> buttonExample = button(100, 50, (255, 255, 255)) # width, height, color, optional radius, optional border thickness
    >>> buttonExample.place(display, events, (100, 200)) # pygame display, pygame eventhandeler, x and y position
    >>> buttonExample.border(10, (0, 0, 0)) # width of border, border color, optional border radius (customizable per corner)
    >>> buttonExample.onClick(function) # important that the function doesn't containt its brackets, optional action activated after mousebutton is released
    >>> isButtonActive = buttonExample.onHold() # optional action when active (same note as .onClick), optional 
    >>> buttonExample.text(mediumFont, (255, 0, 0), "this is a button") # pygame font, text color, text
    
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
    
    def resize(self, width: float, height: float, radius: int = -1):
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
    
    def onMouseOver(self):
        if self.mouseInButton:
            return True
        return False
    
    def changeColorOnHover(self, oldColor: tuple[int,int,int], newColor: tuple[int,int,int], changeTextColor: bool = False, transition: int = 0):
        """
        makes the button color `newColor` if mouse is in the button and makes the button color `oldColor` when not in mouse button
        """
        if self.onMouseOver():
            if changeTextColor:
                self.textColor = newColor
            else:
                self.buttonColor = newColor
        else:
            if changeTextColor:
                self.textColor = oldColor
            else:
                self.buttonColor = oldColor
            
    
    def onHold(self, function = None, *arguments, holdAfterMouseLeave: bool = False): # TODO fix 
        if self.mouseInButton and self.mouseButtonDown and self.clickedNotInButton == False:
            self.buttonClicked = True
            if function != None:
                function(*arguments)
        else:
            self.buttonClicked = False
        if holdAfterMouseLeave:
            if self.mouseButtonDown and self.clickedNotInButton == False:
                self.buttonClicked = True
            else:
                self.buttonClicked = False
        if self.mouseButtonUp:
            self.buttonClicked = False
        
        if self.mouseButtonDown and self.mouseInButton == False:
            self.clickedNotInButton = True
        
                    
        return self.buttonClicked
        
    
    def onClick(self, function = None, *argumets,  actionOnRelease: bool = False): # TODO
        """
        use this to only activate when you clicked the button
        
        
        
        
        \nexample 1:
            >>> if buttonExample.onClick() == True:
            >>>     print("hello world!")
            === when clicked prints: "hello world!"
        
        \nexample 2:
            >>> def myCalculator(number1, number2):
            >>>     return number1 + number2
            >>> calculation = buttonExample.onClick(myCalculator, 5, 7)
            >>> print(calculation)
            === when clicked prints: 12
            
        \nexample 3:
            >>> def hello():
            >>>     print("hello world!")
            >>> buttonExample.onClick(hello, actionOnRelease=True)
            === when released prints: "hello world!
        """
            
        if self.mouseButtonDown and not actionOnRelease: 
            if self.mouseInButton and self.highFlankDetection and self.clickedNotInButton == False:
                returnValue = function(*argumets)
                self.highFlankDetection = False
                return returnValue if returnValue != None else True


        if self.mouseButtonUp and actionOnRelease and self.clickedNotInButton == False:
            if self.mouseInButton and self.lowFlankDetection and self.releasedNotInButton == False:
                returnValue = function(*argumets)
                self.lowFlankDetection = False
                return returnValue if returnValue != None else True
        return False
    
        
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
    
class text:
    def __init__(self, inputText: str):
        self.inputText = inputText
        
    def placeText(self, position: tuple[float, float]):
        pass
    
    class textbox:
        def __init__(self, width) -> None:
            pass
 
 
"""
built in shortcuts

this library comes with some presets to make some developing easier
"""       
class Xbutton:
    def __init__(self, display, actionOnClick = exit, defaultColor: tuple[int,int,int] = (120, 120, 120), size: float = 30, position: tuple[int,int] = (0,0), radius: int = 5, actionOnRelease: bool = False) -> None:
        self._quitButton = button(size, size, defaultColor, radius)
        self.display = display
        self.defaultColor = defaultColor
        self.size = size
        self.xcord = position[0]
        self.ycord = position[1]
        self.actionOnClick = actionOnClick
        self.actionOnRelease = actionOnRelease
    def __getCrossColor__(self):
        colorTotal = 0
        for color in self.defaultColor:
            colorTotal += color
        crossColor = (0,0,0) if colorTotal > 380 else (255, 255, 255)
        return crossColor
    
    
    def place(self, events, screenwidth: float):
        
        self.xcord = screenwidth - self.size
        crossColor = self.__getCrossColor__()
        self._quitButton.text(pygame.font.SysFont(pygame.font.get_default_font(), 40), crossColor, "x")
        self._quitButton.place(self.display, events, (self.xcord, self.ycord))
        self._quitButton.recolor = (255, 0, 0) if self._quitButton.onMouseOver() else (0,0,0)
        self._quitButton.changeColorOnHover(self.defaultColor, (255, 0, 0))
        if crossColor == (0,0,0):
            self._quitButton.changeColorOnHover((0,0,0), (255,255,255),True)
            print(True)
        
        self._quitButton.onClick(self.actionOnClick, actionOnRelease=self.actionOnRelease)
        
    def repostion(self, xcord, ycord):
        self.xcord = xcord
        self.ycord = ycord
        
class menuKeys:
    def __init__(self, display, menuColor: tuple[int,int,int] = (120, 120, 120), size: float = 30) -> None:
        self.exitButton = Xbutton(display, exit, menuColor, size, radius=0, actionOnRelease=True)
        self.textColor = self.exitButton.__getCrossColor__()
        self.maximizeButton = button(size, size, menuColor, 0)
        self.maximizeButton.text(pygame.font.SysFont(pygame.font.get_default_font(), 40), self.textColor, "+")
        self.minimizeButton = button(size, size, menuColor, 0)
        self.minimizeButton.text(pygame.font.SysFont(pygame.font.get_default_font(), 40), self.textColor, "~")
        
        self.display = display
        self.menuColor = menuColor
        self.size = size
        
    def menuPlace(self, events, screenwidth: float, screenheight: float):
        self.exitButton.place(events, screenwidth)
        
        self.minimizeButton.place(self.display, events, (screenwidth - self.size * 3, 0))
        self.minimizeButton.changeColorOnHover(self.menuColor, (0,255,0))
        self.minimizeButton.onClick(pygame.display.iconify, actionOnRelease=True)
        
        self.maximizeButton.place(self.display, events, (screenwidth - self.size * 2, 0))
        self.maximizeButton.changeColorOnHover(self.menuColor, (255, 255, 0))
        if self.maximizeButton.onClick():
            displayScreenW, displayScreenH = windowInfo()
            if screenwidth == displayScreenW and screenheight == displayScreenH:
                self.oldScreenSize = [screenwidth, screenheight]
                windowSize(displayScreenW, displayScreenH)
            else:
                windowSize(self.oldScreenSize[0], self.oldScreenSize[1])
            
        
def windowInfo():
    info = pygame.display.Info()
    screenWidth, screenHeight = info.current_w, info.current_h
    return screenWidth, screenHeight
        
def windowSize(width, heigth, resizable: bool = False):
    display = pygame.display.set_mode((width, heigth))
    return display
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
    clock = pygame.time.Clock()
    test = button(100, 50, color.WHITE, 10)
    test.text(font.H3, color.RED, "button")
    test.border(10, borderRadius=10)
    
    def func():
        print("hello")
    # quitbutton = Xbutton(display, func, color.WHITE)
    menukeys = menuKeys(display)
   
    
    while True:
        clock.tick(30)
        display.fill(color.GREEN)
        events = pygame.event.get()
        test.place(display, events, (100, 100))
        
        # print(test.onClick(func))
        # test.onHold()
        test.changeColorOnHover(color.WHITE, color.BLUE)
        # test.recolor(color.BLUE) if test.onMouseOver() else test.recolor(color.WHITE)
        # quitbutton.place(events, 500)
        menukeys.menuPlace(events, 500, 500)
        
        
        
        for event in events:
            if event.type == pygame.QUIT:
                exit()
    
        pygame.display.update()
    
