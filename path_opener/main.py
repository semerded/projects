import time, os

#file import
from files import jsonHandler
from screens import addScreen, editScreen, mainScreen, deleteScreen, screen
from keyListner import KeyListener
import globals

key_e = KeyListener("e")
key_d = KeyListener("d")
key_a = KeyListener("a")
key_arrowUp = KeyListener("up")
key_arrowDown = KeyListener("down")
key_enter = KeyListener("return")
key_esc = KeyListener("escape")

globals.pathData = jsonHandler.readJson()

mainScreen.place()
        
while True:
    if key_arrowUp.onClicked():
        globals.currentIndicatorIndex -= 1
        if globals.currentIndicatorIndex < 0:
            globals.currentIndicatorIndex = len(globals.pathData) - 1
        mainScreen.place()
        
    if key_arrowDown.onClicked():
        globals.currentIndicatorIndex += 1
        if globals.currentIndicatorIndex > len(globals.pathData) - 1:
            globals.currentIndicatorIndex = 0
        mainScreen.place()
        
    if key_a.onClicked():
        addScreen.place()
        mainScreen.place()
        
        
    if key_d.onClicked():
        deleteScreen.place()
        mainScreen.place()
        
        
    # if key_e.onClicked():
    #     editScreen.place()
    #    mainScreen.place()
    
    if key_enter.onClicked():
        
        os.startfile(globals.pathData[globals.currentIndicatorIndex]["path"])
    
    if key_esc.onClicked():
        screen.Screen.clear()
        break
  
   
    
    time.sleep(0.001)
   
        