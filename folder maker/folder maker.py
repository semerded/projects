import os

def sample():
    checker = True
    for map in mapNameList:
        path = os.path.join(targetPath, map)
        if os.path.exists(path) is False:
            checker = False
    return checker

def checkList(title, list):
    print("\n%s list: \n" % title)  
    for index, map in enumerate(list):
        print(f"\t{index + 1}. {map}")
    prompt = input("type number to delete / enter to skip: ")
    try:
        int(prompt)
    except ValueError:
        return True
    list.pop(int(prompt) - 1)
    
def mapMaker(title, list):
    mapName = input("\n%s name: " % title)
    if mapName.lower() == r"%stop" or mapName.lower() == r"%done":
        return True
    list.append(mapName)
    
       

while True:
    targetPath = input("target path: ")
    
    if "\\" in targetPath:
        targetPath = targetPath.replace("\\", "/")

    if os.path.exists(targetPath) == False:
        raise FileNotFoundError("path not found")


    mapNameList = []
    submapNameList = []
    while True:
        if mapMaker("map", mapNameList):
            break
    while True:
        if checkList("map", mapNameList):
            break
        
        
    while True:
        if mapMaker("submap", submapNameList):
            break
    while True:
        if checkList("submap", submapNameList):
            break
        
    for map in mapNameList:
        path = os.path.join(targetPath, map)
        try: 
            os.mkdir(path) 
        except OSError: 
            continue
            
        for submap in submapNameList:
            subpath = os.path.join(path, submap)
            try: 
                os.mkdir(subpath) 
            except OSError: 
                continue
    
    
    if sample():
        break
    print("maps not correctly made")
    if input("redo? (Y/N): ").lower() != "y":
        break

# end cyclus
print("\nmaps succesfully made!\n")
print("press enter to exit")
input() # end script