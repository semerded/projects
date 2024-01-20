# short commands including an input

from files.fileChecker import fileChecker
import time, sys, msvcrt


def yesNoQuestion():
    if input("(Y/N): ") in ("Y","y"):
        return True
    return False

def checkForValidInput(input):
    if input != "":
        return input
    return None

def checkIfNonValidPath(newPath):
    if not fileChecker(newPath):
        print("\twarning! path not found")
        
def loadDots(amount: int = 10):
    for index in range(amount):
        print("." * (index + 1), "\033[A")
        time.sleep(0.05)
    print()
        
def flushBuffer():
    sys.stdout.flush()
    while msvcrt.kbhit():
        msvcrt.getch()