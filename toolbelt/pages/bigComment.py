from pyperclip import copy
import time
from pyterminal.keyListener import KeyListener
from pyterminal.core import clearScreen, flushBuffer
from pyterminal.loading import loadingDots
from pyterminal.display import title

commentPrefixes = ("#", "//")
commentFills = ("#", "/")

esc = KeyListener("escape")

numberKeys = []
for index in range(10):
    if index + 1 == 10:
        numberKeys.append(KeyListener("0"))
    else:  
        numberKeys.append(KeyListener(str(index + 1)))
        
def askAndConvertComment(commentPrefix, commentFill):
    comment = input("give your comment: ")
    comment = f"{commentPrefix} {comment.strip()} {commentPrefix}"
    bigComment = f"{commentFill * len(comment)}\n{comment}\n{commentFill * len(comment)}" 
    copy(bigComment)

def run():
    title("big comment maker")

    print("1. Python comment (#)")
    print("2. slash comment (//)")
    # TODO add more comment support (example: html)
    while True:
        if esc.isClicked():
            return
        
        for index, key in enumerate(numberKeys):
            if key.isClicked():
                try:
                    loadingDots()
                    flushBuffer()
                    clearScreen()
                    commentPrefix = commentPrefixes[index]
                    commentFill = commentFills[index]
                    askAndConvertComment(commentPrefix, commentFill)
                    return

                except Exception:
                    print("nothing on this key")
                
                
        time.sleep(0.02)
        
        
        
    


