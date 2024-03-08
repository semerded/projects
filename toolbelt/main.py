from pages import pathchanger, stringToList, converter_portal, schoolboek_portaal, bigComment, papagaaienwerk, capitalize, zaklamp

import json, sys, time

from pyterminal.core import clearScreen, flushBuffer
from pyterminal.loading import loadingDots
from pyterminal.keyListener import KeyListener 



# welcome menu
clearScreen()
# print("                .__                               \n",
# "__  _  __ ____ |  |   ____  ____   _____   ____  \n",
# "\ \/ \/ // __ \|  | _/ ___\/  _ \ /     \_/ __ \ \n",
# " \     /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/ \n",
# "  \/\_/  \___  >____/\___  >____/|__|_|  /\___  >\n",
# "             \/          \/            \/     \/ \n",
# "\n",
# "___________________   ________  .____   _____________________.____  ___________\n",
# "\__    ___/\_____  \  \_____  \ |    |  \______   \_   _____/|    | \__    ___/\n",
# "  |    |    /   |   \  /   |   \|    |   |    |  _/|    __)_ |    |   |    |   \n",
# "  |    |   /    |    \/    |    \    |___|    |   \|        \|    |___|    |   \n",
# "  |____|   \_______  /\_______  /_______ \______  /_______  /|_______ \____|   \n",
# "                   \/         \/        \/      \/        \/         \/        \n\n",
# "#" * 60,
# "\n hello %s\n" %name,
# "#" * 60)
# print()


def redraw(clear = True):
    if clear:
        clearScreen()
    print("-" * 60, "\n")
    for index, name in enumerate(callNames):
        print(f"{index + 1}. {name}")
    

delete = KeyListener("delete")
numberKeys = []

for index in range(10):
    if index + 1 == 10:
        numberKeys.append(KeyListener("0"))
    else:  
        numberKeys.append(KeyListener(str(index + 1)))



callNames = ["pathchanger", "string to list converter", "online converter portal", "schoolbooks portal", "big comment maker", "papagaaienwerk", "scentence capitalizer", "flashlight"]
callPrograms = [pathchanger, stringToList, converter_portal, schoolboek_portaal, bigComment, papagaaienwerk, capitalize, zaklamp]


            
redraw(False)        
while True:
    if delete.isClicked():
        sys.exit()
    for index, key in enumerate(numberKeys):
        if key.isClicked():
            loadingDots()
            flushBuffer()
            callPrograms[index].run()
            redraw()
            
    time.sleep(0.02)