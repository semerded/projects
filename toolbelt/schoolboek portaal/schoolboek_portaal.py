import os
from schoolboek_portaal_setup import *

filePath = "schoolboek_portaal.json"
if os.path.isfile(filePath) is False: # check if file exists
    raise Exception("Data file not found")

with open(filePath) as file:
    file = json.load(file)
    
if file["setup"]:
    pass
    setupWindow(file, filePath)

while True:
    print("0. options")
    numberOfWebsites = 0

    for index, website in enumerate(file["boeken"]):
        print(f"{index}. {website}")
        numberOfWebsites += 1
    if numberOfWebsites == 0:
        setupWindow(file, filePath, "links_only")
        continue
    prompt = input(">> ")
    if valueError(prompt, "input is not an int"):
        continue
    


