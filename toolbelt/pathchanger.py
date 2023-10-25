def run():
    from pyperclip import copy
    pathName = input("path name: ")
    if pathName == "<<<":
        return
    pathName = pathName.replace("\\", "/")
    copy(pathName)