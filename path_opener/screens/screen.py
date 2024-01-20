import os

class Screen:
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
