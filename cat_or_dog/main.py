import pygame, requests, json, random
from pygameaddons import * # eigen gemaakte library
from os import path
from io import BytesIO
from pyperclip import copy
from urllib.request import urlopen, Request

# api keys voor de api  {NIET AANKOMEN!!!}
CATAPIKEY = "live_Domf0oeKUtUcnVuuRcNS0yVh3BBvTSy9ee9TN9wt3WqupgEpKrb1sBncHhGKnAnW"
DOGAPIKEY = "live_K4sjv4DLuGrrFq5MngAPs06ToR4gEWqN094L04eXNROEQOua6ckkUSyTcFHiLqUw"

JSONSETUPFILE = "setup.json"
CATBREEDS = "catbreed.json"
DOGBREEDS = "dogbreed.json"

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
EVENTS = savefile["events"]

def updateCalls(dog: bool, cat: bool): # update de lijst van apicalls
    # update alleen wat nodig is
    if dog:
        savefile["dogcalls"] -= 1 
    if cat:
        savefile["catcalls"] -= 1
    with open(JSONSETUPFILE, 'w') as json_file: # update bestand
                json.dump(savefile, json_file, indent = 4, separators=(',',': '))

def getFacts(selection): # krijg leuke feitjes tijdens het laden
        if selection == "dog":
            FACTURL = "https://dog-api.kinduff.com/api/facts?number=1" # voor honden
        else:
            FACTURL = "https://catfact.ninja/fact" # voor katten
        try:
            fact = requests.get(FACTURL).json() # haal het feitje op
        except: # mocht er iets misgaan
            return "fact_not_loaded"
            
        # haal het feitje uit de api dict
        if selection == "dog":
            return fact["facts"][0]
        elif selection == "cat":
            return fact["fact"]
        else:
            return "error"

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
        

scrollCounter = [0,0] # origineel zou het programma 2 of meer scrollposities aankunnen maar er is uiteindelijk maar 1 ingebouwd
def scroll(event, maxSidebarScroll): # regel het scrollen voor het programma
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

hier wordt alles voor het visuele programma klaargemaakt
"""
pygame.init()
pygame.display.set_caption("under construction") #TODO
displayW, displayH = windowInfo() # krijg de grote van het scherm van de gebruiker
display = pygame.display.set_mode((displayW - 100, displayH - 100), pygame.RESIZABLE) # stel het scherm in op de grote van de gebruiker 
clock = pygame.time.Clock() # klok om de framerate te bepalen
screenWidth, screenHeight = windowInfo() # krijg de grote van het pygame scherm
HPheartImg = pygame.image.load("heart.png")
HPheartImg = pygame.transform.scale(HPheartImg, (100, 100))
 
maxSidebarScroll = -99999999999999999999999 # ja geen uitleg nodig
action = { # alle acties in een programma 
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
        self.__factButton = button(40, 40, color.DARKGRAY, 5)
        self.factMenu = False
        
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
        self.__sidebarWidth = 270
        self.__imageSurfaces = []
        self.__choseBreedText = text(display, font.FONT100, (0, 0))
        self.__searchButton = button(screenWidth - 280, 50, color.GREY, radius=5) 
        self.__loadingText = text(display, font.customFont(200), (0,0))
        self.__loadingFacts = textbox(display, font.H1, (0,0))
        self.__allImages = True
        self.__fact = None
        
        self.__gameEventText = textbox(display, font.FONT50, (0,0))

        # categorieën
        self.__imagesActive = False
        self.__infoActive = False
        self.__gameActive = False
        
    
    def __closeBigImage__(self): # om de uitvergrote foto te sluiten
        self.__allImages = True
        
    def __getGameImages__(self):
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
        if self.__hp > 0:
            if self.__hp > 100:
                self.__hp = 100
        return hpdifference
        
    def __getGameEvent__(self, animal):            
        event = random.choice(list(EVENTS[animal].keys()))
        hpdifference = self.__hpHandeler__(EVENTS[animal][event])
        if hpdifference > 0:
            hptext = f"you gained {hpdifference}hp"
        elif hpdifference < 0:
            hptext = f"you lost {abs(hpdifference)}hp"
        else:
            hptext = "like nothing really happend"
        self.__showGameText__(f"{event} \n {hptext} \n \n {self.__hp}hp left")
        
        
        
    def __showGameText__(self, text):
        self.__gameEventText.__calcbox__(screenWidth / 2, text)
        pygame.draw.rect(display, color.BLACK, pygame.Rect(screenWidth / 4 - 15,  screenHeight / 4 - 15, screenWidth / 2 + 25, screenHeight / 2 + 25), border_radius=15)
        pygame.draw.rect(display, color.WHITE, pygame.Rect(screenWidth / 4 - 5,  screenHeight / 4 - 5, screenWidth / 2 + 5, screenHeight / 2 + 5), border_radius=5)
        self.__gameEventText.reposition(screenWidth / 4, screenHeight / 2 - self.__gameEventText.boxheight / 2)
        self.__gameEventText.place(screenWidth / 2, color.BLACK, text, True)
        pygame.display.update()
        self.__getGameImages__()
        self.updateImageSize()
        
    
    def __closeFactMenu__(self):
        self.factMenu = False  
    def __showFactAfterLoad__(self):
        if self.__category != "game" and self.__fact != None:
            self.__factButton.text(font.FONT50, color.WHITE, "i")
            self.__factButton.place(display, events, (screenWidth - 100, 5))
            self.__factButton.changeColorOnHover(color.DARKGRAY, color.GRAY)
            if self.__factButton.onClick():
                self.factMenu = True
                self.__factBox = textbox(display, font.H2, (0,0))
                self.__factQuitButton = Xbutton(display, self.__closeFactMenu__)
                self.__factBox.__calcbox__(200, self.__fact)

            
            # fact wordt getoond onder api content
                    
            
          
        
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
        
        # als er een fact is gegeven
        self.__showFactAfterLoad__()
        
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
                self.__loadingFacts.reposition(self.__sidebarWidth, screenHeight / 2 + 100)
                
                self.__loadingText.place(color.random(), "loading...")
                self.__fact = getFacts(self.__selection)
                self.factMenu = False
                
                self.__loadingFacts.place(screenWidth - self.__sidebarWidth, color.random(), self.__fact, True)
                pygame.draw.rect(display, color.GREEN, pygame.Rect(screenWidth - 100, 5, 40, 40)) # om de i te verstoppen tijdens het laden
                pygame.display.set_caption("het reageert wel hoor")
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
                    self.__name = textbox(display, font.FONT50, (0,0)) # 0,0 betekent dat de positie later wordt aangepast
                    self.__origin = text(display, font.H1, (0,0))
                    self.__temperament = textbox(display, font.H3, (0,0))
                    
                    # text langs foto
                    self.__description = textbox(display, font.H3, (0,0))
                    self.__weightHeight = textbox(display, font.H1, (0,0))
                    self.__lifespan = text(display, font.H1, (0,0))
                    self.__extraInfo = textbox(display, font.H3, (0,0)) # voor honden is dit "breed_group" en "bred_for", voor katten de sterren
                  
                
                if self.__category == "images":
                    imageTab = get(selection=self.__selection, category=self.__category, amount=8)
                    self.__imageSurfaces, self.__originalImageSize = imageTab.getImages()
                    
                    self.__imageAmount = imageTab.imageAmount
                    self.__imagesActive = True
                    self.updateImageSize()  
                pygame.display.set_caption("the ultimate pet app")
               
                    
        elif self.__category == "game" and not self.__gameActive:
            self.factMenu = False
            
            self.__GameDogImage = get(selection="dog")
            self.__GameCatImage = get(selection="cat")
            self.__getGameImages__()
            
            self.__GamePetDogButton = button(0,0, color.BLUE, radius=5)
            self.__GamePetDogButton.text(font.H1, color.BLACK, "pet the dog")
            self.__GamePetCatButton = button(0,0, color.BLUE, radius=5)
            self.__GamePetCatButton.text(font.H1, color.BLACK, "pet the cat")
            self.__GameDoNothingButton = button(0, 0, color.RED, radius=5)
            self.__GameDoNothingButton.text(font.H1, color.BLACK, "do nothing")
            
            
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

            
            # screenheight / 2 is de afmeting van de foto zijn x en y as
            
            # onder foto
            self.__name.reposition(275, screenHeight / 2 + 180)
            self.__name.place(screenHeight / 2, color.BLACK, self.__breedInfo["name"], True)
            if self.__name.onHover() and action["mouseButtonClicked"]:
                copy(self.__breedInfo["name"]) # wanneer op de naam wordt geklikt word de naam gekopieërd naar het klembord
            self.__origin.centerdWidth(270, 270 + screenHeight / 2, screenHeight / 2 + 190 + self.__name.boxheight)
            try:
                origin = self.__breedInfo["origin"]
            except KeyError:
                origin = "Unknown"
            self.__origin.place(color.DARKGRAY, origin)
            
            self.__temperament.reposition(275, screenHeight / 2 + 220 + self.__name.boxheight)
            self.__temperament.place(screenHeight / 2, color.GRAY, self.__breedInfo["temperament"], True)
        
            # naast foto
            # diverse inhoud maken
            if self.__selection == "cat":
                weightHeight = f"weight: {self.__breedInfo['weight']['metric']}kg"
                description = f""
            elif self.__selection == "dog":
                self.__description.changeFont(font.FONT50)
                weightHeight = f"weight: {self.__breedInfo['weight']['metric']}kg \n height: {self.__breedInfo['height']['metric']}cm"
                description = f"breed group: {self.__breedInfo['breed_group']} \n bred for: {self.__breedInfo['bred_for']}"
            else:
                weightHeight = "None"
                description = "None"
            boxWidth = screenWidth - (screenHeight / 2 + 300)
            self.__weightHeight.reposition(280 + screenHeight / 2, 120)
            
            self.__weightHeight.place(boxWidth, color.BLUE, weightHeight)
            
            self.__lifespan.reposition(280 + screenHeight / 2, 120 + self.__weightHeight.boxheight)
            self.__lifespan.place(color.LIGHTBLUE, self.__breedInfo['life_span'])
            
            self.__description.reposition(280 + screenHeight / 2, 140 + self.__weightHeight.boxheight)
            
            self.__description.place(boxWidth, color.BLACK, description)
            
        """
        category images
        
        er worden 8* foto's getoond
        
            * alleen 24 en 32 bit foto's worden getoond, sommige doorgekregen foto's voldoen daar niet aan
                Hierdoor worden er soms minder foto's getoond
        
        de foto's kunnen vergroot worden door er op te klikken
        zo krijg je wel de foto te zien in zijn originele afmetingen
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
        
        het spel is opgebouwd uit 2 foto's en 3 knoppen
        je kunt kiezen om de hond of de kat te aaien
        hierbij wordt een random event getoond en de hierbij horende levens opgeteld of afgetrokken
        je kunt ook kiezen om niks te doen maar dan verlies je zoizo levens
        het is niet compitetief bedoeld, gewoon voor de fun
        """
        if self.__gameActive:
            # toon hondenfoto / knop
            xPos = screenWidth - 50 - self.__imageSurfaces[0].get_width()
            buttonYpos = screenHeight / 2 + self.__imageSurfaces[0].get_height() / 2 + 10
            display.blit(self.__imageSurfaces[0], (xPos, screenHeight / 2 - self.__imageSurfaces[0].get_height() / 2)) 
            
            self.__GamePetDogButton.changeColorOnHover(color.DARKGREEN, color.GREEN)
            self.__GamePetDogButton.place(display, events, (xPos, buttonYpos))
           
            
            # toon kattenfoto / knop
            display.blit(self.__imageSurfaces[1], (50, screenHeight / 2 - self.__imageSurfaces[1].get_height() / 2)) 
            
            self.__GamePetCatButton.changeColorOnHover(color.DARKGREEN, color.GREEN)
            self.__GamePetCatButton.place(display, events, (50, buttonYpos))
            
             
            whitespace = screenWidth / 2 - (screenWidth / 2 - (50 + self.__imageSurfaces[0].get_width()))
            # doe niets
            self.__GameDoNothingButton.changeColorOnHover(color.RED, color.LESSRED)
            self.__GameDoNothingButton.place(display, events, (whitespace + 5, buttonYpos))
            
            """
            eerst wordt alles gerenderd voordat de knoppen worden gelezen
            dit om te voorkomen dat een foto verdwijnt
            """
            if self.__hp <= 0:
                self.__showGameText__("game over")
            elif self.__GamePetDogButton.onClick():
                self.__getGameEvent__("dog")
                
            elif self.__GamePetCatButton.onClick():
                self.__getGameEvent__("cat")
                
            elif self.__GameDoNothingButton.onClick():
                hp = -random.randint(5, 10)
                diff = self.__hp + hp
                hpdifference = self.__hpHandeler__(hp)
                self.__showGameText__(f"you did nothing \n you lost {abs(hpdifference)} \n \n %shp left" % diff)
            else:
            
                # toon hp
                display.blit(HPheartImg, (whitespace, screenHeight / 2 - 50))
                simpleText(display, font.customFont(120), (whitespace + 100, screenHeight / 2 - 40), color.RED, self.__hp)   
                
        
        """
        tijdens het laden wordt er een feitje getoond
        als je niet de tijd kreeg om dit feitje te lezen kun je hem altijd nog een keer zien
        """
        if self.factMenu:
            # toon fact onder aan scherm
            pygame.draw.rect(display, color.BLACK, pygame.Rect(screenWidth - 225, screenHeight - self.__factBox.boxheight - 80, 225, self.__factBox.boxheight + 80), border_radius=15)
            pygame.draw.rect(display, color.WHITE, pygame.Rect(screenWidth - 215, screenHeight - self.__factBox.boxheight - 70, 205, self.__factBox.boxheight + 60), border_radius=5)
            self.__factBox.reposition(screenWidth - 210, screenHeight - self.__factBox.boxheight - 30)
            self.__factBox.place(200, color.GRAY, self.__fact)  
            self.__factQuitButton.repostion(screenWidth - 40, screenHeight - self.__factBox.boxheight - 70) 
            self.__factQuitButton.place(events, 0)  
                
                
            
            
    
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