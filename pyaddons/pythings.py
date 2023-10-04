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

def intput(message: str =""):
    while True:
        prompt = input(message)
        try:
            int(prompt)
        except ValueError:
            print("input was not an int")
            continue
        return int(prompt)

