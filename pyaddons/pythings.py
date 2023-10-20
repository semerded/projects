def isNumber(input, errorMessage: str = "") -> bool:
    try:
        int(input)
        float(input)
    except ValueError:
        return False
    return True


def average(list: list):
    for element in list:
        if not isNumber(element):
            raise ValueError("non number in list")
    listLength = len(list)
    return sum(list) / listLength

def intput(message: str ="", errorMessage: str = "input was not an int", repeatUntilInt: bool = True):
    while True:
        prompt = input(message)
        try:
            int(prompt)
        except ValueError:
            print(errorMessage)
            if not repeatUntilInt:
                return
            continue
        return int(prompt)

def isEven(number: int):
    if number % 2 == 0:
        return True
    return False
