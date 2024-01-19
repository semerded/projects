import os, keyboard, json, time
from enum import Enum

JSON_FILE_LOCATION = "path_opener/path opener save file.json"

class screens(Enum):
    mainScreen = 0
    editScreen = 1
    deleteScreen = 2
    addScreen = 3

currentIndicatorIndex = 0
currentScreen = screens.mainScreen

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')
    

def printMainScreen():
    clearScreen()
    for index, paths in enumerate(pathData):
        if index == currentIndicatorIndex:
            print(">>> %s" %paths["name"])
        else:
            print("    %s" %paths["name"])
            
def printAddScreen():
    clearScreen()
    print("add a path executable")
    newName = input("name: ")
    newPath = input("path: ")
    # TODO add check for file
        
    
def readJson():
    global pathData
    with open(JSON_FILE_LOCATION) as filePath:
        pathData = json.load(filePath)
    
def saveJson():
    with open(JSON_FILE_LOCATION, 'w') as json_file:
        json.dump(pathData, json_file, indent = 4, separators=(',',': '))
        
        
class KeyListener:
    def __init__(self, key: str) -> None:
        self.key = key
        self.clickedSafety = False
        
    def onClicked(self):
        if keyboard.is_pressed(self.key):
            if not self.clickedSafety:
                self.clickedSafety = True
                return True
            return False
        else:
            self.clickedSafety = False
            return False

key_e = KeyListener("e")
key_d = KeyListener("d")
key_a = KeyListener("a")
key_arrowUp = KeyListener("up")
key_arrowDown = KeyListener("down")
key_enter = KeyListener("return")

readJson()
printMainScreen()

while True:
    if currentScreen == screens.mainScreen:
        if key_arrowUp:
            currentIndicatorIndex -= 1
            if currentIndicatorIndex < 0:
                currentIndicatorIndex = len(pathData) - 1
            printMainScreen()
            
        if key_arrowDown:
            currentIndicatorIndex += 1
            if currentIndicatorIndex > len(pathData) - 1:
                currentIndicatorIndex = 0
            printMainScreen()
        
    elif currentScreen == screens.addScreen:
        printAddScreen()
        
    elif currentScreen == screens.deleteScreen:
        
    elif currentScreen == screens.editScreen:
        
    else:
        currentScreen = screens.mainScreen
    
    
    time.sleep(0.001)
   
        