from pyperclip import copy
from pyterminal.core import clearScreen
from pyterminal.keyListener import KeyListener
            
def run():
    clearScreen()
    woord = input("woord dat herhaald moet worden: ")
    aantal = input("aantal keren herhaald: ")
    newString = ""
    for nummer in range(int(aantal)):
        newString += (woord + str(nummer) + "\n")
    copy(newString)