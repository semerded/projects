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

class get:
    def __init__(self, breedID :str = "", selection: str = "", amount: int = 0) -> None:
        self.breedID = breedID
        self.selection = selection
        self.amount = amount
    
    def getInfo(self):
        BreedURL = f"https://api.the{self.selection}api.com/v1/breeds/{self.breedID}"
        self.breedInfo = requests.get(BreedURL).json()
        return self.breedInfo
    
    def getImages(self):
        apikey = self.__getAPIkey__()
        BreedImageURL = f"https://api.the{self.selection}api.com/v1/images/search?limit={self.amount}&breed_ids={self.breedID}&api_key={apikey}"
        self.breedImage = requests.get(BreedImageURL).json()
        return self.breedImage
    
    def showImage(self, imageNumber):
        req = Request(
            url=self.breedImage[imageNumber]["url"], 
            headers={'User-Agent': 'Mozilla/5.0'})
        imageString = urlopen(req).read()
        imageFile = BytesIO(imageString)
        pyimage = pygame.image.load(imageFile)
        self._imageSize = screenHeight / 2
        pyimage = pygame.transform.smoothscale(pyimage, (self._imageSize, self._imageSize))
        return pyimage
    
    def __getAPIkey__(self):
        if self.selection == "cat":
            updateCalls(False, True)
            return CATAPIKEY
        elif self.selection == "dog":
            updateCalls(True, False)
            return DOGAPIKEY
        else:
            raise ValueError("selection was not a cat or dog")
    @property
    def imageAmount(self):
        return len(self.breedImage)
    
    @property
    def imageSize(self):
        return self._imageSize
        
        
        
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
        self.breedID = ""
        self.selection = "cat"
        # header
        self.infoButton = button(120, 40, color.BLUE, 5)
        self.imageButton = button(120, 40, color.BLUE, 5)
        self.gameButton = button(120, 40, color.BLUE, 5)
        self.quitButton = Xbutton(display, size= 40)
        self.category = "info"
        
        # sidebar
        self.breeds = loadBreed(CATBREEDS)

        self.choseDog = button(120, 40, color.ORANGE, 5)
        self.choseCat = button(120, 40, color.ORANGE, 5)    
        self.choseDog.text(font.H2, color.BLACK, "DOG")
        self.choseCat.text(font.H2, color.BLACK, "CAT")
        
        self.infoActive = False
        
        # scroll sidebar
        self.hoverBreed = ""
        self.chosenBreed = ""

        # body
        self.imageSize = 0
        self.sidebarWidth = 270
        self.imageSurfaces = []
        self.choseBreedText = text(display, font.FONT100, (0, 0))
        self.searchButton = button(screenWidth - 280, 50, color.GREY, radius=5) 
        self.loadingText = text(display, font.customFont(200), (0,0))



    def header(self):
        pygame.draw.rect(display, color.GREEN, pygame.Rect(0, 0, screenWidth, 50))
        
        buttonColor = color.TURQUISE if self.category == "info" else color.BLUE
        self.infoButton.text(font.H2, color.BLACK, f"{self.selection} info")
        self.infoButton.place(display, events, (screenWidth / 2 - 190, 5))
        self.infoButton.changeColorOnHover(buttonColor, color.LIGHTBLUE)
        if self.infoButton.onClick():
            self.category = "info"
            self.sidebarWidth = 270
        
        buttonColor = color.TURQUISE if self.category == "images" else color.BLUE
        self.imageButton.text(font.H2, color.BLACK, f"{self.selection} images")
        self.imageButton.place(display, events, (screenWidth / 2 - 60, 5))
        self.imageButton.changeColorOnHover(buttonColor, color.LIGHTBLUE)
        if self.imageButton.onClick():
            self.category = "images"
            self.sidebarWidth = 0
            self.infoActive = False
        
        buttonColor = color.TURQUISE if self.category == "game" else color.BLUE
        self.gameButton.text(font.H2, color.BLACK, "game")
        self.gameButton.place(display, events, (screenWidth / 2 + 70, 5))
        self.gameButton.changeColorOnHover(buttonColor, color.LIGHTBLUE)
        if self.gameButton.onClick():
            self.category = "game"
            self.sidebarWidth = 0
            self.infoActive = False
        
        self.quitButton.repostion(screenWidth - 50, 5)
        self.quitButton.place(events, screenWidth)


    def sidebar(self):
        self.choseDog.place(display, events, (10, 5))
        self.choseDog.changeColorOnHover(color.ORANGE, color.RED)
        if self.choseDog.onClick():
            self.infoActive = False
            self.breeds = loadBreed(DOGBREEDS)
            self.selection = "dog"
            scrollCounter[0] = 0
            self.hoverBreed = ""
            self.chosenBreed = ""

        
        self.choseCat.place(display, events, (140, 5))
        self.choseCat.changeColorOnHover(color.ORANGE, color.RED)
        if self.choseCat.onClick():
            self.infoActive = False
            self.breeds = loadBreed(CATBREEDS)
            self.selection = "cat"
            scrollCounter[0] = 0
            self.hoverBreed = ""
            self.chosenBreed = ""

            

    def scrollsidebar(self):
        if self.category == "info":
            global scrollType
            if rectDetection(display, 0, 50, self.sidebarWidth, screenHeight - 50, color.GREY):
                scrollType = 0
            else:
                self.hoverBreed = ""
            spacing = 0
            for breed in self.breeds["breeds"]:
                Color = color.YELLOW if self.hoverBreed == breed else color.DARKGREEN
                textColor = color.BLACK if self.hoverBreed == breed else color.WHITE
                if self.chosenBreed == breed:
                    Color = color.RED
                    textColor = color.BLACK
                if simpleButton(display, 5, 55 + spacing + scrollCounter[0], 260, 40, font.H3, breed, textColor=textColor, buttonColor=Color, radius=5):
                    self.hoverBreed = breed
                    if action["mouseButtonClicked"]:
                        self.chosenBreed = breed
                
                spacing += 45


    def body(self):
        global scrollType, imageSize
        if rectDetection(display, self.sidebarWidth, 50, screenWidth - self.sidebarWidth, screenHeight - 50, color.WHITE):
            scrollType = 1
        if self.chosenBreed == "" and self.category == "info":
            self.choseBreedText.centerdText((self.sidebarWidth, screenWidth, 50, screenHeight))
            self.choseBreedText.place(color.BLACK, f"choose a {self.selection}")
        else:
            self.searchButton.resize(screenWidth - (self.sidebarWidth + 10), 50, 5)
            self.searchButton.text(font.H1, color.BLACK, "SEARCH")
            self.searchButton.changeColorOnHover(color.GREY, color.LESSWHITE)
            self.searchButton.place(display, events, (self.sidebarWidth + 5, 55))
            if self.searchButton.onClick():
                self.loadingText.centerdText((self.sidebarWidth, screenWidth, 50, screenHeight))
                self.loadingText.place(color.random(), "loading...")
                pygame.display.flip() # bij het ophalen van de info blijft het scherm tijdelijk hangen
                # zolang hij dus aan het laden is zal de text op het scherm blijven staan
                
                self.imageSurfaces = []
                self.breedID = self.breeds["breeds"][self.chosenBreed]
                infoTab = get(self.breedID, self.selection, savefile["maxInfoPictures"]) # om het laden makkelijker te maken limiteer ik de foto's tot 5
                print(self.breedID, self.selection)
                
                self.breedInfo = infoTab.getInfo()
                infoTab.getImages()
                print(infoTab.imageAmount)
                
                for image in range(infoTab.imageAmount):
                    self.imageSurfaces.append(infoTab.showImage(image))
                print(self.imageSurfaces)
                self.imageBackButton = button(infoTab.imageSize / 2 - 3, 50, color.RED, 5)
                self.imageForwardButton = button(infoTab.imageSize / 2 - 3, 50, color.GREEN, 5)
                imageSize = infoTab.imageSize
                self.imageAmount = infoTab.imageAmount
                self.infoActive = True
                self.imageCounter = 0
                
                # text voor onder de foto
                self.name = text(display, font.FONT50, (0,0))
                self.origin = text(display, font.H1, (0,0))
                self.temperament = text(display, font.H3, (0,0))
    
    def updateImageSizes(self):
        if screenHeight >= 700:
            self.__updateImageSizes__(screenHeight)
        else:
            self.__updateImageSizes__(700)
    
    def __updateImageSizes__(self, screenHeight):
        for index, image in enumerate(self.imageSurfaces):
            self.imageSurfaces[index] = pygame.transform.smoothscale(image, (screenHeight / 2, screenHeight / 2))
        self.imageBackButton.resize(screenHeight / 4 - 3, 50, 5)
        self.imageForwardButton.resize(screenHeight / 4 - 3, 50, 5)  

    def info(self):
        # foto
        if self.infoActive:
            self.imageBackButton.text(font.H1, color.BLACK, "<")
            if self.imageCounter > 0:
                self.imageBackButton.changeColorOnHover(color.GREEN, (0,200,0))
            else:
                self.imageBackButton.recolor(color.RED)
                
            self.imageBackButton.place(display, events, (280, screenHeight / 2 + 120))
            if self.imageBackButton.onClick():
                if self.imageCounter > 0:
                    self.imageCounter -= 1
            
            self.imageForwardButton.text(font.H1, color.BLACK, ">")
            if self.imageCounter < self.imageAmount - 1:
                self.imageForwardButton.changeColorOnHover(color.GREEN, (0,200,0))
            else:
                self.imageForwardButton.recolor(color.RED)
            self.imageForwardButton.place(display, events, (screenHeight / 4 + 3 + 280, screenHeight / 2 + 120))
            if self.imageForwardButton.onClick():
                if self.imageCounter < self.imageAmount - 1:
                    self.imageCounter += 1
                    
         
            display.blit(self.imageSurfaces[self.imageCounter], (280, 115))
        
            # onder foto
            self.name.centerdText((270, 270 + screenHeight / 2, screenHeight / 2 + 180, screenHeight / 2 + 200))
            self.name.place(color.BLACK, self.breedInfo["name"])
            
            self.origin.centerdText((270, 270 + screenHeight / 2, screenHeight / 2 + 210, screenHeight / 2 + 230))
            self.origin.place(color.DARKGRAY, self.breedInfo["origin"])
            
            self.temperament.centerdText((270, 270 + screenHeight / 2, screenHeight / 2 + 230, screenHeight / 2 + 245))
            self.temperament.place(color.GRAY, self.breedInfo["temperament"])
        
    @property
    def breedHeight(self):
        return self.breeds["height"]

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