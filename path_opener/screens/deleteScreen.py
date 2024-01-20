from screens.screen import Screen
from files.jsonHandler import saveJson
import globals, inputCommands

def place():
    Screen.clear()
    inputCommands.flushBuffer()
    currentPathNameBeingDeleted = globals.pathData[globals.currentIndicatorIndex]["name"]
    print("delete %s" %currentPathNameBeingDeleted)
    if inputCommands.yesNoQuestion():
        globals.pathData.pop(globals.currentIndicatorIndex)
        saveJson(globals.pathData)
        print("%s deleted")
        globals.currentIndicatorIndex = 0

    else:
        print("deletion aborted")
    inputCommands.loadDots()
    