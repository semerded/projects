import random, os
try:
    import pygame
except ModuleNotFoundError:
    raise ModuleNotFoundError("install pygame with 'pip install pygame'")
try:
    import pygame_textinput
except ModuleNotFoundError:
    raise ModuleNotFoundError("install pygame_textinput with 'pip install pygame_textinput'")




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
        self.__width = width
        self.__height = height
        self.__buttonColor = color
        self.__radius = radius
        
        self.__radiusTL = -1
        self.__radiusTR = -1
        self.__radiusBL = -1
        self.__radiusBR = -1
        self.__borderThickness = 0
        
        self.__mouseInButton = False
        self.__clickedNotInButton = False
        self.__mouseButtonDown = False
        self.__mouseButtonUp = True
        self.__textAvailable = False
        self.__borderAvailable = False
        self.__highFlankDetection = False
        self.__lowFlankDetection = False
        self.__events = None
        self.__clickedNotInButton = False
        self.__releasedNotInButton = False

        
    def __repr__(self) -> str:
        return f"{self.__width, self.__height}"
        
    
    def text(self, font: pygame.font, color: tuple[int,int,int], text: str):
        self.__textMessage = text
        self.__textFont = font
        self.__textColor = color
        self.__textAvailable = True
        
    def border(self, borderWidth: int, borderColor: tuple[int,int,int] = (0,0,0), borderRadius: int = 0, borderLeft: int = 0, borderRight: int = 0, borderTop: int = 0, borderBottom: int = 0):
        self.__borderThickness = 0
        self.__borderWidth = borderWidth
        self.__borderColor = borderColor
        self.__borerRadius = borderRadius
        self.__borderLeft = borderLeft
        self.__borderRight = borderRight
        self.__borderTop = borderTop
        self.__borderBottom = borderBottom
        self.__borderAvailable = True
        self.__buttonClicked = False
        
    def radius(self, radiusTopLeft: int = -1, radiusTopRight: int = -1, radiusBottomLeft: int = -1, radiusBottomRight: int = -1):
        self.__radiusTL = radiusTopLeft
        self.__radiusTR = radiusTopRight
        self.__radiusBL = radiusBottomLeft
        self.__radiusBR = radiusBottomRight
    
    def resize(self, width: float, height: float, radius: int = -1):
        self.__width = width
        self.__height = height
        self.__radius = radius
    
    def recolor(self, newColor: tuple[int,int,int]):
        self.__buttonColor = newColor
        
    def __checkButtonStatus__(self):
        if self.__events != None:
            for event in self.__events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__mouseButtonUp = False
                    self.__highFlankDetection = True
                    self.__mouseButtonDown = True
                    if self.__mouseInButton == False:
                        self.__clickedNotInButton = True
                    else:
                        self.__clickedNotInButton = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.__mouseButtonDown = False
                    self.__lowFlankDetection = True
                    self.__mouseButtonUp = True
                    if self.__mouseInButton == False:
                        self.__releasedNotInButton = True
                    else:
                        self.__releasedNotInButton = False
                    
        else:
            raise SyntaxError("place the '.place' methode before any '.on~' methods")
    
    def onMouseOver(self):
        if self.__mouseInButton:
            return True
        return False
    
    def changeColorOnHover(self, oldColor: tuple[int,int,int], newColor: tuple[int,int,int], changeTextColor: bool = False, transition: int = 0):
        """
        makes the button color `newColor` if mouse is in the button and makes the button color `oldColor` when not in mouse button
        """
        if self.onMouseOver():
            if changeTextColor:
                self.__textColor = newColor
            else:
                self.__buttonColor = newColor
            return True
        elif changeTextColor:
            self.__textColor = oldColor
        else:
            self.__buttonColor = oldColor
        return False
            
    
    def onHold(self, function = None, *arguments, holdAfterMouseLeave: bool = False): # TODO fix 
        if self.__mouseInButton and self.__mouseButtonDown and self.__clickedNotInButton == False:
            self.__buttonClicked = True
            if function != None:
                function(*arguments)
        else:
            self.__buttonClicked = False
        if holdAfterMouseLeave:
            if self.__mouseButtonDown and self.__clickedNotInButton == False:
                self.__buttonClicked = True
            else:
                self.__buttonClicked = False
        if self.__mouseButtonUp:
            self.__buttonClicked = False
        
        if self.__mouseButtonDown and self.__mouseInButton == False:
            self.__clickedNotInButton = True
        
                    
        return self.__buttonClicked
        
    
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
            
        if self.__mouseButtonDown and not actionOnRelease: 
            if self.__mouseInButton and self.__highFlankDetection and self.__clickedNotInButton == False:
                if function != None:
                    returnValue = function(*argumets)
                else: returnValue = None
                self.__highFlankDetection = False
                return returnValue if returnValue != None else True


        if self.__mouseButtonUp and actionOnRelease and self.__clickedNotInButton == False:
            if self.__mouseInButton and self.__lowFlankDetection and self.__releasedNotInButton == False:
                if function != None:
                    returnValue = function(*argumets)
                else: returnValue = None

                self.__lowFlankDetection = False
                return returnValue if returnValue != None else True
        return False
    
        
    def place(self, display, events, position: tuple[float, float]):
        self.__events = events
        self.__checkButtonStatus__()

        # print the border if the user provides a border
        if self.__borderAvailable:
            if self.__borderWidth <= 0:
                BShift = self.__borderWidth / 2
                pygame.draw.rect(display, self.__borderColor, pygame.Rect(position[0] - BShift, position[1] - BShift, self.__width + self.__borderWidth, self.__height + self.__borderWidth), border_radius=self.__borerRadius)

            elif self.__borderBottom <= 0 or self.__borderTop <= 0 or self.__borderLeft <= 0 or self.__borderRight <= 0:
                pygame.draw.rect(display, self.__borderColor, pygame.Rect(position[0] - self.__borderLeft, position[1] - self.__borderTop , self.__width + self.__borderLeft + self.__borderRight, self.__height + self.__borderTop + self.__borderBottom), border_radius=self.__borerRadius)
           
        # print button
        buttonRect = pygame.draw.rect(display, self.__buttonColor, pygame.Rect(position[0], position[1], self.__width, self.__height), self.__borderThickness , self.__radius, self.__radiusTL, self.__radiusTR, self.__radiusBL, self.__radiusBR)
        
        # print text in the middle of the button if the user provides text
        if self.__textAvailable:
            printText = self.__textFont.render(self.__textMessage, True, self.__textColor)
            display.blit(printText, (position[0] + self.__width / 2 - printText.get_width() / 2, position[1] + self.__height / 2 - printText.get_height() / 2))
    
         
        mouse_pos = pygame.mouse.get_pos()
        if buttonRect.collidepoint(mouse_pos):
            self.__mouseInButton = True
            return True
        self.__mouseInButton = False
        return False
    
class text:
    def __init__(self, display, font, position: tuple[float,float]) -> None:
        self.__display = display
        self.__font = font
        self.__position = position
        
        self.__border = False
        self.__background = False
        self.__xcenter = False
        self.__ycenter = False
        self.__padding = 0



    def centerd(self, xmin: float, xmax: float, ymin: float, ymax: float):
        """
        position[min width, max width, min height, max height]
        """
        self.__position = [(xmin + xmax) / 2, (ymin + ymax) / 2]
        self.__xcenter = True
        self.__ycenter = True
        
    def centerdWidth(self, xmin: float, xmax: float, ycord: float):
        self.__position = [(xmin + xmax) / 2, ycord]
        self.__xcenter = True

    
    def centerdHeight(self, xcord: float, ymin: float, ymax: float):
        self.__position = [xcord, (ymin + ymax) / 2]
        self.__ycenter = True
    
    def reposition(self, xcord: float, ycord: float):
        self.__position = [xcord, ycord]
        
    def border(self, color: tuple[int,int,int], borderWidth: int, borderRadius: int = -1):
        self.__surface = self.__textsurface.get_rect()
        self.__borderWidth = borderWidth
        self.__borderRadius = borderRadius
        self.__borderColor = color
        self.__border = True

        
    def background(self, color: tuple[int,int,int], padding = 0, radius: int = -1):
        self.__surface = self.__textsurface.get_rect()
        self.__backgroundRadius = radius
        self.__backgroundColor = color
        self.__padding = padding
        
        self.__background = True
        
    def place(self, color:tuple[int,int,int], text: str):
        self.__textsurface = self.__font.render(f"{text}", True, color) 
        
        # padding
        if self.__padding > 0:
            padding = self.__padding / 2
        else:
            padding = 0
        if self.__background:
            pygame.draw.rect(self.__display, self.__backgroundColor, pygame.Rect(self.__position[0] - padding, self.__position[1] - padding, self.__surface[2] + self.__padding, self.__surface[3] + self.__padding), border_radius=self.__backgroundRadius)

        if self.__border:
            pygame.draw.rect(self.__display, self.__borderColor, pygame.Rect(self.__position[0] - self.__borderWidth / 2 - padding, self.__position[1] - self.__borderWidth / 2 - padding, self.__surface[2] + self.__borderWidth + self.__padding, self.__surface[3] + self.__borderWidth + self.__padding), self.__borderWidth, self.__borderRadius)
        
        # place text
        if self.__xcenter:  
            self.__position[0] -= self.__textsurface.get_width() / 2
            
        if self.__ycenter:
            self.__position[1] -= self.__textsurface.get_height() / 2      
        
        self.__textRect = self.__display.blit(self.__textsurface, (self.__position[0], self.__position[1]))
        return self.__textRect
    
    def onHover(self):
        mousePos = pygame.mouse.get_pos()
        if self.__textRect.collidepoint(mousePos):
            return True
        return False
    
    @property
    def rect(self):
        return self.__textRect
    
    @property
    def surface(self):
        return self.__textsurface
        
class textbox:
    def __init__(self, display, font, position: tuple[int,int]) -> None:
        self.__calculatedWidth = -1
        self.__textBoxList = []
        self.__position = position
        self.__font = font
        self.__text = text(display, font, position)
        self.__activeText = None
        
    def __calcbox__(self, width, text: str):
        self.__textBoxList = []
        self.__activeText = text
        text = text.split(" ")
        line = ""

        for word in text:
            self.__surface = self.__font.render(f"{line} {word}", True, (0,0,0))
            surface = self.__surface.get_rect()
            if surface[2] < width:
                line += word + " "
            else:
                self.__textBoxList.append(line[:-1])
                line = word + " "
        self.__textBoxList.append(line[:-1]) 
        self.__textHeight = surface[3]
        self.__boxHeight = surface[3] * len(self.__textBoxList)
        
        self.__calculatedWidth = width
    
    def reposition(self, xcord, ycord):
        self.__position= (xcord, ycord)
    
    def place(self, width, color: tuple[int,int,int], text: str, centerd: bool = False):
        if self.__calculatedWidth != width or self.__activeText != text:
            self.__calcbox__(width, text)
        self.__width = width
       
        linecounter = 0
        for line in self.__textBoxList:
            if centerd:
                self.__text.centerdWidth(self.__position[0], self.__position[0] + width, self.__position[1] + (linecounter * self.__textHeight))
            else:
                self.__text.reposition(self.__position[0], self.__position[1] + (linecounter * self.__textHeight))
            self.__text.place(color, line)

            linecounter += 1
            
    def onHover(self):
        self.__boxRect = pygame.Rect(self.__position[0], self.__position[1], self.__width, self.boxheight)
        mousePos = pygame.mouse.get_pos()
        if self.__boxRect.collidepoint(mousePos):
            return True
        return False
    
    @property
    def boxheight(self):
        return self.__boxHeight
    
    
    
    
        
        
 
"""
built in shortcuts

this library comes with some presets to make some developing easier
"""       
class Xbutton:
    def __init__(self, display, actionOnClick = exit, defaultColor: tuple[int,int,int] = (120, 120, 120), size: float = 30, position: tuple[int,int] = (0,0), radius: int = 5, actionOnRelease: bool = True) -> None:
        self.__quitButton = button(size, size, defaultColor, radius)
        self.__display = display
        self.__defaultColor = defaultColor
        self.__size = size
        self.__xcord = position[0]
        if self.__xcord != 0:
            self.__repostioned = True
        else:
            self.__repostioned = False


        self.__ycord = position[1]
        self.__actionOnClick = actionOnClick
        self.__actionOnRelease = actionOnRelease

    def __getCrossColor__(self):
        colorTotal = 0
        for color in self.__defaultColor:
            colorTotal += color
        crossColor = (0,0,0) if colorTotal > 380 else (255, 255, 255)
        return crossColor
    
    
    def place(self, events, screenwidth: float):
        if self.__repostioned == False:
            self.__xcord = screenwidth - self.__size
        crossColor = self.__getCrossColor__()
        self.__quitButton.text(pygame.font.SysFont(pygame.font.get_default_font(), self.__size + 10), crossColor, "x")
        self.__quitButton.place(self.__display, events, (self.__xcord, self.__ycord))
        self.__quitButton.recolor = (255, 0, 0) if self.__quitButton.onMouseOver() else (0,0,0)
        self.__quitButton.changeColorOnHover(self.__defaultColor, (255, 0, 0))
        if crossColor == (0,0,0):
            self.__quitButton.changeColorOnHover((0,0,0), (255,255,255),True)
        
        self.__quitButton.onClick(self.__actionOnClick, actionOnRelease=self.__actionOnRelease)
        
    def repostion(self, xcord, ycord):
        self.__xcord = xcord
        self.__ycord = ycord
        self.__repostioned = True

"""in progress"""
class menuKeys:
    def __init__(self, display, screenDimensions: tuple[int,int], menuColor: tuple[int,int,int] = (120, 120, 120), size: float = 30) -> None:
        self.__exitButton = Xbutton(display, exit, menuColor, size, radius=0, actionOnRelease=True)
        self.__textColor = self.__exitButton.__getCrossColor__()
        self.__maximizeButton = button(size, size, menuColor, 0)
        self.__maximizeButton.text(pygame.font.SysFont(pygame.font.get_default_font(), 40), self.__textColor, "+")
        self.__minimizeButton = button(size, size, menuColor, 0)
        self.__minimizeButton.text(pygame.font.SysFont(pygame.font.get_default_font(), 40), self.__textColor, "~")
        
        self.__mouseButtonDown = False
        self.__display = display
        self.__menuColor = menuColor
        self.__size = size
        self.__displayInfo = [screenDimensions[0], screenDimensions[1]]
        self.__oldmousePos = (0,0)
        
    def menuPlace(self, events, screenwidth: float, screenheight: float):
        self.__exitButton.place(events, screenwidth)
        
        self.__minimizeButton.place(self.__display, events, (screenwidth - self.__size * 3, 0))
        self.__minimizeButton.changeColorOnHover(self.__menuColor, (0,255,0))
        self.__minimizeButton.onClick(pygame.display.iconify, actionOnRelease=True)
        
        self.__maximizeButton.place(self.__display, events, (screenwidth - self.__size * 2, 0))
        self.__maximizeButton.changeColorOnHover(self.__menuColor, (255, 255, 0))
        self.__resize__(events)
        if self.__maximizeButton.onClick():
            displayScreenW, displayScreenH = windowInfo()
            
            if screenwidth == displayScreenW and screenheight == displayScreenH:
                self.__oldScreenSize = [screenwidth, screenheight]
                return pygame.display.set_mode((self.__displayInfo[0], self.__displayInfo[1]))
            else:
                return pygame.display.set_mode((self.__oldScreenSize[0], self.__oldScreenSize[1]), pygame.RESIZABLE | pygame.NOFRAME)
        return self.__display
    
    def __resize__(self, events):
        
        mousePos = pygame.mouse.get_pos()
        screenWidth, screenHeight = windowInfo()
        if mousePos[0] <= 2 and mousePos[0] > 0 or mousePos[0] >= screenWidth - 3:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__mouseButtonDown = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.__mouseButtonDown = False
            if self.__mouseButtonDown:
                    return pygame.display.set_mode((abs(abs(mousePos[0]) - abs(self.__oldmousePos[0])), screenHeight), pygame.RESIZABLE | pygame.NOFRAME)
        if mousePos[1] <= 2 or mousePos[1] >= screenHeight - 3:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__oldmousePos = pygame.mouse.get_pos()
                    self.__mouseButtonDown = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.__mouseButtonDown = False
                    
            if self.__mouseButtonDown:
                    return pygame.display.set_mode((screenWidth, abs(abs(mousePos[1]) - abs(self.__oldmousePos[1]))), pygame.RESIZABLE | pygame.NOFRAME)

               
      
             
        
def windowInfo():
    """
    call this `before` making a display in pygame to get the dimensions of your `computer screen`\n
    call this `after` making a display in pygame to get the dimensions of the `pygame display`
    """
    info = pygame.display.Info()
    return info.current_w, info.current_h

def windowMinSize(display, minWidth, minHeight, *flags):
    screenWidth, screenHeight = windowInfo()
    if screenWidth < minWidth:
        return pygame.display.set_mode((minWidth, screenHeight), *flags), True
    if screenHeight < minHeight:
        return pygame.display.set_mode((screenWidth, minHeight), *flags), True
    return display, False
        
def simpleButton(display, xposition: int, yposition: int, width: int, height: int, textFont, text: str = "", textColor: tuple[int, int, int] = (255, 255, 255), buttonColor: tuple[int, int, int] = (0, 0, 0), radius: int = -1, border: int = 0):
    printText = textFont.render(text, True, textColor)
    if width <= 0 or height <= 0:
        rect = pygame.draw.rect(display, buttonColor, pygame.Rect(
                xposition - 5, yposition - 5, printText.get_width() + 10, printText.get_height() + 10), border, radius)
        display.blit(printText, (xposition, yposition))
    else:
        rect = pygame.draw.rect(display, buttonColor, pygame.Rect(
                xposition, yposition, width, height), border, radius)
        display.blit(printText, (xposition + width / 2 - printText.get_width() / 2, yposition + height / 2 - printText.get_height() / 2))
    
    
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        return True
    return False

def rectDetection(display, xposition: int, yposition: int, width: int, height: int, buttonColor: tuple[int,int,int], radius: int = -1, border: int = 0):
    rect = pygame.draw.rect(display, buttonColor, pygame.Rect(
            xposition, yposition, width, height), border, radius)
    
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        return True
    return False

def simpleText(display, font, position: tuple[int,int], color: tuple[int,int,int], text: str):
        textsurface = font.render(f"{text}", True, color)
        display.blit(textsurface, (position[0], position[1]))

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
    GRAY = GREY = (100,100,100)
    DARKGRAY = DARKGREY = (50,50,50)
    DARKMODEGRAY = DARKMODEGREY = (30,30,30)
    BLACK = (0,0,0)
    
    def random():
        tuple = []
        for i in range(3):
            tuple.append(random.randint(0, 255))
        return (tuple[0], tuple[1], tuple[2])
        

            

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
    
    def customFont(size, font = None):
        if font == None:
            return pygame.font.SysFont(pygame.font.get_default_font(), size)
        else:
            return pygame.font.SysFont(font, size)


    
if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = "1"

    pygame.init()
    screenWidth, screenHeight = windowInfo()
    display = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    test = button(100, 50, color.WHITE, 10)
    test.text(font.H3, color.RED, "button")
    test.border(10, borderRadius=10)
    Text = text(display, font.H1, (300, 300))
    def func():
        print("hello")
    quitbutton = Xbutton(display, exit, color.WHITE)
    
    box = textbox(display, font.FONT50, (0, 0))
    # print(windowInfo())
    
    while True:
        clock.tick(30)
        display.fill(color.GREEN)
        events = pygame.event.get()
        test.place(display, events, (100, 100))
        
        Text.place(color.RED, "hello")
        Text.border(color.BLACK, 3)
        Text.background(color.BLUE, 20)
        # print(test.onClick(func))
        # test.onHold()
        test.changeColorOnHover(color.WHITE, color.BLUE)
        # test.recolor(color.BLUE) if test.onMouseOver() else test.recolor(color.WHITE)
        quitbutton.place(events, 500)
        
        box.place(400, color.BLACK, "dit is een text waarmee ik gebruik maak van textboxes zoals html probeer ik dit zelf nu lol", True)
        # print(pygame.mouse.get_pos())
        print(box.boxheight)
        
        for event in events:
            if event.type == pygame.QUIT:
                exit()
    
        pygame.display.update()
    
