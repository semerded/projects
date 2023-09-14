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
    if number < 0:
        number = number * -1
    return number

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
country = pygame_textinput.TextInputVisualizer()
city = pygame_textinput.TextInputVisualizer()

# Geef tweeletter-code van land (https://www.iban.com/country-codes)
land = input("Geef tweeletter-code van land (Belgie = BE): ")
# Geef stad:
stad = input(f"Geef stad (in het Engels): ")
# Geef API-key:
API_key = "9da16052f332fd97fd4a46847cebc13f"

# Stel de url  op, waarmee we JSON-data kunnen afhalen van openweathermap.org
url = f"https://api.openweathermap.org/data/2.5/forecast?q={stad},{land}&appid={API_key}"



""" STAP 2: JSON-data via request afhalen van openweathermap.org endpoint """
response_json = requests.get(url).json()

print(response_json)

def countrybar():
    pygame.draw.rect(display, )


while True:
    display.fill(wit)
    eventsGet = pygame.event.get()
    
    countrybar()
    
    for event in eventsGet:
        if event.type == pygame.QUIT:
            exit()
    
    
    
    
    




