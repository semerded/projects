import pyperclip
pathName = input("path name: ")
pathName = pathName.replace("\\", "/")
pyperclip.copy(pathName)