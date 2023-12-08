try:
    import pygame
except ImportError:
    raise ImportError("import pygame")
import random
import sys
from typing_extensions import TypeAlias, Literal
from enum import Enum

from colors import Color
from fonts import Font

pygame.init()

screenUnit: TypeAlias = int | str
modifiableFunctions: TypeAlias = Literal[
    "quit"
]

RGBvalue: TypeAlias = tuple[int, int, int]
font : TypeAlias = pygame.font

def notBelowZero(input: int | float) -> (int | float):
    if input < 0:
        return 0
    return input


class mouseButton(Enum):
    leftMouseButton = 1
    rightMouseButton = 2
    middleMouseButton = 3
    unknownbutton1 = 4
    unknownbutton2 = 5
    mouseButton4 = 6
    mouseButton5 = 7
    
class interactionType(Enum):
    mouseOver = 1
    mouseClick = 2
    mouseRelease = 3
    mouseHold = 4


screenInfo = pygame.display.Info()
userScreenWidth = screenInfo.current_w
userScreenHeight = screenInfo.current_h
mainDisplay = None

mouseButtonsStatus = [False, False, False, False, False]
previousMouseButtonStatus = [False, False, False, False]


class AppConstructor():
    def __init__(self, screenWidth, screenHeight, *flags) -> None:
        global mainDisplay
        self.screenWidth = screenInfo.current_w
        self.screenHeight = screenInfo.current_h
        self.APPdisplayFlags = flags

        self.minimumScreenWidth = None
        self.minimumScreenHeight = None
        self.modifiedFunctions = {"quit": None}

        self.APPdisplay = pygame.display.set_mode(
            (screenWidth, screenHeight), *flags)
        mainDisplay = self.APPdisplay

    def eventHandler(self, appEvents: pygame.event):
        Updating.updateDisplay()
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseButtonsStatus[event.button] = True

            if event.type == pygame.MOUSEBUTTONUP:
                mouseButtonsStatus[event.button] = False

    def resizeAppscreen(self, screenWidth, screenHeight, *flags):
        self.APPdisplayFlags = flags
        self.APPdisplay = pygame.display.set_mode(
            (screenWidth, screenHeight), *flags)

    def setModifiableFunctions(self, **kwargs: modifiableFunctions):  # TODO
        for modifiedFunction, newFunction in kwargs.items():
            self.modifiedFunctions[modifiedFunction] = newFunction

    def setMinimumScreenDimensions(self, minimumScreenWidth: screenUnit = None, minimumScreenHeight: screenUnit = None):
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
        self.APPdisplay = pygame.display.set_mode(
            (self.screenWidth, self.screenHeight), *self.APPdisplayFlags)
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

    def vw(screenUnit: float) -> float:
        return userScreenWidth / 100 * screenUnit

    def vh(screenUint: float) -> float:
        return userScreenHeight / 100 * screenUnit


class Image:
    def __init__(self, fileName: str, nameHint: str = "") -> None:
        self.image = pygame.image.load(fileName, nameHint)
        self.imageSize = self.getSize
        self.imagePosition = (0, 0)

    def resizeAndKeepProportions(self, width: float, height: float):
        aspectRatio = self.getAspectRatio
        imageWidth, imageHeight = self.getSize
        if aspectRatio < 1:
            width = int(imageWidth * aspectRatio)
        else:
            height = int(imageHeight / aspectRatio)
        self.scale(width, height)

    def scale(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.imageSize = self.getSize

    def isMouseOver(self):
        return Interactions.isMouseOver(self.getImageRect)

    def isClicked(self, mouseButton: mouseButton):
        return Interactions.isClicked(self.getImageRect, mouseButton)

    def isReleased(self, mouseButton: mouseButton):
        return Interactions.isReleased(self.getImageRect, mouseButton)

    def isHolding(self, mouseButton: mouseButton):
        return Interactions.isHolding(self.getImageRect, mouseButton)

    def place(self, xPosition: float, yPosition: float):
        self.imagePosition = (xPosition, yPosition)
        self.image.blit(mainDisplay, self.imagePosition)

    @property
    def getAspectRatio(self):
        imageWidth, imageHeight = self.getSize
        return imageWidth / imageHeight

    @property
    def getSize(self):
        return self.image.get_size()

    @property
    def getPosition(self):
        return self.imagePosition

    @property
    def getImageRect(self):
        return pygame.Rect(*self.getPosition, *self.getSize)

    @property
    def getImage(self):
        return self.image


class Interactions:
    def __init__(self) -> None:
        pass

    def isMouseButtonPressed(mouseButton: mouseButton):
        if mouseButtonsStatus[mouseButton.value]:
            return True
        return False

    def mouseButtonPositiveFlank(mouseButton: mouseButton):
        if mouseButtonsStatus[mouseButton] and not previousMouseButtonStatus[mouseButton]:
            previousMouseButtonStatus[mouseButton] = True
            return True
        return False

    def mouseButtonNegativeFlank(mouseButton: mouseButton):
        if not mouseButtonsStatus[mouseButton] and previousMouseButtonStatus[mouseButton]:
            previousMouseButtonStatus[mouseButton] = False
            return True
        return False

    def isMouseOver(rect: pygame.Rect):
        mousePos = pygame.mouse.get_pos()
        if rect.collidepoint(mousePos):
            return True
        return False

    def isClicked(rect: pygame.Rect, mouseButton: mouseButton):
        if Interactions.isMouseOver(rect) and Interactions.mouseButtonPositiveFlank(mouseButton.value):
            return True
        return False

    def isReleased(rect: pygame.Rect, mouseButton: mouseButton):
        if Interactions.isMouseOver(rect) and Interactions.mouseButtonNegativeFlank(mouseButton.value):
            return True
        return False

    def isHolding(rect: pygame.Rect, mouseButton: mouseButton):
        if Interactions.isMouseOver(rect) and Interactions.isMouseButtonPressed(mouseButton.value):
            return True
        return False
            


class Text:

    pass

    def place(self):
        pass
    
class Updating:
    def updateDisplay():
        pygame.display.update()
        
    def __init__(self, **kwargs) -> None:
        self.objectList = kwargs
        self.emptyObjectList = kwargs
        
    def resetObjectList(self):
        self.objectList = self.emptyObjectList


class Button:
    def __init__(self,
                 size: tuple[screenUnit, screenUnit],
                 color: RGBvalue,
                 borderRadius:int = -1
                 ) -> None:
        self.buttonSize = size
        self.buttonColor = color
        self.borderRadius = borderRadius
        self.buttonAtributes = Updating(_text=False, _border=False)

    def simpleButton(size,
                     position, 
                     backgroundColor: RGBvalue = Color.LIGHTGRAY, 
                     text: str = "", 
                     font: font = Font.H3,
                     textColor: RGBvalue = Color.BLACK, 
                     cornerRadius: int = -1, 
                     borderWidth: int = 0,
                     borderColor: RGBvalue = Color.BLACK,
                     ) -> bool:
        
        buttonRect = Drawing.rectangle(position[0], position[1], size[0], size[1], backgroundColor, cornerRadius)
        if borderWidth > 0:
            buttonRect = Drawing.border(borderWidth, buttonRect, borderColor, cornerRadius)
        if text != "":
            buttonText = font.render(text, True, textColor)
            mainDisplay.blit(buttonText, (position[0] + size[0] / 2 - buttonText.get_width() / 2, position[1] + size[1] / 2 - buttonText.get_height() / 2))
        return Interactions.isClicked(buttonRect, mouseButton.leftMouseButton)
        
        

    def text(self, text: str, textFont: pygame.font = Font.H4, textColor: RGBvalue = Color.BLACK):
        self._text = text
        self._textFont = textFont
        self._textColor = textColor
        self.buttonAtributes["_text"] = True

    def border(self):
        ...

    def radius(self):
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

class Drawing:
    def rectangle(xPosition: float, yPosition: float, width: float, height: float, color: RGBvalue = Color.LIGHTGRAY, cornerRadius: int = -1):
        return pygame.draw.rect(mainDisplay, color, pygame.Rect(xPosition, yPosition, width, height), border_radius=cornerRadius)
    
    def border(borderWidth: int, rectValue: pygame.Rect | tuple[float, float, float, float], color: RGBvalue = Color.BLACK, cornerRadius: int = -1) -> pygame.Rect:
        if isinstance(rectValue, pygame.Rect):
            xPosition = rectValue.x - borderWidth / 2
            yPosition = rectValue.y - borderWidth / 2
            width = rectValue.width + borderWidth
            height = rectValue.height + borderWidth
        else:
            xPosition = rectValue[0] - borderWidth / 2
            yPosition = rectValue[1] - borderWidth / 2
            width = rectValue[2] - borderWidth
            height = rectValue[3] - borderWidth
        return pygame.draw.rect(mainDisplay, color, pygame.Rect(xPosition, yPosition, width, height), width=borderWidth, border_radius=cornerRadius)
 
            
class textbox:
    def __init__(self) -> None:
        pass
