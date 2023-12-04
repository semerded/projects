import time, logging
import threading
from datetime import datetime
from enum import Enum

def isNumber(input, errorMessage: str = "") -> bool:
    try:
        int(input)
        float(input)
    except ValueError:
        return False
    return True


def average(list: list):
    for element in list:
        if not isNumber(element):
            raise ValueError("non number in list")
    listLength = len(list)
    return sum(list) / listLength

def intput(message: str ="", errorMessage: str = "input was not an int", repeatUntilInt: bool = True):
    while True:
        prompt = input(message)
        try:
            int(prompt)
        except ValueError:
            print(errorMessage)
            if not repeatUntilInt:
                return
            continue
        return int(prompt)

def logger(fileName:str = "logging") -> logging.Logger:
    logging.basicConfig(filename=fileName + ".log",
                         format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%H:%M:%S',
                        filemode='w',
                        level=logging.INFO)
    logger = logging.getLogger()
    logger.info("program started: %s"%datetime.now())
    return logger


def valid(item: any) -> bool:
    if item == None:
        return False
    return True

def loopThrough(object, counter:int)->int:
    if counter >= len(object):
        counter = 0
    else:
        counter += 1
    return counter # TODO return object from list

# def loadingIndicator():
#     global loadingIndicatorStage
#     try:
#         loadingIndicatorStage
#     except NameError:
#         loadingIndicatorStage = 0
#     loadingIndicators = [".  ", ".. ", "..."]
#     currentLoadingIndicator = loadingIndicators[loadingIndicatorStage]
#     loadingIndicatorStage += 1
#     if loadingIndicatorStage == 3:
#         loadingIndicatorStage = 0
#     return currentLoadingIndicator

class loadingCharTypes(Enum):
    DOTS = 0
    SLASH = 1
    
class printLoadingStatus:
    def __init__(self, loadingChar:loadingCharTypes, waitTime: int = 100, extraPrintInfo:str = "") -> None: # TODO test extraprintinfo
        self.printSpeed = waitTime / 1000
        self.threadActive = False
        self.loadingIndicatorStage = 0

        self.loadingIndicators = [[".  ", ".. ", "..."], ["\\", "|", "/", "|"]]
        self.loadingChars = self.loadingIndicators[loadingChar.value]
        self.extraPrintInfo = extraPrintInfo

    def config(self, loadingChar:loadingCharTypes = None, waitTime:int = None, extraPrintInfo:str = None) -> None:
        if valid(loadingChar):
            self.loadingChars = self.loadingIndicators[loadingChar.value]
        if valid(waitTime):
            self.printSpeed = waitTime / 1000
        if valid(extraPrintInfo):
            self.extraPrintInfo = extraPrintInfo
        
    def loadingIndicator(self) -> str:
        self.loadingIndicatorStage += 1
        if self.loadingIndicatorStage >= len(self.loadingChars):
            self.loadingIndicatorStage = 0
        return self.loadingChars[self.loadingIndicatorStage]
        
        
    def printLoop(self):
        while self.threadActive:
            print(f"{self.extraPrintInfo}{self.loadingIndicator()}\033[A")
            
    
    def start(self) -> bool:
        self.threadActive = True
        try:
            self.thread = threading.Thread(target=self.printLoop, args=())  
            self.thread.start()
        except:
            return False
        return True

        
    def stop(self) -> None:
        self.threadActive = False
        
test = printLoadingStatus(loadingCharTypes.SLASH)
test.start()
time.sleep(2)
test.stop()
test.config(loadingCharTypes.DOTS)
time.sleep(2)
test.start()
time.sleep(2)
test.stop()


# counter = 0
# while True:
#     counter += 1
#     print(counter)
#     time.sleep(0.1)
    
    

    
