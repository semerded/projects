from pyperclip import copy

woord = input("woord dat herhaald moet worden: ")
aantal = input("aantal keren herhaald: ")
newString = ""
for nummer in range(int(aantal)):
    newString += (woord + str(nummer) + "\n")
copy(newString)