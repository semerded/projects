import pathchanger, capitalize, papagaaienwerk, zaklamp, folder_maker, storageCleanUpTool.storageCleanUpTool
import json, msvcrt, os

import os



def redraw():
    # welcome menu
    os.system('cls' if os.name == 'nt' else 'clear')

    print("                .__                               \n",
    "__  _  __ ____ |  |   ____  ____   _____   ____  \n",
    "\ \/ \/ // __ \|  | _/ ___\/  _ \ /     \_/ __ \ \n",
    " \     /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/ \n",
    "  \/\_/  \___  >____/\___  >____/|__|_|  /\___  >\n",
    "             \/          \/            \/     \/ \n",
    "\n",
    "___________________   ________  .____   _____________________.____  ___________\n",
    "\__    ___/\_____  \  \_____  \ |    |  \______   \_   _____/|    | \__    ___/\n",
    "  |    |    /   |   \  /   |   \|    |   |    |  _/|    __)_ |    |   |    |   \n",
    "  |    |   /    |    \/    |    \    |___|    |   \|        \|    |___|    |   \n",
    "  |____|   \_______  /\_______  /_______ \______  /_______  /|_______ \____|   \n",
    "                   \/         \/        \/      \/        \/         \/        \n\n",
    "#" * 60,
    "\n hello %s\n" % name,
    "#" * 60)
    print("-" * 60, "\n")
    for currentNameNumber in range(len(callNames)):
            print(f"{currentNameNumber + 1}. {callNames[currentNameNumber]}")


with open("toolbelt setup.json") as setupFile:
    setup = json.load(setupFile)
name = setup["name"]

callNumbers = [1,2,3,4,5,6]
callNumbersAlt = [b'&', 'é', b'"',b"'", b'(', '§']
callNames = ["pathchanger", "capitalize", "papagaaienwerk", "zaklamp", "folder maker", "large files finder (storage clean up tool)"]
callPrograms = [pathchanger, capitalize, papagaaienwerk, zaklamp, folder_maker, storageCleanUpTool.storageCleanUpTool]

def Main():
    input_char = msvcrt.getch()
    if input_char.lower() == b"q":
        exit()
    for index, altCall in enumerate(callNumbersAlt):
        if input_char == altCall:
            callPrograms[index].run()
    try:
        input_char = int(input_char)
    except ValueError:
        redraw()
    else:
        if input_char in callNumbers:
            callPrograms[input_char - 1].run()
            redraw()
        else:
            redraw()
            
redraw() # initial draw            
while True:
    # try:
        Main()
    # except:
    #     print("an error has occurd")
        