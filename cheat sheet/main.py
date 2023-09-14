import pygame
import pygame_textinput
import json
import os
import pyperclip
from colors import *
from setup import *
from functions import *

"""
program info

default border radius = 5
"""

# global vars
quitButton = inputFieldQuitButton = False
inputStep = lineCounter = scrollCounter = editNumber = 0


action = {
    "quitActive": False,
    "crtl": False,
    "shift":False,
    "enableSearch": False,
    "searching": False,
    "inputField": False,
    "mouseClick": False,
    "comfirmClose": False,
    "editField": False,
    
}

# const vars
JsonBuildUp = ["name", "description", "function"]


# buttons on sticky top
languageList = ["javascript", "arduino", "python", "html"]
languageColorList = [geel, turquise, blauw, oranje]
LanguageColor = geel
deleteItem = [False, 0]


# pygame functions
def vierkantdetectie(xpositie: int, ypositie: int, lengte: int, hoogte: int, kleurvierkant: tuple[int, int, int] = (0, 0, 0), rand: int = 0, afvlakking: int = -1):

    global mouse_pos
    rect = pygame.draw.rect(display, kleurvierkant, pygame.Rect(
        xpositie, ypositie, lengte, hoogte), rand, afvlakking)
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        return True
    return False

def button(xpositie: int, ypositie: int, lengte: int, hoogte: int, textFont, text: str = "", textColor: tuple[int, int, int] = (255, 255, 255), kleurvierkant: tuple[int, int, int] = (0, 0, 0), rand: int = 0, afvlakking: int = -1):
    global mouse_pos

    printText = textFont.render(text, True, textColor)
    if lengte <= 0 or hoogte <= 0:
        rect = pygame.draw.rect(display, kleurvierkant, pygame.Rect(
                xpositie - 5, ypositie - 5, printText.get_width() + 10, printText.get_height() + 10), rand, afvlakking)
        display.blit(printText, (xpositie, ypositie))
    else:
        rect = pygame.draw.rect(display, kleurvierkant, pygame.Rect(
                xpositie, ypositie, lengte, hoogte), rand, afvlakking)
        display.blit(printText, (xpositie + lengte / 2 - printText.get_width() / 2, ypositie + hoogte / 2 - printText.get_height() / 2))
    
    
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        return True
    return False

def centerdPopUp(width:int, height:int, borderwidth:int, borderheight:int, color:tuple[int,int,int], borderColor:tuple[int,int,int] = (0,0,0)):
    centerdRect = pygame.Rect(0, 0, width, height)
    centerdBorderRect = pygame.Rect(0, 0, width + borderwidth, height + borderheight)
    centerdRect.center = (screenWidth / 2, screenHeight / 2)
    centerdBorderRect.center = centerdRect.center
    pygame.draw.rect(display, borderColor, centerdBorderRect, border_radius=5)
    pygame.draw.rect(display, color, centerdRect, border_radius=5)

def text(font, color, x_axis, y_axis, text):
    printText = font.render(text, True, color)
    display.blit(printText, (x_axis, y_axis))


def centerdText(font, color, y_axis, text):
    printText = font.render(text, True, color)
    display.blit(printText, (screenWidth / 2 -
                 printText.get_width() / 2, y_axis))
    
def neg(number):
    if number < 0:
        number = number * -1
    return number


JsonFilePath = "cheat sheet.json"
JsonSetupPath = "setup.json"
# check if file exists
if os.path.isfile(JsonFilePath) is False or os.path.isfile(JsonSetupPath) is False:
    raise Exception("File not found")

# open json files (setup file and save file)
with open(JsonFilePath) as filepath:
    savefile = json.load(filepath)
def loadJson():
    global setupfile
    with open(JsonSetupPath) as setuppath:
        setupfile = json.load(setuppath)
loadJson()
CheatLanguage = savefile["javascript"]
refreshRate = setupfile["refreshrate"]

os.environ['SDL_VIDEO_CENTERED'] = '1'


pygame.init()

h1 = pygame.font.SysFont(pygame.font.get_default_font(), 32)
h4 = pygame.font.SysFont(pygame.font.get_default_font(), 24)
defaultTextSize = pygame.font.SysFont('arial', 20)
clock = pygame.time.Clock()


def getScreenInfo():
    global screenHeight, screenWidth
    info = pygame.display.Info()
    screenWidth, screenHeight = info.current_w, info.current_h


def checkScreenSize():
    global display, screenWidth, screenHeight
    if screenWidth < 800:
        screenWidth = 800
    if screenHeight < 500:
        screenHeight = 500
    display = pygame.display.set_mode(
        (screenWidth, screenHeight), pygame.RESIZABLE)


getScreenInfo()
screenWidth, screenHeight = screenWidth - 100, screenHeight - 100
checkScreenSize()


pygame.display.set_caption("schijt blad")
pygame.key.set_repeat(400, 30)  # press every 50 ms after waiting 200 ms
search = pygame_textinput.TextInputVisualizer()
inputName = pygame_textinput.TextInputVisualizer()
inputDescription = pygame_textinput.TextInputVisualizer()
inputFunction = pygame_textinput.TextInputVisualizer()
inputList = [inputName, inputDescription, inputFunction]

def emptyInput():
    for input in inputList:
        input.value = ""

def stickyTop():
    global CheatLanguage, LanguageColor, quitButton, inputStep, scrollCounter
    pygame.draw.rect(display, groen, pygame.Rect(0, 0, screenWidth, 50))

    # quit button
    quitButtonKleur = rood if quitButton else grijs
    quitButton = button(
        (screenWidth - 30), 0, 30, 30, h1, "X", wit, quitButtonKleur, afvlakking=5)

    # add button
    if button(screenWidth - 50 - 100, 5, 110, 40, h4, "add function", zwart, wit, afvlakking=5) and action["mouseClick"]:
        emptyInput()
        action["editField"] = False
        action["inputField"] = True
        inputStep = 0

    # language buttons
    for index, language in enumerate(languageList):
        if button(5 + (100 * index), 5, 100, 40, h4, language, zwart, languageColorList[index], afvlakking=5) and action["mouseClick"]:
            LanguageColor = languageColorList[index]
            CheatLanguage = savefile[language]
    pygame.draw.line(display, LanguageColor, (0, 90),
                     (screenWidth, 90), 5)  # draw start line
    
    if scrollCounter < 0 and button(20, screenHeight - 50, 30, 30, h1, "^", zwart, LanguageColor, afvlakking=15) and action["mouseClick"]:
        scrollCounter = 0
        
    # scroll balk
    try:
        scrollScale = (screenHeight - 93 - 40) / lineCounter
    except ZeroDivisionError:
        scrollScale = 0
    
    
    pygame.draw.rect(display, wit, pygame.Rect(screenWidth - 20, 93, 20, screenHeight - 93))
    pygame.draw.rect(display, grijs, pygame.Rect(screenWidth - 20,(neg(scrollCounter)) * scrollScale + 93 , 20, 40)) #screenHeight - (screenHeight - 93)
        


def inputField(titleText, savebuttonText, editFile: bool, number: int | None = None, values: list = []):
    """
    breedte = 780
        helft: 390
    hoogte = 480
        helft: 240
    
    """
    global inputFieldQuitButton, inputStep
    action["enableSearch"] = False
    centerdPopUp(780, 480, 10, 10, LanguageColor)

    # input field quit button
    inputFieldQuitColor = rood if inputFieldQuitButton else grijs
    inputFieldQuitButton = button(
        ((screenWidth / 2) + (790 / 2) - 35), ((screenHeight / 2) - (490 / 2) + 5), 30, 30, h1, "X", wit, inputFieldQuitColor, afvlakking=5)
    if inputFieldQuitButton and action["mouseClick"]:
        action["inputField"] = False
        action["editField"] = False

    # inputs
    inputWidth = screenWidth / 2 - 380
    centerdText(h1, zwart, screenHeight / 2 - 200, titleText)
    print(number)

    # input name
    centerdText(h4, zwart, screenHeight / 2 - 130, "Function Name")
    pygame.draw.rect(display, wit, pygame.Rect(screenWidth / 2 - 385, screenHeight / 2 - 110, 760, 50), border_radius=5)
    if inputStep == 0:
        inputName.update(eventGet)
    else:
        inputName.cursor_visible = False
    display.blit(inputName.surface, (inputWidth, screenHeight / 2 - 100))

    # input description
    centerdText(h4, zwart, screenHeight / 2 - 30, "Function Description")
    pygame.draw.rect(display, wit, pygame.Rect(screenWidth / 2 - 385, screenHeight / 2 - 10, 760, 50), border_radius=5)

    if inputStep == 1:
        inputDescription.update(eventGet)
    else:
        inputDescription.cursor_visible = False
    display.blit(inputDescription.surface, (inputWidth, screenHeight / 2))
    
    # input function
    centerdText(h4, zwart, screenHeight / 2 + 70, "Function")
    pygame.draw.rect(display, wit, pygame.Rect(screenWidth / 2 - 385, screenHeight / 2 + 90, 760, 50), border_radius=5)

    if inputStep == 2:
        inputFunction.update(eventGet)
    else:
        inputFunction.cursor_visible = False
    display.blit(inputFunction.surface,
                     (inputWidth, screenHeight / 2 + 100)) 
    if not inputName.value == "" and not inputDescription.value == "" and not inputFunction.value == "":
        saveButtonColor = groen
        saveCheck = True
    else:
        saveButtonColor = rood
        saveCheck = False
    pygame.draw.rect(display, zwart, pygame.Rect(screenWidth / 2 - 105, screenHeight / 2 + 175, 210, 60), border_radius=5)
    if button(screenWidth / 2 - 100, screenHeight / 2 + 180, 200, 50, h1, savebuttonText, wit, saveButtonColor, afvlakking=5) and saveCheck and action["mouseClick"]:
        addFunctionDict = {
            "name": inputName.value,
            "description": inputDescription.value,
            "function": inputFunction.value
        }
        CheatLanguage.append(addFunctionDict)
        with open(JsonFilePath, 'w') as json_file:
            json.dump(savefile, json_file, indent = 4, separators=(',',': '))
        inputName.value = inputDescription.value = inputFunction.value = ""
        inputStep = 0
        action["editField"] = False
        action["inputField"] = False
        
    
    

def quitApp(type, bypass = False):
    global action
    if type == "click" and quitButton:
        action["quitActive"] = True
    else:
        if quitButton and action["quitActive"]:
            if bypass:
                exit()
            action["comfirmClose"] = True
        else:
            action["quitActive"] = False

def confirmPopUp(text):
    centerdPopUp(250, 150, 10, 10, groen, wit)
    centerdText(h1, zwart, screenHeight / 2 - 50, text)
    if button(screenWidth / 2 - 95, screenHeight / 2, 90, 40, h1, "confirm", zwart, blauw, afvlakking=5) and action["mouseClick"]:
        return True
    if button(screenWidth / 2 + 5, screenHeight / 2, 90, 40, h1, "cancel", zwart, rood, afvlakking=5) and action["mouseClick"]:
        return False


def placeTextFromJson():
    global lineCounter, deleteItem, editNumber
    lineCounter = 0
    

    for i in range(len(CheatLanguage)):
        if action["searching"]:
            # skip item if the search value doesn't contain the name
            if not search.value.lower() in CheatLanguage[i]['name']:
                continue
            
        if button(screenWidth - 110, 100 + lineCounter + scrollCounter, 30, 30, h1, "E", wit, blauw, afvlakking=5) and action["mouseClick"]: # edit button
            action["editField"] = True
            editNumber = i
        if button(screenWidth - 70, 100 + lineCounter + scrollCounter, 30, 30, h1, "x", wit, rood, afvlakking=5) and action["mouseClick"]: # copy button
            deleteItem[0] = True
            deleteItem[1] = i
        if button(screenWidth - 110, 140 + lineCounter + scrollCounter, 70, 30, h1, "copy", zwart, LanguageColor, afvlakking=5) and action["mouseClick"]: # delete button
            pyperclip.copy(f"{CheatLanguage[i]['function']}")
            
        # name of function in green
        text(h1, groen, 10, 100 + lineCounter + scrollCounter, f"{CheatLanguage[i]['name']}")
        lineCounter += 30

        # description of function in grey
        text(h4, grijs, 10, 100 + lineCounter + scrollCounter,
             f"{CheatLanguage[i]['description']}")
        lineCounter += 25

        # function in white (spaced appart)
        functionList = CheatLanguage[i]['function'].split("\n")
        for line in range(len(functionList)):
            text(defaultTextSize, wit, 10, 100 +
                 lineCounter + scrollCounter, f"{functionList[line]}")
            
            lineCounter += 23

        # draw line to see the difference better
        pygame.draw.line(display, LanguageColor, (0, 100 +
                         lineCounter + 10 + scrollCounter), (screenWidth, 100 + lineCounter + 10 + scrollCounter), 5)
        lineCounter += 25


def searchMode():
    search.update(eventGet)
    display.blit(search.surface, (10, 55))
    
def scroll(direction):
    global scrollCounter
    if lineCounter > screenHeight - 200 and scrollCounter <= 0:
        if abs(scrollCounter) + screenHeight - 200 < lineCounter:
            scrollCounter += direction * 20
            if scrollCounter > 0:
                scrollCounter = 0
        elif direction > 0:
            scrollCounter += direction * 20    
  
 


"""
main loop
"""

while True:
    clock.tick(refreshRate)
    display.fill(darkmodegrey)  # redraw screen
    eventGet = pygame.event.get()

    # the chosen language from the json file will be placed and space appart for easy reading (scrollable)
    placeTextFromJson()
    
    # header that doesn't move while scrolling
    stickyTop()

    if action["enableSearch"]:
        pygame.draw.rect(display, wit, pygame.Rect(0, 50, screenWidth, 38))
        searchMode()
        action["searching"] = True if search.value != "" else False

    else:
        pygame.draw.rect(display, grijs, pygame.Rect(0, 50, screenWidth, 38))
        text(h1, zwart, 10, 60, "Crtl + F to search a title")

    if action["inputField"]:
        inputField("INPUT A NEW FUNCTION", "Save Function", False)
        
    if action["editField"]:
        inputField("EDIT FUNCTION", "Update Function", True, editNumber, [CheatLanguage[editNumber]['name'], CheatLanguage[editNumber]['description'], CheatLanguage[editNumber]['function']])
        for index, input in enumerate(inputList):
            input.value = CheatLanguage[editNumber][JsonBuildUp[index]]
        
    if action["comfirmClose"]:
        confirm = confirmPopUp("close app?")
        if confirm:
            exit()
        elif confirm == False:
            action["comfirmClose"] = False
        
    if deleteItem[0]:
        if action["comfirmClose"]:
            action["comfirmClose"] = False
        confirm = confirmPopUp("delete item?")
        if confirm:
            CheatLanguage.pop(deleteItem[1])
            with open(JsonFilePath, 'w') as json_file:
                json.dump(savefile, json_file, indent = 4, separators=(',',': '))
            deleteItem[0] = False
        elif confirm == False:
            deleteItem[0] = False

    # events
    for event in eventGet:
        if event.type == pygame.MOUSEBUTTONDOWN:
            action["mouseClick"] = True
            quitApp("click")

        if event.type == pygame.MOUSEBUTTONUP:
            action["mouseClick"] = False
            if action["shift"]:
                quitApp("quit", True)

            else:
                quitApp("quit")
            
        if event.type == pygame.MOUSEWHEEL:
            scroll(event.y)
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                action["shift"] = True
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:  # crtl pressed
                action["crtl"] = True
            if event.key == pygame.K_RETURN:
                if action["inputField"]:
                    inputStep += 1
                    if inputStep == 3:
                        inputStep = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                action["shift"] = False
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:  # crtl unpressed
                action["crtl"] = False

            if event.key == pygame.K_f:
                if action["crtl"]:  # enable search
                    action["enableSearch"] = not action["enableSearch"]
                    search.value = ""  # empty search bar
            if event.key == pygame.K_v:
                if action["crtl"]:
                    if action["inputField"]:
                        inputList[inputStep].value = ""
                        inputList[inputStep].value = pyperclip.paste().replace("\r", "")

        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.WINDOWRESIZED:
            getScreenInfo()
            checkScreenSize()

    
    pygame.display.flip()
