import pygame, requests, json, pygame_textinput
from pygameaddons import *
from os import path

CATAPIKEY = "live_Domf0oeKUtUcnVuuRcNS0yVh3BBvTSy9ee9TN9wt3WqupgEpKrb1sBncHhGKnAnW"
DOGAPIKEY = "live_K4sjv4DLuGrrFq5MngAPs06ToR4gEWqN094L04eXNROEQOua6ckkUSyTcFHiLqUw"

JSONSETUPFILE = "setup.json"
CATBREEDS = "catbreed.json"
DOGBREEDS = "dogbreed.json"

breedID = ""
selection = "cat"
dogImageURL = f"https://api.thedogapi.com/v1/images/search?limit={9}&api_key={CATAPIKEY}"
caImagetURL = f"https://api.thecatapi.com/v1/images/search?limit={9}&api_key={CATAPIKEY}"

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
setup()

def updateCalls(dog: bool, cat: bool):
    if dog:
        savefile["dogcalls"] -= 1
    if cat:
        savefile["catcalls"] -= 1
    with open(JSONSETUPFILE, 'w') as json_file:
                json.dump(savefile, json_file, indent = 4, separators=(',',': '))


def getImages(dogURL, catURL):
    dogImage = requests.get(dogURL).json()
    catImage = requests.get(catURL).json()
    updateCalls()
    # om bij te houden hoevaak de api is opgroepen
    
def getInfo(breedID, selection):
    BreedURL = f"https://api.the{selection}api.com/v1/breeds/{breedID}"
    breedInfo = requests.get(BreedURL).json()
    if selection == "dog":
        updateCalls(True, False)
    if selection == "cat":
        updateCalls(False, True)
    return breedInfo
    
scrollCounter = [0,0]
def scroll(event, maxSidebarScroll):
    global scrollCounter
    
    # omhoog scrollen = negatief
    # omlaag scrollen = positief
    if scrollCounter[scrollType] <= 0:
        scrollCounter[scrollType] += event * 40
    if scrollCounter[scrollType] >= 0: # om geen gekke glitches te krijgen bij omhoogscrollen
        scrollCounter[scrollType] = 0
    if scrollCounter[scrollType] <= maxSidebarScroll:
        scrollCounter[scrollType] = maxSidebarScroll
    print(scrollCounter)
    return maxSidebarScroll
# dragon li
      

"""
pygame setup
"""
pygame.init()
pygame.display.set_caption("under construction") #TODO
pygame.key.set_repeat(400, 30)  # press every 50 ms after waiting 200 ms
displayW, displayH = windowInfo()
print(windowInfo())
display = pygame.display.set_mode((displayW - 100, displayH - 100), pygame.RESIZABLE)
clock = pygame.time.Clock()
screenWidth, screenHeight = windowInfo()
 
maxSidebarScroll = -99999999999999999999999 # ja geen uitleg nodig
action = {
    "mouseButtonClicked": False
}

"""
onderdelen van de app
"""
# header
infoButton = button(120, 40, color.BLUE, 5)
imageButton = button(120, 40, color.BLUE, 5)
gameButton = button(120, 40, color.BLUE, 5)
quitButton = Xbutton(display, size= 40)

def header():
    pygame.draw.rect(display, color.GREEN, pygame.Rect(0, 0, screenWidth, 50))
    infoButton.text(font.H2, color.BLACK, f"{selection} info")
    infoButton.place(display, events, (screenWidth / 2 - 190, 5))
    infoButton.changeColorOnHover(color.BLUE, color.LIGHTBLUE)
    infoButton.onClick()
    
    imageButton.text(font.H2, color.BLACK, f"{selection} images")
    imageButton.place(display, events, (screenWidth / 2 - 60, 5))

    imageButton.changeColorOnHover(color.BLUE, color.LIGHTBLUE)
    imageButton.onClick()
    
    gameButton.text(font.H2, color.BLACK, "game")
    gameButton.place(display, events, (screenWidth / 2 + 70, 5))
    gameButton.changeColorOnHover(color.BLUE, color.LIGHTBLUE)
    gameButton.onClick()
    
    quitButton.repostion(screenWidth - 50, 5)
    quitButton.place(events, screenWidth)


# sidebar 
def loadBreed(fileLocation):
    with open(fileLocation) as breedFile:
        return json.load(breedFile)

breeds = loadBreed(CATBREEDS)

choseDog = button(120, 40, color.ORANGE, 5)
choseCat = button(120, 40, color.ORANGE, 5)    
choseDog.text(font.H2, color.BLACK, "DOG")
choseCat.text(font.H2, color.BLACK, "CAT")



def sidebar():
    global breeds, selection, hoverBreed ,chosenBreed

    choseDog.place(display, events, (10, 5))
    choseDog.changeColorOnHover(color.ORANGE, color.RED)
    if choseDog.onClick():
        breeds = loadBreed(DOGBREEDS)
        selection = "dog"
        scrollCounter[0] = 0
        hoverBreed = chosenBreed = ""

    
    choseCat.place(display, events, (140, 5))
    choseCat.changeColorOnHover(color.ORANGE, color.RED)
    if choseCat.onClick():
        breeds = loadBreed(CATBREEDS)
        selection = "cat"
        scrollCounter[0] = 0
        hoverBreed = chosenBreed = ""

        

hoverBreed = chosenBreed = ""
def scrollsidebar():
    global scrollType, hoverBreed, chosenBreed
    if rectDetection(display, 0, 50, 270, screenHeight - 50, color.GREY):
        scrollType = 0
    spacing = 0
    for breed in breeds["breeds"]:
        Color = color.YELLOW if hoverBreed == breed else color.DARKGREEN
        textColor = color.BLACK if hoverBreed == breed else color.WHITE
        if chosenBreed == breed:
            Color = color.RED
            textColor = color.BLACK
        if simpleButton(display, 5, 55 + spacing + scrollCounter[0], 260, 40, font.H3, breed, textColor=textColor, buttonColor=Color, radius=5):
            hoverBreed = breed
            if action["mouseButtonClicked"]:
                chosenBreed = breed
        
        spacing += 45


"""
body

info over de dieren
"""
choseBreedText = text(display, font.FONT100, (0, 0))
searchButton = button(screenWidth - 280, 50, color.GREY, radius=5) 
def body():
    global scrollType, breedID
    if rectDetection(display, 270, 50, screenWidth - 270, screenHeight - 50, color.WHITE):
        scrollType = 1
    if chosenBreed == "":
        choseBreedText.centerdText((270, screenWidth, 50, screenHeight))
        choseBreedText.place(color.BLACK, f"choose a {selection}")
    else:
        searchButton.text(font.H1, color.BLACK, "SEARCH")
        searchButton.changeColorOnHover(color.GREY, color.LESSWHITE)
        searchButton.place(display, events, (275, 55))
        if searchButton.onClick():
            breedID = breeds["breeds"][chosenBreed]
            print(breedID)
            breedInfo = getInfo(breedID)
            print(breedInfo)   
            
        
    
class dier:
    pass

    
while True:
    clock.tick(60)
    display.fill(color.WHITE)
    display = windowMinSize(display, 1000, 500, pygame.RESIZABLE)    
    events = pygame.event.get()
    screenWidth, screenHeight = windowInfo()
    
    scrollsidebar()
    header()
    sidebar()
    body()
    
    
    if scrollCounter[0] < maxSidebarScroll:
        scrollCounter[0] = maxSidebarScroll
    screenNotUsed = displayH - screenHeight
    maxSidebarScroll = breeds["height"] - screenNotUsed + 50
    
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEWHEEL:
            scroll(event.y, maxSidebarScroll)
        if event.type == pygame.MOUSEBUTTONDOWN:
            action["mouseButtonClicked"] = True
        if event.type == pygame.MOUSEBUTTONUP:
            action["mouseButtonClicked"] = False

    
    
    pygame.display.flip()

    