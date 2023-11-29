def run():
    import os, logging, time, json, msvcrt
    
    try:
        import byteconvertion
    except ModuleNotFoundError:
        import storageCleanUpTool.byteconvertion as byteconvertion
        
    try:
        import getReport
    except ModuleNotFoundError:
        import storageCleanUpTool.getReport as getReport


    print("\n\nA scan of your whole system will start\nThis will take a couple of minutes")
    print("Start?: ")
    prompt = msvcrt.getche()
    print("preparring tool")
    time.sleep(1)
    print("checking system")
    time.sleep(1)
    print("let's go!")
    time.sleep(1)
    
    #TODO add terminal animation

    if not prompt.lower() == b"y":
        return
    
    def saveDataToJson(fileSaveType, dict, fileSize, filePath):
        with open(jsonPath) as JSONfile:
            dict = json.load(JSONfile)
        
        dict[fileSaveType][filePath] = byteconvertion.byteConvertion(fileSize)
        logger.info(f"{filePath} ~ {fileSize}")
        
        with open(jsonPath, 'w') as JSONfile:
            json.dump(dict, JSONfile, indent = 4, separators=(',',': '))
        
        return dict

    # setting up logger
    logging.basicConfig(filename="logging.log",
                        format='%(asctime)s %(message)s',
                        filemode='w',
                        level=logging.INFO)
    logger = logging.getLogger()

    # checking if report files exist
    def checkPaths(file: str, errorMsg: str = ""):
        if os.path.isfile("storageCleanUpTool\%s" % file):
            logger.info("%s found" % file)
            return "storageCleanUpTool\%s" % file
        
        elif os.path.isfile(file):
            logger.info("%s found" % file)
            return file

        else:
            logger.error("%s not found" % file)
            if not errorMsg == "":
                print("Couldn't find %s\n" % file, errorMsg) 
            return False

    reportPath = checkPaths("storageCleanUpReport.html", "You can find the report in the JSON file")
    jsonPath = checkPaths("storageCleanUpSaveFile.json", "Please add this file in this folder")
    if not jsonPath:
        return 

    # start main program

    possibleDiskNames = ['c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    largeFiles = {"1GB": {}, "100MB": {}, "windows": {}}
    with open(jsonPath, 'w') as JSONfile:
            json.dump(largeFiles, JSONfile, indent = 4, separators=(',',': '))
    
    fileCheckedAmount = 0
    timeStarted = time.time()

    for diskName in possibleDiskNames:
        if os.path.exists("%s:/" % diskName):

            for path, dirs, files in os.walk("%s:/" % diskName):
                for file in files:
                    timeElapsed = round(time.time() - timeStarted, 2)
                    filePath = os.path.join(path, file)
                    fileCheckedAmount += 1
                    
                    try:
                        print(f"{timeElapsed} | {len(largeFiles['1GB'])} > 1GB | {len(largeFiles['100MB'])} > 100MB | checking: {filePath}")
                        fileSize = os.path.getsize(filePath)
                        if not any(x in filePath.lower() for x in ["windows", "sys"]) :
                            if fileSize > 1000000000:
                                largeFiles = saveDataToJson("1GB", largeFiles, fileSize, filePath)

                            elif fileSize > 100000000:
                                largeFiles = saveDataToJson("100MB", largeFiles, fileSize, filePath)

                        elif fileSize > 100000000:
                            largeFiles = saveDataToJson("windows", largeFiles, fileSize, filePath)
                            
                    except:
                        print("checking file failed")
                        logger.exception("failed to check %s" % filePath)
                    

                        
                        

    # sorting files
    with open(jsonPath) as JSONfile:
            largeFiles = json.load(JSONfile)
    for types in largeFiles:
        try:
            largeFiles[types] = sorted(largeFiles[types].items(), key=lambda item: item[1], reverse=True)
            logger.info("report sorted")
        except:
            logger.warn("report not sorted")
    with open(jsonPath, "w") as JSONfile:
        json.dump(largeFiles, JSONfile, indent = 4, separators=(',',': '))
            
    getReport.getReport(reportPath, largeFiles, [timeElapsed, fileCheckedAmount])

    print(f"{len(largeFiles['1GB'])} files above 1GB found")
    print(f"{len(largeFiles['100MB'])} files above 100MB (under 1GB) found")
    print((f"{len(largeFiles['windows'])} files above 100MB with 'windows' in it"))
    print(f"runtime = {timeElapsed}s | files checked = {fileCheckedAmount}")
    # open report in html file
    os.system("start %s" % reportPath)
    input("done >>> ")