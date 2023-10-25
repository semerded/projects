def run():
    from pyperclip import copy
    woord = input("woord dat herhaald moet worden: ")
    aantal = input("aantal keren herhaald: ")
    if woord == "<<<" or aantal == "<<<":
        return
    newString = ""
    for nummer in range(int(aantal)):
        newString += (woord + str(nummer) + "\n")
    copy(newString)