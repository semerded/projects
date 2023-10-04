import pygame, requests, json
from pygameaddons import *
from os import path
from io import BytesIO
from urllib.request import urlopen, Request

CATAPIKEY = "live_Domf0oeKUtUcnVuuRcNS0yVh3BBvTSy9ee9TN9wt3WqupgEpKrb1sBncHhGKnAnW"
DOGAPIKEY = "live_K4sjv4DLuGrrFq5MngAPs06ToR4gEWqN094L04eXNROEQOua6ckkUSyTcFHiLqUw"

JSONSETUPFILE = "setup.json"
CATBREEDS = "catbreed.json"
DOGBREEDS = "dogbreed.json"


dogImageURL = f"https://api.thedogapi.com/v1/images/search?limit={9}&api_key={CATAPIKEY}"
caImagetURL = f"https://api.thecatapi.com/v1/images/search?limit={9}&api_key={CATAPIKEY}"

def setup(): # checkt hoevaak je nog de api kunt oproepen TODO reset elke maand
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

def updateCalls(dog: bool, cat: bool): # update de lijst van apicalls
    # update alleen wat nodig is
    if dog:
        savefile["dogcalls"] -= 1 
    if cat:
        savefile["catcalls"] -= 1
    with open(JSONSETUPFILE, 'w') as json_file: # update bestand
                json.dump(savefile, json_file, indent = 4, separators=(',',': '))

class get: # hierin wordt de api opgeroepen en de data verwerkt
    def __init__(self, breedID :str = "", selection: str = "", amount: int = 0) -> None:
        self.__breedID = breedID
        self.__selection = selection
        self.__amount = amount
    
    def getInfo(self): # krijg de info van het geselecteerde ras
        BreedURL = f"https://api.the{self.__selection}api.com/v1/breeds/{self.__breedID}"
        self.__breedInfo = requests.get(BreedURL).json()
        return self.__breedInfo
    
    def getImages(self): # krijg foto's van het geselecteerde ras
        apikey = self.____getAPIkey__()
        BreedImageURL = f"https://api.the{self.__selection}api.com/v1/images/search?limit={self.__amount}&breed_ids={self.__breedID}&api_key={apikey}"
        self.__breedImage = requests.get(BreedImageURL).json()
        return self.__breedImage
    
    def showImage(self, imageNumber):
        req = Request(
            url=self.__breedImage[imageNumber]["url"], 
            headers={'User-Agent': 'Mozilla/5.0'})
        imageString = urlopen(req).read()
        imageFile = BytesIO(imageString)
        pyimage = pygame.image.load(imageFile)
        self.___imageSize = screenHeight / 2
        pyimage = pygame.transform.smoothscale(pyimage, (self.___imageSize, self.___imageSize))
        return pyimage
    
    def __getAPIkey__(self): # 
        if self.__selection == "cat":
            updateCalls(False, True)
            return CATAPIKEY
        elif self.__selection == "dog":
            updateCalls(True, False)
            return DOGAPIKEY
        else:
            raise ValueError("selection was not a cat or dog")
    @property
    def imageAmount(self):
        return len(self.__breedImage)
    
    @property
    def imageSize(self):
        return self.___imageSize
        
        
        
    def getRandomImage(self):
        pass
    
    def getGameImage(self):
        pass

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

def loadBreed(fileLocation):
    with open(fileLocation) as breedFile:
        return json.load(breedFile)

"""
opbouw van de app ondergeschikt in de app klasse

ik gebruik hier klassen om makkelijker variabelen rond te gooien tussen de verschillende UI delen
"""
class app:
    def __init__(self):
        self.__breedID = ""
        self.__selection = "cat"
        # header
        self.__infoButton = button(120, 40, color.BLUE, 5)
        self.__imageButton = button(120, 40, color.BLUE, 5)
        self.__gameButton = button(120, 40, color.BLUE, 5)
        self.__quitButton = Xbutton(display, size= 40)
        self.__category = "info"
        
        # sidebar
        self.__breeds = loadBreed(CATBREEDS)

        self.__choseDog = button(120, 40, color.ORANGE, 5)
        self.__choseCat = button(120, 40, color.ORANGE, 5)    
        self.__choseDog.text(font.H2, color.BLACK, "DOG")
        self.__choseCat.text(font.H2, color.BLACK, "CAT")
        
        self.__infoActive = False
        
        # scroll sidebar
        self.__hoverBreed = ""
        self.__chosenBreed = ""

        # body
        self.__imageSize = 0
        self.__sidebarWidth = 270
        self.__imageSurfaces = []
        self.__choseBreedText = text(display, font.FONT100, (0, 0))
        self.__searchButton = button(screenWidth - 280, 50, color.GREY, radius=5) 
        self.__loadingText = text(display, font.customFont(200), (0,0))



    def header(self):
        pygame.draw.rect(display, color.GREEN, pygame.Rect(0, 0, screenWidth, 50))
        
        buttonColor = color.TURQUISE if self.__category == "info" else color.BLUE
        self.__infoButton.text(font.H2, color.BLACK, f"{self.__selection} info")
        self.__infoButton.place(display, events, (screenWidth / 2 - 190, 5))
        self.__infoButton.changeColorOnHover(buttonColor, color.LIGHTBLUE)
        if self.__infoButton.onClick():
            self.__category = "info"
            self.__sidebarWidth = 270
        
        buttonColor = color.TURQUISE if self.__category == "images" else color.BLUE
        self.__imageButton.text(font.H2, color.BLACK, f"{self.__selection} images")
        self.__imageButton.place(display, events, (screenWidth / 2 - 60, 5))
        self.__imageButton.changeColorOnHover(buttonColor, color.LIGHTBLUE)
        if self.__imageButton.onClick():
            self.__category = "images"
            self.__sidebarWidth = 0
            self.__infoActive = False
        
        buttonColor = color.TURQUISE if self.__category == "game" else color.BLUE
        self.__gameButton.text(font.H2, color.BLACK, "game")
        self.__gameButton.place(display, events, (screenWidth / 2 + 70, 5))
        self.__gameButton.changeColorOnHover(buttonColor, color.LIGHTBLUE)
        if self.__gameButton.onClick():
            self.__category = "game"
            self.__sidebarWidth = 0
            self.__infoActive = False
        
        self.__quitButton.repostion(screenWidth - 50, 5)
        self.__quitButton.place(events, screenWidth)


    def sidebar(self):
        self.__choseDog.place(display, events, (10, 5))
        self.__choseDog.changeColorOnHover(color.ORANGE, color.RED)
        if self.__choseDog.onClick():
            self.__infoActive = False
            self.__breeds = loadBreed(DOGBREEDS)
            self.__selection = "dog"
            scrollCounter[0] = 0
            self.__hoverBreed = ""
            self.__chosenBreed = ""

        
        self.__choseCat.place(display, events, (140, 5))
        self.__choseCat.changeColorOnHover(color.ORANGE, color.RED)
        if self.__choseCat.onClick():
            self.__infoActive = False
            self.__breeds = loadBreed(CATBREEDS)
            self.__selection = "cat"
            scrollCounter[0] = 0
            self.__hoverBreed = ""
            self.__chosenBreed = ""

            

    def scrollsidebar(self):
        if self.__category == "info":
            global scrollType
            if rectDetection(display, 0, 50, self.__sidebarWidth, screenHeight - 50, color.GREY):
                scrollType = 0
            else:
                self.__hoverBreed = ""
            spacing = 0
            for breed in self.__breeds["breeds"]:
                Color = color.YELLOW if self.__hoverBreed == breed else color.DARKGREEN
                textColor = color.BLACK if self.__hoverBreed == breed else color.WHITE
                if self.__chosenBreed == breed:
                    Color = color.RED
                    textColor = color.BLACK
                if simpleButton(display, 5, 55 + spacing + scrollCounter[0], 260, 40, font.H3, breed, textColor=textColor, buttonColor=Color, radius=5):
                    self.__hoverBreed = breed
                    if action["mouseButtonClicked"]:
                        self.__chosenBreed = breed
                
                spacing += 45


    def body(self):
        global scrollType, imageSize
        if rectDetection(display, self.__sidebarWidth, 50, screenWidth - self.__sidebarWidth, screenHeight - 50, color.WHITE):
            scrollType = 1
        if self.__chosenBreed == "" and self.__category == "info":
            self.__choseBreedText.centerdText((self.__sidebarWidth, screenWidth, 50, screenHeight))
            self.__choseBreedText.place(color.BLACK, f"choose a {self.__selection}")
        else:
            self.__searchButton.resize(screenWidth - (self.__sidebarWidth + 10), 50, 5)
            self.__searchButton.text(font.H1, color.BLACK, "SEARCH")
            self.__searchButton.changeColorOnHover(color.GREY, color.LESSWHITE)
            self.__searchButton.place(display, events, (self.__sidebarWidth + 5, 55))
            if self.__searchButton.onClick():
                self.__loadingText.centerdText((self.__sidebarWidth, screenWidth, 50, screenHeight))
                self.__loadingText.place(color.random(), "loading...")
                pygame.display.flip() # bij het ophalen van de info blijft het scherm tijdelijk hangen
                # zolang hij dus aan het laden is zal de text op het scherm blijven staan
                
                self.__imageSurfaces = []
                self.__breedID = self.__breeds["breeds"][self.__chosenBreed]
                infoTab = get(self.__breedID, self.__selection, savefile["maxInfoPictures"]) # om het laden makkelijker te maken limiteer ik de foto's tot 5
                print(self.__breedID, self.__selection)
                
                self.__breedInfo = infoTab.getInfo()
                infoTab.getImages()
                print(infoTab.imageAmount)
                
                for image in range(infoTab.imageAmount):
                    self.__imageSurfaces.append(infoTab.showImage(image))
                print(self.__imageSurfaces)
                self.__imageBackButton = button(infoTab.imageSize / 2 - 3, 50, color.RED, 5)
                self.__imageForwardButton = button(infoTab.imageSize / 2 - 3, 50, color.GREEN, 5)
                imageSize = infoTab.imageSize
                self.__imageAmount = infoTab.imageAmount
                self.__infoActive = True
                self.__imageCounter = 0
                
                # text voor onder de foto
                self.__name = text(display, font.FONT50, (0,0))
                self.__origin = text(display, font.H1, (0,0))
                self.__temperament = text(display, font.H3, (0,0))
    
    def updateImageSizes(self):
        if screenHeight >= 700:
            self.____updateImageSizes__(screenHeight)
        else:
            self.____updateImageSizes__(700)
    
    def __updateImageSizes__(self, screenHeight):
        for index, image in enumerate(self.__imageSurfaces):
            self.__imageSurfaces[index] = pygame.transform.smoothscale(image, (screenHeight / 2, screenHeight / 2))
        self.__imageBackButton.resize(screenHeight / 4 - 3, 50, 5)
        self.__imageForwardButton.resize(screenHeight / 4 - 3, 50, 5)  

    def info(self):
        # foto
        if self.__infoActive:
            self.__imageBackButton.text(font.H1, color.BLACK, "<")
            if self.__imageCounter > 0:
                self.__imageBackButton.changeColorOnHover(color.GREEN, (0,200,0))
            else:
                self.__imageBackButton.recolor(color.RED)
                
            self.__imageBackButton.place(display, events, (280, screenHeight / 2 + 120))
            if self.__imageBackButton.onClick():
                if self.__imageCounter > 0:
                    self.__imageCounter -= 1
            
            self.__imageForwardButton.text(font.H1, color.BLACK, ">")
            if self.__imageCounter < self.__imageAmount - 1:
                self.__imageForwardButton.changeColorOnHover(color.GREEN, (0,200,0))
            else:
                self.__imageForwardButton.recolor(color.RED)
            self.__imageForwardButton.place(display, events, (screenHeight / 4 + 3 + 280, screenHeight / 2 + 120))
            if self.__imageForwardButton.onClick():
                if self.__imageCounter < self.__imageAmount - 1:
                    self.__imageCounter += 1
                    
         
            display.blit(self.__imageSurfaces[self.__imageCounter], (280, 115))
        
            # onder foto
            self.__name.centerdText((270, 270 + screenHeight / 2, screenHeight / 2 + 180, screenHeight / 2 + 200))
            self.__name.place(color.BLACK, self.__breedInfo["name"])
            
            self.__origin.centerdText((270, 270 + screenHeight / 2, screenHeight / 2 + 210, screenHeight / 2 + 230))
            self.__origin.place(color.DARKGRAY, self.__breedInfo["origin"])
            
            self.__temperament.centerdText((270, 270 + screenHeight / 2, screenHeight / 2 + 230, screenHeight / 2 + 245))
            self.__temperament.place(color.GRAY, self.__breedInfo["temperament"])
        
    @property
    def breedHeight(self):
        return self.__breeds["height"]

APP = app() 

while True:
    clock.tick(60)
    display.fill(color.WHITE)
    display, temp = windowMinSize(display, 1400, 700, pygame.RESIZABLE)
    events = pygame.event.get()
    screenWidth, screenHeight = windowInfo()
    
    APP.scrollsidebar()
    APP.header()
    APP.sidebar()
    APP.body()
    
    APP.info()

    
    if scrollCounter[0] < maxSidebarScroll:
        scrollCounter[0] = maxSidebarScroll
    screenNotUsed = displayH - screenHeight
    maxSidebarScroll = APP.breedHeight - screenNotUsed + 50
    
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEWHEEL:
            scroll(event.y, maxSidebarScroll)
        if event.type == pygame.MOUSEBUTTONDOWN:
            action["mouseButtonClicked"] = True
        if event.type == pygame.MOUSEBUTTONUP:
            action["mouseButtonClicked"] = False
        if event.type == pygame.WINDOWRESIZED:
            APP.updateImageSizes()    


    
    
    pygame.display.flip()