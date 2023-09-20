import json, requests, pygame, os, pygame_textinput
from colors import *

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
    if number > 0:
        number = number * -1
    return number

scrollCounter = 0
def scroll(direction):
    # 8715
    global scrollCounter
    if direction < 0: # scroll down
        if abs(scrollCounter) < abs(8715 - (screenHeight - 100)):
            scrollCounter += direction * 100
        else:
            scrollCounter = -8715 + (screenHeight - 105)
    if direction > 0: # scroll up
        scrollCounter += direction * 100
        if scrollCounter > 0:
            scrollCounter = 0

os.environ['SDL_VIDEO_CENTERED'] = '1'


pygame.init()


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

h1 = pygame.font.SysFont(pygame.font.get_default_font(), 32)
h4 = pygame.font.SysFont(pygame.font.get_default_font(), 24)
defaultTextSize = pygame.font.SysFont('arial', 20)
clock = pygame.time.Clock()
pygame.display.set_caption("weather forcaster")
pygame.key.set_repeat(400, 30)  # press every 50 ms after waiting 200 ms
cityInput = pygame_textinput.TextInputVisualizer()


country = ""
status = -1
validInput = False

action = {
    "mouseClicked": False, 
    "cityInput": False,
}

APIKEY = "9da16052f332fd97fd4a46847cebc13f" # api key

JsonFilePath = "countrycodes.json"
if os.path.isfile(JsonFilePath) is False:
    raise Exception("File not found")
with open(JsonFilePath) as filepath:
    alpha2codes = json.load(filepath)



def requestAPI(city):
    global status
    # website: openweathermap.org

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={APIKEY}"
    response_json = requests.get(url).json()
    if response_json['cod'] == '200':
        status = 200
    elif response_json['cod'] == '404':
        status = 404
    else:
        status = 0

def header():
    pygame.draw.rect(display, LIGHTBLUE, pygame.Rect(0, 0, screenWidth, 100))
    

def countrybar():
    global country
    countryButtonHeight = 0
    vierkantdetectie(0, 100, 300, screenHeight - 100, LESSWHITE)
    for countries in alpha2codes:
        buttonColor = GREEN if country == countries["Code"] else YELLOW
        if button(5, 105 + countryButtonHeight + scrollCounter, 290, 30, h1, countries["Name"], BLACK, buttonColor, afvlakking=5) and action["mouseClicked"]:
            country = countries["Code"]
            action["cityInput"] = True
            
        countryButtonHeight += 35

def inputField():
    global validInput
    searchBarColor = GREY if action["cityInput"] else LESSWHITE
    searchBar = vierkantdetectie(300, 100, screenWidth - 160 - 300, 40, searchBarColor)
    if searchBar and action["mouseClicked"]:
        action["cityInput"] = True
    if not searchBar and action["mouseClicked"]:
        action["cityInput"] = False
    
    if action["cityInput"]:
        cityInput.update(eventsGet)
    else:
        cityInput.cursor_visible = False
    display.blit(cityInput.surface, (310, 105))
    if country != "" and cityInput.value != "":
        validInput = True
    else:
        validInput = False
    
    buttonColor = GREEN if validInput else RED
    if button(screenWidth - 155, 105, 150, 30, h1, "Search City", BLACK, buttonColor, afvlakking=5) and action["mouseClicked"]:
        if validInput:
            requestAPI(cityInput.value)
            action["cityInput"] = False
            cityInput.value = ""
        else:
            action["cityInput"] = True
            
class ShowResult:
    workwidth = screenWidth - 300
    workheight = screenHeight - 100

    def Weather():
        pass

    def NotFound():
        pass

    def Error():
        pass
while True:
    display.fill(WHITE)
    eventsGet = pygame.event.get()
    inputField()

    countrybar()
    
    header()
    
    # check status
    if status == 200:
        ShowResult.Weather()
    elif status == 404:
        ShowResult.NotFound()
    else:
        ShowResult.Error()
    
    
    for event in eventsGet:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.WINDOWRESIZED:
            getScreenInfo()
            checkScreenSize()
        if event.type == pygame.MOUSEBUTTONDOWN:
            action["mouseClicked"] = True
        if event.type == pygame.MOUSEBUTTONUP:
            action["mouseClicked"] = False
        if event.type == pygame.MOUSEWHEEL:
            scroll(event.y)
    pygame.display.flip()
    
    
    
    




