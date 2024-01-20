from screens.screen import Screen
from files.fileChecker import fileChecker
from files.jsonHandler import saveJson
import globals, inputCommands

def place():
    Screen.clear()
    print("add a path executable")
    newName = input("name: ")
    newPath = input("path: ")
    inputCommands.checkIfNonValidPath(newPath)
    alternativePath = input("alternative path (enter to skip): ")
    alternativePath = inputCommands.checkForValidInput(alternativePath)
    if alternativePath != None:
        inputCommands.checkIfNonValidPath(newPath)

    print("\nsave '%s'?" % newName)
    if inputCommands.yesNoQuestion():
        globals.pathData.append(
                {
                "name": newName, 
                "path": newPath, 
                "altPath": alternativePath
                }
            )
        
        print("path added")
        saveJson(globals.pathData)
    else:
        print("path aborted")
    
    inputCommands.loadDots(15)
