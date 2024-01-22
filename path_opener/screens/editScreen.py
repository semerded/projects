from screens.screen import Screen
from files.jsonHandler import saveJson
import globals, inputCommands

def place():
    Screen.clear()
    inputCommands.flushBuffer()
    currentPathBeingEdited = globals.pathData[globals.currentIndicatorIndex]
    print("editing %s" %currentPathBeingEdited["name"])
    print("old path: %s" %currentPathBeingEdited["path"])
    print("old alternative path: %s\n" %currentPathBeingEdited["altPath"])
    newName = input("new name (enter to skip): ")
    newName = inputCommands.checkForValidInput(newName)
    
    newPath = input("new path (enter to skip): ")
    newPath = inputCommands.checkForValidInput(newPath)
    if newPath != None:  
        inputCommands.checkIfNonValidPath(newPath)
    
    newAltPath = input("new alternative path (enter to skip): ")
    newAltPath = inputCommands.checkForValidInput(newAltPath)
    if newAltPath != None:
        inputCommands.checkIfNonValidPath(newAltPath)
    
    print("you have changed:")
    if newName != None:
        print("  name")
        print(f"    {currentPathBeingEdited['name']} -> {newName}")
    
    if newPath != None:
        print("  path")
        print(f"    {currentPathBeingEdited['path']} -> {newPath}")
        
    if newAltPath != None:
        print("  alternative path")
        print(f"    {currentPathBeingEdited['altPath']} -> {newAltPath}")
    
    print("\nconfirm: ")
    if inputCommands.yesNoQuestion():
        if newName != None:
            currentPathBeingEdited["name"] = newName
        if newPath != None:
            currentPathBeingEdited["path"] = newPath
        if newAltPath != None:
            currentPathBeingEdited["altPath"] = newAltPath
        saveJson(globals.pathData)
        print("path updated")
    else:
        print("updating aborted")
    inputCommands.loadDots(15)
    
    
    
    
        