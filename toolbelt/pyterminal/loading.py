import time

def loadingDots(amount: int = 10):
    for index in range(amount):
        print("." * (index + 1), "\033[A")
        time.sleep(0.05)
    print()