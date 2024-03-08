import os, json, webbrowser, time
from pyterminal.core import clearScreen, flushBuffer
from pyterminal.keyListener import KeyListener
from pyterminal.loading import loadingDots
from pyterminal.display import title


filePath = "pages/converterlist.json"
if os.path.isfile(filePath) is False: # check if file exists
    raise ImportError("Data file not found")

with open(filePath) as file:
    file = json.load(file)



esc = KeyListener("escape")
numberKeys = []

for index in range(10):
    if index + 1 == 10:
        numberKeys.append(KeyListener("0"))
    else:  
        numberKeys.append(KeyListener(str(index + 1)))
        
def draw():
    title("converter portal (find all useful converters with 1 click)")
    for index, data in enumerate(file):
        print(f"{index + 1}. {data["name"]}")
    
def openUrl(index):
    data = file[index]
    webbrowser.open(data["url"])

def run():
    draw()
    while True:
        if esc.isClicked():
            return
        
        for index, key in enumerate(numberKeys):
            if key.isClicked():
                try:
                    print(f"loading {file[index]["name"]} ({file[index]["url"]})")
                    loadingDots()
                    openUrl(index)
                except Exception:
                    print("nothing on this key")
                flushBuffer()
                clearScreen()
                draw()
                
        time.sleep(0.02)
