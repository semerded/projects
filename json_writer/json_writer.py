import json, os

if os.path.isfile('data_jsonwriter.json') is False: # check if file exists
    raise Exception("Data file not found")
   
with open('data_jsonwriter.json') as datapath: # open file
    data = json.load(datapath) # take data out of file and save it

filenumber = data["filenumber"]

alphabet = "abcdefghijklmnopqrstuvwxyz"

def makeFile(filenumber):
    while True:
        filepath = f"output\\file{filenumber}.json"
        if (os.path.isfile(filepath) is False):
            open(filepath, 'w')
            return filepath, filenumber

        else:
            filenumber += 1

def deleteItems(openList, promptFilter, type, length = 0):
        print("working...")
        if promptFilter.lower() == "y":
            counter = 0
            while True:
                redoFilter = False
                counter += 1
                print("cycle %s" % counter)
                for index, element in enumerate(openList):
                    if type:
                        if len(element) < length:
                            openList.pop(index)
                    else:
                        for i, letter in enumerate(element):
                            if letter.lower() not in alphabet:
                                openList.pop(index)

                for index, element in enumerate(openList):
                    if type:
                        if len(element) < length:
                            redoFilter = True
                    else:
                        for i, letter in enumerate(element):
                            if letter.lower() not in alphabet:
                                redoFilter = True
                if not redoFilter:
                    break
        return

def restricitons(openList):
    promptFilter = input("only letters from alphabet? (Y/N): ")
    deleteItems(openList, promptFilter, False)
    
    promptFilter = input("lengthristriction? (Y/N): ")
    if promptFilter.lower() == "y":
        length = input("minimum length of word: ")
        error = False
        try:
            int(length)
        except ValueError:
            print("no number error")
            error = True
        else:
            if int(length) < 2:
                print("number to small")
        if error:
            print("error occurred: default number set to 4")
            length = 4
        length = int(length)
        deleteItems(openList, promptFilter, True, length)

    return openList

def selector1():
    prompt = input("textfile location: ")
    if os.path.isfile(prompt) is False:
        print("file not found")
        exit()
    file = open(prompt, "r")
    text = file.read()
    openDict = {}
    openList = text.split("\n")
    numberOfWords = len(openList)

    openList = restricitons(openList)

    openDict["data"] = openList
    filepath, number = makeFile(filenumber)
    with open(filepath, 'w') as json_file:
            json.dump(openDict, json_file, indent = 4, separators=(',',': '))
    print("\n\n\n\n\noperation succesfull")

    numberOfWordsLeft = len(openDict["data"])
    print(f"\nnumbes of words in original list: {numberOfWords}")
    print(f"number of words left: {numberOfWordsLeft}")
    print(f"words deleted: {numberOfWords - numberOfWordsLeft}")
    print(f"file name: file{number}.json")
    return number
    



def selector2():
    prompt = input("json file location: ")
    if os.path.isfile(prompt) is False:
        print("file not found")
        exit()
    with open(prompt) as filepath: # open file
        openDict = json.load(filepath) # take data out of file and save it
    prompt = input("key for words: ")
    try:
        openDict[prompt]
    except KeyError:
        print("key does not exitst")
    else:
        openList = openDict[prompt]
        numberOfWords = len(openList)
        openList = restricitons(openList)
        openDict["data"] = openList
        filepath, number = makeFile(filenumber)
        with open(filepath, 'w') as json_file:
            json.dump(openDict, json_file, indent = 4, separators=(',',': '))
        print("\n\n\n\n\noperation succesfull")

        numberOfWordsLeft = len(openDict["data"])
        print(f"\nnumbes of words in original list: {numberOfWords}")
        print(f"number of words left: {numberOfWordsLeft}")
        print(f"words deleted: {numberOfWords - numberOfWordsLeft}")
        print(f"file name: file{number}.json")
        return number
    
def selector3():
    prompt = input("json file location: ")
    if os.path.isfile(prompt) is False:
        print("file not found")
        exit()
    with open(prompt) as filepath: # open file
        openDict = json.load(filepath) # take data out of file and save it
    prompt = input("key for words: ")
    try:
        openDict[prompt]
    except KeyError:
        print("key does not exitst")
    else:
        maxLengthWord = 0
        openList = openDict[prompt]
        for woord in openList:
            if len(woord) > maxLengthWord:
                maxLengthWord = len(woord)
        print("the longest element in the file is %s letters long" % maxLengthWord)

print("writer selector")
print("1. word list\n2. json file\n3. longest element in json file calculator")
selector = input("number: ")
try:
    int(selector)
except ValueError:
    print("No number error")
    exit()
selector = int(selector)

if selector == 1:
    filenumber = selector1()

elif selector == 2:
    filenumber = selector2()
elif selector == 3:
    selector3()
    exit()
else:
    print("selector not avalible")
    exit()



data["filenumber"] = filenumber

with open('data_jsonwriter.json', "w") as json_file:
    json.dump(data, json_file, indent = 4, separators=(',',': '))


