import os, msvcrt, sys, time

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def flushBuffer():
    sys.stdout.flush()
    while msvcrt.kbhit():
        msvcrt.getch()
        
def loadingDots(amount: int = 10):
    for index in range(amount):
        print("." * (index + 1), "\033[A")
        time.sleep(0.05)
    print()
    
def yesNoQuestion():
    return input("(Y/N): ") in ("Y","y")