def valueError(waarde, valueErrorMessage:str = ""):
    """
zal True terug geven als de waarde geen integer is
zal False terug geven als de waarde wel een integer is
    """
    try:
        int(waarde)
    except ValueError:
        if valueErrorMessage != "":
            print(valueErrorMessage)
        return True
    else:
        return False

def endShell():
    """
    let's you exit the shell with enter to avoid the Shell to close automatically after the last action
    """
    print("press enter to exit")
    input()