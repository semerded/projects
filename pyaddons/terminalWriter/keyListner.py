import keyboard

class KeyListener:
    def __init__(self, key: str) -> None:
        self.key = key
        self.clicked = False
        self.released = True
        
    def _reader(self):
        return keyboard.is_pressed(self.key)
        
    def onClicked(self):
        if self._reader():
            if not self.clicked:
                self.clicked = True
                return True
            return False
        self.clicked = False
        return False
    
    def onRelease(self):
        if not self._reader():
            if not self.released:
                self.released = True
                return True
            return False
        self.released = False
        return False
            
        
    def isPressed(self):
        return self._reader()
