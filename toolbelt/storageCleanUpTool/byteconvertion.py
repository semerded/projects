convertionRates = {1000000000: "GB", 1000000: "MB", 1000: "KB"}

def byteConvertion(bytes: int)-> str:
    for convertions in convertionRates:
        if bytes > convertions:
            return f"{bytes / convertions} {convertionRates[convertions]}"
    return f"{bytes}"

