from screens.screen import Screen
import globals

def place():
    Screen.clear()
    print("(a) add path | (e) edit path | (d) delete path | (esc) quit\n")
    for index, paths in enumerate(globals.pathData):
        if index == globals.currentIndicatorIndex:
            print(">>> %s" %paths["name"])
        else:
            print("    %s" %paths["name"])

