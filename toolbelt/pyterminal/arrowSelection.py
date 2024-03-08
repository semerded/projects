from keyListener import KeyListener
from keyEnum import keyboardKeys
from core import goToBeginningOfLine, clearScreen

class ArrowSelection:
    def __init__(self, selection: list[str]) -> None:
        self.arrowUp = KeyListener(keyboardKeys.arrowUp)
        self.arrowDown = KeyListener(keyboardKeys.arrowDown)
        self.enter = KeyListener(keyboardKeys.enter)
        self.currentSelectionIndex = 0
        self.selection = selection
        self.firstDraw = True
        self.previousDrawLength = len(selection)
        
        
    def getSelectionLength(self):
        return len(self.selection)
    
    def place(self):
        if self.arrowUp.isClicked():
            self.currentSelectionIndex -= 1
            self._drawer()

        if self.arrowDown.isClicked():
            self.currentSelectionIndex += 1
            self._drawer()
        
        if self.firstDraw:
            self._drawer()
            self.firstDraw = False
            
        if self.enter.isClicked():
            return self.selection[self.currentSelectionIndex]      
        
    def _fixSelectionIndexOverflow(self):
        if self.currentSelectionIndex < 0:
            self.currentSelectionIndex = self.getSelectionLength() - 1
        
        if self.currentSelectionIndex > self.getSelectionLength() - 1:
            self.currentSelectionIndex = 0
            
    def _drawer(self):
        self._fixSelectionIndexOverflow()
        # clearScreen()
        if not self.firstDraw:
            for _ in range(self.previousDrawLength):
                print("\033[A", end = "")
            
        for index, item in enumerate(self.selection):
            if index == self.currentSelectionIndex:
                print(">>> %s" %item)
            else:
                print("    %s" %item)
        self.previousDrawLength = self.getSelectionLength()
        

test = ArrowSelection(["hello", "goodbye", "quit"])
while True:
    test.place()
                
        