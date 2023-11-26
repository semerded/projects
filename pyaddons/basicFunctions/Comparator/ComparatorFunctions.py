from typing import overload

class StringNotIntable(Exception):
    "raised when a string can not be converted to an int"
    pass

def isEven(number: int)-> bool:
    if number % 2 == 0:
        return True
    return False

def isNumber(input)-> bool:
    if type(input) in [int, float]:
        return True
    return False

def tryInt(input)-> bool:
    try:
        int(input)
    except ValueError:
        return False
    return True

# @overload
# def strToInt(string:str, )-> int:
#     try:
#         string = int(string)
#     except ValueError:
#             raise StringNotIntable("The given string Can't be converted to an int") 
#     return string

# @overload
# def strToInt(string:str, exceptValue:any = None):
#     try:
#         string = int(string)
#     except ValueError:
#         return exceptValue
#     return string

        

def isNumberString(string:str):
    fullNumberString = True
    for char in string:
        if not tryInt(char):
            fullNumberString = False
    return fullNumberString

def greater(input, biggerThan)-> bool:
    return True if input > biggerThan else False

def smaller(input, smallerThan)-> bool:
    return True if input < smallerThan else False


