from functions import *
import json
def setupWindow(file,filepath, command:str = ""):
    def addLink(multiple: bool = False):
        while True:
            link = input("link: ")
            if link.lower() == "stop" and multiple:
                link = "stop"
                break
            if link[:4] == "http":
                break
            print("link not valid")
        return link
        
    print("schoolboek portaal setup")
    data = file["data"]
    if not command == "links_only":
        # naam
        data["naam"] = input("naam: ").capitalize()

    # links voor sites
    print("\n\n\nadd websites\n")
    while True:
        linkList = []
        print("website naam (stop to end)")
        websiteName = input(">> ")
        if websiteName.lower() == "stop":
            break
        while True:
            print("\n1. 1 link\n2. meerdere links")
            prompt = input(">> ")
            if not valueError(prompt, "value is not an int"):
                break
        if int(prompt) == 1:
            print("add link")
            linkList.append(addLink())
            
            
            file["boeken"][websiteName] = linkList
        else:
            print("add links / stop")
            while True:
                link = addLink(True)
                if link == "stop":
                    break
                linkList.append(link)
        
        print("\noverview:")
        print(f"\tnaam: {websiteName}\n\tlink: {file['boeken'][websiteName]}")
        if input("correct? (Y/N): ") == "Y":
            with open(filepath, "w") as json_file:
                json.dump(data, json_file, indent = 4, separators=(',',': '))
        
    endShell()
        
