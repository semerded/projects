import keyboard
class KeyListener:
    def __init__(self, key: str) -> None:
        self.key = key
        self.clickedSafety = False
        
    def onClicked(self):
        if keyboard.is_pressed(self.key):
            if not self.clickedSafety:
                self.clickedSafety = True
                return True
            return False
        else:
            self.clickedSafety = False
            return False