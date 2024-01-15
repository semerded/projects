from enum import Enum
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
    
class overFlow(Enum):
    ellipsis = 1
    hide = 2
    show = 3