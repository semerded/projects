import os, threading, time
hoppaV2fileFlags = []
printThreadActive = True
deleteThreadActive = True



def loadingIndicator():
    global loadingIndicatorStage
    try:
        loadingIndicatorStage
    except NameError:
        loadingIndicatorStage = 0
    loadingIndicators = [".  ", ".. ", "..."]
    currentLoadingIndicator = loadingIndicators[loadingIndicatorStage]
    loadingIndicatorStage += 1
    if loadingIndicatorStage == 3:
        loadingIndicatorStage = 0
    return currentLoadingIndicator

def printStatus():
    while printThreadActive:
        print(f"hoppa files found: {len(hoppaV2fileFlags)}{loadingIndicator()}\033[A")
        time.sleep(0.1)
    
def deleteStatus():
    while deleteThreadActive:
        print(f"deleting{loadingIndicator()}\033[A")
        time.sleep(0.1)


def main():
    global printThreadActive, deleteThreadActive
    possibleDiskNames = ['c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    failedHoppaFiles = []
    hoppaFilesRemoved = 0


        

    for diskName in possibleDiskNames:
        if os.path.exists("%s:/" %diskName):
            for path, dirs, files in os.walk("%s:/" %diskName):
                for file in files:
                    if file == "hoppaV2.txt":
                        filePath = os.path.join(path, file)
                        if filePath not in hoppaV2fileFlags:
                            hoppaV2fileFlags.append(filePath)

    printThreadActive = False
                        
    print("I found %s hoppa files\t" % len(hoppaV2fileFlags))
    if input("delete all hoppa files? (Y/N): ").lower() == "y":
        deleteStatusThread.start()
        for hoppaV2filePath in hoppaV2fileFlags:
            try:
                os.remove(hoppaV2filePath)
                hoppaFilesRemoved += 1
            except:
                failedHoppaFiles.append(hoppaV2filePath)
                
        deleteThreadActive = False
        print("succesfully removed %s hoppa files" %hoppaFilesRemoved)
        if len(failedHoppaFiles) > 0:
            print("unsuccesfully deleted %s hoppa files" %len(failedHoppaFiles))
            print(failedHoppaFiles)
    input()
    exit()
    
    
mainThread = threading.Thread(target=main, args=())
printStatusThread = threading.Thread(target=printStatus, args=())
deleteStatusThread = threading.Thread(target=deleteStatus, args=())
mainThread.start()
printStatusThread.start()
