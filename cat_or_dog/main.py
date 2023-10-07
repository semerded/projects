import pygame, requests, json, random
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
    def __init__(self, breedID :str = "", selection: str = "", category: str = "", amount: int = 1) -> None:
        self.__breedID = breedID
        self.__selection = selection
        self.__amount = amount
        self.__category = category
    
    def getInfo(self): # krijg de info van het geselecteerde ras
        BreedURL = f"https://api.the{self.__selection}api.com/v1/breeds/{self.__breedID}"
        self.__breedInfo = requests.get(BreedURL).json()
        return self.__breedInfo
    
    def getImages(self): # krijg foto's van het geselecteerde ras
        
        # klaarmaken van url
        apikey = self.__getAPIkey__()
        BreedImageURL = f"https://api.the{self.__selection}api.com/v1/images/search?limit={self.__amount}&api_key={apikey}"
        print(BreedImageURL)
        if self.__category == "info":
            BreedImageURL += f"&breed_ids={self.__breedID}"
            
        # api oproepen
        self.__breedImage = requests.get(BreedImageURL).json()
        self.__imageList = []
        self.__originalImageSurface = []
        
        # elke foto omzetten naar leesbare data voor pygame
        for image in range(len(self.__breedImage)):
            req = Request(
                        url=self.__breedImage[image]["url"], 
                        headers={'User-Agent': 'Mozilla/5.0'})
            imageString = urlopen(req).read()
            imageFile = BytesIO(imageString)
            pyimage = pygame.image.load(imageFile)
            originalSurface = pyimage
            self.__imageSize = screenHeight / 2
            try:
                pyimage = pygame.transform.smoothscale(pyimage, (self.__imageSize, self.__imageSize)) # de afbeelding wordt automatisch geschaald
            except ValueError:
                continue
            
            self.__originalImageSurface.append(originalSurface)
            self.__imageList.append(pyimage)
        return self.__imageList, self.__originalImageSurface # geef de lijst met data terug
    
    
    def __getAPIkey__(self): # maak de api key klaar
        if self.__selection == "cat":
            updateCalls(False, True)
            return CATAPIKEY
        elif self.__selection == "dog":
            updateCalls(True, False)
            return DOGAPIKEY
        else:
            raise ValueError("selection was not a cat or dog")
        
    @property
    def imageAmount(self): # geeft het aantal foto's terug
        return len(self.__imageList)
    
    @property
    def imageSize(self): # geeft de grote de afbeeldingen terug
        return self.__imageSize
        
    
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
        self.__allImages = True

        # categorieën
        self.__imagesActive = False
        self.__infoActive = False
        self.__gameActive = False
        
    
    def __closeBigImage__(self):
        self.__allImages = True
        
    def __getGameImages__(self): # TODO fix als er geen foto opgehaald wordt
        self.__imageSurfaces = []
        while True:
            dogImage, temp = self.__GameDogImage.getImages()
            if dogImage != []:
                break
        while True:
            catImage, temp = self.__GameCatImage.getImages()
            if catImage != []:
                break
        self.__imageSurfaces.append(dogImage[0])
        self.__imageSurfaces.append(catImage[0])
        
    def __hpHandeler__(self, hpdifference):
        self.__hp += hpdifference
        if self.__hp <= 0:
            ...
        
    def __getGameEvent__(self, animal):
        EVENTS = {
            "cat": {
                "you've been scrached by the cat": -30, 
                "the cat liked you but he didn't let you pet him": -5,
                "the cat was scared and ran away": -10,
                "the cat was angry and attacked you": -25, 
                "you got a disease from the cat": -99,
                "the cat liked you": 10,
                "the cat loved you": 30,
                "the cat wanted to be adopted": 99,
                "the cat wanted to be pet": 20, 
                "ultimate scratch attack": -50,
                "the cat was possessed by satan": -66,
                "the cat turned around twice": 2,
                "the cat turned around once": 1,
                "the cat pooped": -10,
                "the cat did a cat thing": 3,
                "the cat licked you": 20,
                "the cat hissed": -3,
                "paw to face": -20,
                "meawwww": 4,
                
            },
            "dog": {
                "the dog wanted a pet": 15,
                "the dog was a good boy": 5,
                "nothing happend": 0,
                "the dog was a bad boy": -5,
                "the dog peed on your shoes": -10,
                "the dog peed on your shoes but you liked it (weird)": 10,
                "the dog shit on the floor": -15,
                "the dog attacked": -25,
                "the dog was a government spy": -40,
                "the dog liked you": 10,
                "the dog liked you a bit more": 15,
                "the dog licked you": 20,
                "the dog had rabies": -99,
                "the dog killed you": -999,
                "the dog bit your finger of": -35,
                "the dog bit your leg of": -50,
                "the dog bit you in your nutsack": -98,
                "the dog licked your hand": 15,
                "the dog did nothing": 0,
                "the dog ran away": -5,
                "the dog started humping your leg": -10,
                "the dog barked": -3,
                "the dog had dirty paws and made your white pants dirty": -13,
                "bark bark": -5,
                "arf arf (knocked loose refference)": 5,
            }
           
        }
        
        
        # hp handeler
        
    def header(self):
        # header achtergrond
        pygame.draw.rect(display, color.GREEN, pygame.Rect(0, 0, screenWidth, 50))
        
        # knop kies info categorie
        buttonColor = color.TURQUISE if self.__category == "info" else color.BLUE
        self.__infoButton.text(font.H2, color.BLACK, f"{self.__selection} info")
        self.__infoButton.place(display, events, (screenWidth / 2 - 190, 5))
        self.__infoButton.changeColorOnHover(buttonColor, color.LIGHTBLUE)
        
        if self.__infoButton.onClick():
            self.__category = "info"
            self.__sidebarWidth = 270
            self.__imagesActive = False
            self.__gameActive = False
            
            
            
        # knop kies images categorie
        buttonColor = color.TURQUISE if self.__category == "images" else color.BLUE
        self.__imageButton.text(font.H2, color.BLACK, f"{self.__selection} images")
        self.__imageButton.place(display, events, (screenWidth / 2 - 60, 5))
        self.__imageButton.changeColorOnHover(buttonColor, color.LIGHTBLUE)
        
        if self.__imageButton.onClick():
            self.__category = "images"
            self.__sidebarWidth = 0
            self.__infoActive = False
            self.__gameActive = False
        
        # knop kies game categorie
        buttonColor = color.TURQUISE if self.__category == "game" else color.BLUE
        self.__gameButton.text(font.H2, color.BLACK, "game")
        self.__gameButton.place(display, events, (screenWidth / 2 + 70, 5))
        self.__gameButton.changeColorOnHover(buttonColor, color.LIGHTBLUE)
        
        if self.__gameButton.onClick():
            self.__category = "game"
            self.__sidebarWidth = 0
            self.__infoActive = False
            self.__imagesActive = False

        
        # exit knop
        self.__quitButton.repostion(screenWidth - 50, 5)
        self.__quitButton.place(events, screenWidth)
        
        if self.__category != "game":
        
            # knop kies hond
            self.__choseDog.place(display, events, (10, 5))
            self.__choseDog.changeColorOnHover(color.ORANGE, color.RED)
            if self.__choseDog.onClick():
                self.__infoActive = False
                self.__breeds = loadBreed(DOGBREEDS)
                self.__selection = "dog"
                scrollCounter[0] = 0
                self.__hoverBreed = ""
                self.__chosenBreed = ""

            # knop kies kat
            self.__choseCat.place(display, events, (140, 5))
            self.__choseCat.changeColorOnHover(color.ORANGE, color.RED)
            if self.__choseCat.onClick():
                self.__infoActive = False
                self.__breeds = loadBreed(CATBREEDS)
                self.__selection = "cat"
                scrollCounter[0] = 0
                self.__hoverBreed = ""
                self.__chosenBreed = ""



    def sidebar(self):
        # alleen actief als categorie info actief is
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
            self.__choseBreedText.centerd(self.__sidebarWidth, screenWidth, 50, screenHeight)
            self.__choseBreedText.place(color.BLACK, f"choose a {self.__selection}")
        elif self.__allImages and self.__category != "game":
            self.__searchButton.resize(screenWidth - (self.__sidebarWidth + 10), 50, 5)
            self.__searchButton.text(font.H1, color.BLACK, "SEARCH")
            self.__searchButton.changeColorOnHover(color.GREY, color.LESSWHITE)
            self.__searchButton.place(display, events, (self.__sidebarWidth + 5, 55))
            if self.__searchButton.onClick(actionOnRelease=True):
                self.__loadingText.centerd(self.__sidebarWidth, screenWidth, 50, screenHeight)
                self.__loadingText.place(color.random(), "loading...")
                pygame.display.flip() # bij het ophalen van de info blijft het scherm tijdelijk hangen
                # zolang hij dus aan het laden is zal de text op het scherm blijven staan
                
                self.__imageSurfaces = []
                
                if self.__category == "info":
                    self.__breedID = self.__breeds["breeds"][self.__chosenBreed]
                    infoTab = get(self.__breedID, self.__selection, self.__category, savefile["maxInfoPictures"]) # om het laden makkelijker te maken limiteer ik de foto's tot 5

                    # roep de info op van de api's            
                    self.__breedInfo = infoTab.getInfo()
                    self.__imageSurfaces, temp = infoTab.getImages()
    
                    # knoppen toevoegen
                    self.__imageBackButton = button(infoTab.imageSize / 2 - 3, 50, color.RED, 5)
                    self.__imageForwardButton = button(infoTab.imageSize / 2 - 3, 50, color.GREEN, 5)
                    imageSize = infoTab.imageSize
                    self.__imageAmount = infoTab.imageAmount
                    self.__infoActive = True
                    self.__imageCounter = 0
                
                    # text voor onder de foto
                    self.__name = text(display, font.FONT50, (0,0))
                    self.__origin = text(display, font.H1, (0,0))
                    self.__temperament = textbox(display, font.H3, (0,0))
                
                if self.__category == "images":
                    imageTab = get(selection=self.__selection, category=self.__category, amount=8)
                    self.__imageSurfaces, self.__originalImageSize = imageTab.getImages()
                    
                    self.__imageAmount = imageTab.imageAmount
                    self.__imagesActive = True
                    self.updateImageSize()  
                
               
                    
        elif self.__category == "game" and not self.__gameActive:
            
            self.__GameDogImage = get(selection="dog")
            self.__GameCatImage = get(selection="cat")
            self.__getGameImages__()
            
            self.__GamePetDogButton = button(0,0, color.BLUE, radius=5)
            self.__GamePetDogButton.text(font.H1, color.BLACK, "pet the dog")
            self.__GamePetCatButton = button(0,0, color.BLUE, radius=5)
            self.__GamePetCatButton.text(font.H1, color.BLACK, "pet the cat")
            self.__GameDoNothingButton = button(0, 0, color.RED, radius=5)
            self.__GameDoNothingButton.text(font.H1, color.BLACK, "do nothing")
            
            self.__GameText = text(display, font.FONT150, (0,0))
            
            self.__hp = 100
            self.__gameActive = True
            self.updateImageSize()
            
            

    def apiContent(self):
        """
        hier wordt de content die je terug krijgt van de api verwerkt en geplaatst
        """
        """
        category info
        
        er wordt een kader met een foto getoond
        hieronder komt de algemene info
        hierlangs komt meer info
        """
        if self.__infoActive:
            
            # foto
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
            self.__name.centerdWidth(270, 270 + screenHeight / 2, screenHeight / 2 + 180)
            self.__name.place(color.BLACK, self.__breedInfo["name"])
            
            self.__origin.centerdWidth(270, 270 + screenHeight / 2, screenHeight / 2 + 220)
            try:
                origin = self.__breedInfo["origin"]
            except KeyError:
                origin = "Unknown"
            self.__origin.place(color.DARKGRAY, origin)
            
            self.__temperament.reposition(275, screenHeight / 2 + 250)
            self.__temperament.place(screenHeight / 2 - 10, color.GRAY, self.__breedInfo["temperament"], True)
        
        
        """
        category images
        
        er worden 8* foto's getoond
        
            * alleen 24 en 32 bit foto's worden getoond, sommige doorgekregen foto's voldoen daar niet aan
                Hierdoor worden er soms minder foto's getoond
        """   
        if self.__imagesActive:
            if self.__allImages:
                for image in range(self.__imageAmount):
                    y = 110 if image < 4 else (screenHeight + 110) / 2
                    x = image * screenWidth / 4 + 3 if image < 4 else (image - 4) * screenWidth / 4 + 3
                    
                    imageRect = display.blit(self.__imageSurfaces[image], (x + 6, y + 3))
                    mousePos = pygame.mouse.get_pos()
                    if imageRect.collidepoint(mousePos) and action["mouseButtonClicked"]:
                        # laat foto in het groot zien
                        display.fill(color.WHITE)
                        self.__bigImageSize = self.__originalImageSize[image]
                        self.__allImages = False
                        
                        self._bigImageWidth, self.__bigImageHeight = pygame.Surface.get_size(self.__bigImageSize)
                        self.__quitBigImage = Xbutton(display, self.__closeBigImage__)
            else:
                scaleFactor = (screenHeight - 150) / self.__bigImageHeight # elke frame scalen

                bigImage = pygame.transform.scale_by(self.__bigImageSize, scaleFactor)
                pygame.draw.rect(display, color.BLACK, pygame.Rect(screenWidth / 2 - bigImage.get_width() / 2 - 10, screenHeight / 2 - bigImage.get_height() / 2 - 10, bigImage.get_width() + 20, bigImage.get_height() + 20), border_radius= 10)
                display.blit(bigImage, (screenWidth / 2 - bigImage.get_width() / 2, screenHeight / 2 - bigImage.get_height() / 2))  
                self.__quitBigImage.repostion(screenWidth / 2 + bigImage.get_width() / 2 - 30, screenHeight / 2 - bigImage.get_height() / 2)
                self.__quitBigImage.place(events, 0)

        
        """
        category game
        
        
        """
        if self.__gameActive:
            # toon hondenfoto / knop
            xPos = screenWidth - 50 - self.__imageSurfaces[0].get_width()
            buttonYpos = screenHeight / 2 + self.__imageSurfaces[0].get_height() / 2 + 10
            display.blit(self.__imageSurfaces[0], (xPos, screenHeight / 2 - self.__imageSurfaces[0].get_height() / 2)) 
            
            self.__GamePetDogButton.changeColorOnHover(color.DARKGREEN, color.GREEN)
            self.__GamePetDogButton.place(display, events, (xPos, buttonYpos))
            if self.__GamePetDogButton.onClick():
                self.__getGameEvent__("dog")
            
            # toon kattenfoto / knop
            display.blit(self.__imageSurfaces[1], (50, screenHeight / 2 - self.__imageSurfaces[1].get_height() / 2)) 
            
            self.__GamePetCatButton.changeColorOnHover(color.DARKGREEN, color.GREEN)
            self.__GamePetCatButton.place(display, events, (50, buttonYpos))
            if self.__GamePetCatButton.onClick():
                self.__getGameEvent__("cat")
                
            # doe niets
            self.__GameDoNothingButton.changeColorOnHover(color.RED, color.LESSRED)
            self.__GameDoNothingButton.place(display, events, (screenWidth / 2 - (screenWidth / 2 - (50 + self.__imageSurfaces[0].get_width())) + 5, buttonYpos))
            if self.__GameDoNothingButton.onClick():
                self.__hpHandeler__(-random.randint(5, 10))
                print(self.__hp)
                self.__getGameImages__()
                self.updateImageSize()
                
            
            
    
    """
    om de foto's en knoppen de juiste schaal te houden worden ze bij elke verandering geresized
    
    """
    def updateImageSize(self):
        x = 1400 if screenWidth < 1400 else screenWidth
        y = 700 if screenHeight < 700 else screenHeight
        
        if self.__category == "info":
            self.__updateImageSizes__(y / 2, y / 2)
            
        elif self.__category == "images":
            self.__updateImageSizes__((x - 110) / 4 - 6, (y - 110) / 2 - 6)
        
        elif self.__category == "game":
            self.__updateImageSizes__(y / 1.4, y / 1.4)
            
    
    def __updateImageSizes__(self, xcord, ycord):
        for index, image in enumerate(self.__imageSurfaces):
            self.__imageSurfaces[index] = pygame.transform.smoothscale(image, (xcord, ycord))
            
        if self.__category == "info" and self.__breedID != "":
            self.__imageBackButton.resize(screenHeight / 4 - 3, 50, 5)
            self.__imageForwardButton.resize(screenHeight / 4 - 3, 50, 5) 
            
        elif self.__category == "game"  and self.__gameActive:
            self.__GamePetDogButton.resize(self.__imageSurfaces[1].get_width(), 50, 5)
            self.__GamePetCatButton.resize(self.__imageSurfaces[0].get_width(), 50, 5)
            self.__GameDoNothingButton.resize(screenWidth - self.__imageSurfaces[0].get_width() * 2 - 110, 50, 5)
            
        
        
    @property
    def breedHeight(self):
        return self.__breeds["height"]
        
    

APP = app() # maak app aan

while True:
    clock.tick(60)
    display.fill(color.WHITE)
    display, temp = windowMinSize(display, 1400, 700, pygame.RESIZABLE)
    events = pygame.event.get()
    screenWidth, screenHeight = windowInfo()
    
    
    APP.sidebar()
    APP.header()
    APP.body()
    APP.apiContent()
    
    
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
            APP.updateImageSize()    


    
    
    pygame.display.flip()