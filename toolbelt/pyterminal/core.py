import os, msvcrt, sys

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def flushBuffer():
    sys.stdout.flush()
    while msvcrt.kbhit():
        msvcrt.getch()
        
def endProgram(text: str = "program finished"):
    print(text)
    input()
    sys.exit()
    
def goToBeginningOfLine():
    print("\033[A", end="")