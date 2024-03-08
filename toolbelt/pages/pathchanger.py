from pyterminal.core import clearScreen
from pyterminal.display import title

def run():
    clearScreen()
    title("path changer (changes \\ to /)")
    from pyperclip import copy
    pathName = input("path name: ")
    if pathName == "<<<":
        return
    pathName = pathName.replace("\\", "/")
    copy(pathName)