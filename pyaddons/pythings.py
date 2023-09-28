def isNumber(input, errorMessage: str = ""):
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


    