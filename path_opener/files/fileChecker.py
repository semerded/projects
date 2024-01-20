import os

def fileChecker(filePath):
    if os.path.isfile(filePath) == True:
        return True
    return False