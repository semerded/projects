from pyperclip import copy

def strToList(string:str)-> list:
    tempList = []
    for letter in string:
        tempList.append(letter)
    return tempList

def toString(input:any)-> str:
    return f"{input}"

def outCome(outComeList):
    print("printed to clipboard!")
    print("length of list: %s" % len(outComeList))
    copy(toString(outComeList))

def run():
    print("\n\n1.divide per letter\n2.other division")

    if input(">>> ") == "1":
        outComeList = strToList(input("string: "))
        outCome(outComeList)
    else:
        stringInput = input("string: ")
        division = input("char division: ")
        outComeList = stringInput.split(division)
        outCome(outComeList)