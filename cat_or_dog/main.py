import pygame, requests, json, pygame_textinput
from pygameaddons import *
from os import path

CATAPIKEY = "live_Domf0oeKUtUcnVuuRcNS0yVh3BBvTSy9ee9TN9wt3WqupgEpKrb1sBncHhGKnAnW"
DOGAPIKEY = "live_K4sjv4DLuGrrFq5MngAPs06ToR4gEWqN094L04eXNROEQOua6ckkUSyTcFHiLqUw"

JSONSETUPFILE = "setup.json"
CATBREEDS = "catbreed.json"
DOGBREEDS = "dogbreed.json"
# dogURL = f"https://api.thedogapi.com/v1/images/search?limit={amount}&api_key={CATAPIKEY}"
# catURL = f"https://api.thecatapi.com/v1/images/search?limit={amount}&api_key={CATAPIKEY}"

def setup():
    global savefile
    if path.isfile(JSONSETUPFILE) is False:
        raise Exception("File not found")
    with open(JSONSETUPFILE) as filepath:
        savefile = json.load(filepath)
    if savefile["dogcalls"] < 100 or savefile["catcalls"] < 100:
        print("less than 100 calls left")
    if savefile["dogcalls"] < 10 or savefile["catcalls"] < 10:
        if input("less than 10 calls left! continue?: ").lower() != "y":
            raise ValueError("script stopped because not enough keys left")
# setup()

def getImages(dogURL, catURL):
    dogImage = requests.get(dogURL).json()
    catImage = requests.get(catURL).json()
    
    
    
    # om bij te houden hoevaak de api is opgroepen
    savefile["dogcalls"] -= 1
    savefile["catcalls"] -= 1
    with open(JSONSETUPFILE, 'w') as json_file:
                json.dump(savefile, json_file, indent = 4, separators=(',',': '))
      

# dragon li
      

"""
pygame setup
"""
pygame.init()
pygame.display.set_caption("under construction") #TODO
pygame.key.set_repeat(400, 30)  # press every 50 ms after waiting 200 ms
displayW, displayH = windowInfo()
display = pygame.display.set_mode((displayW - 100, displayH - 100), pygame.RESIZABLE)
clock = pygame.time.Clock()
 

"""
onderdelen van de app
"""
# header


def header():
    pygame.draw.rect(display, color.GREEN, pygame.Rect(0, 0, screenWidth, 50))
   

# sidebar 
choseDog = button(80, 40, color.ORANGE, 5)
choseCat = button(80, 40, color.ORANGE, 5)    
choseDog.text(font.H2, color.BLACK, "DOG")
choseCat.text(font.H2, color.BLACK, "CAT")

 
def sidebar():
    choseDog.place(display, events, (10, 5))
    choseDog.changeColorOnHover(color.ORANGE, color.RED)
    if choseDog.onClick():
        breeds = loadBreed(DOGBREEDS)
    
    choseCat.place(display, events, (100, 5))
    choseCat.changeColorOnHover(color.ORANGE, color.RED)
    if choseCat.onClick():
        breeds = loadBreed(CATBREEDS)

    rectDetection(display, 0, 50, 190, screenHeight - 50, color.GREY)
    
    for breed in breeds["breeds"]:
        simpleButton(display, 5, 100)
    
    
def loadBreed(fileLocation):
    with open(fileLocation) as breedFile:
        return json.load(breedFile)
    
class dier:
    pass

    
while True:
    clock.tick(60)
    display.fill(color.WHITE)
    display = windowMinSize(display, 500, 500, pygame.RESIZABLE)    
    events = pygame.event.get()
    screenWidth, screenHeight = windowInfo()

    header()
    sidebar()
    
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    
    pygame.display.flip()

    