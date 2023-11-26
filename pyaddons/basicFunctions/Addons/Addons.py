def YNquestion(customMsg:str = "")-> bool:
    if input("%s (Y/N): " % customMsg).lower() == "y":
        return True
    return False

def strToList(string:str)-> list:
    tempList = []
    for letter in string:
        tempList.append(letter)
    return tempList

def toString(input:any)-> str:
    return f"{input}"