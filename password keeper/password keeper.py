import os, json, random
from time import sleep

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


    
def passwordGenerator(lengte: int = 12, kleine_letters: bool = True, hoofdletter: bool = True, cijfers: bool = True, speciale_tekens: bool = True):
    char = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "@&#!|*%" 
    ]
    karakters = wachtwoord = ""
    if kleine_letters:
        karakters += char[0]
    if hoofdletter:
        karakters += char[1]
    if cijfers:
        karakters += char[2]
    if speciale_tekens:
        karakters += char[3]
    truerandom = random.randint(1,100)
    for i in range(truerandom):
        wachtwoord = ""
        for j in range(lengte):
            wachtwoord += random.choice(karakters)
    return wachtwoord
    
def passwordMaker():
    print("\nwelcome to password maker\n")
    while True:
        password = passwordGenerator()
        print("suggested password: %s"% password)
        prompt = input("\n1. use suggested password\n2. new suggested password\n3. write own password\n>> ")
        while True:
            if valueError(prompt, "input is not an int"):
                continue
            break
        prompt = int(prompt)
        if prompt == 1:
            return password
        elif prompt == 2:
            continue
        else:
            password = input("make your own password: ")
            if password != "":
                return password

    


        



if os.path.isfile('password keeper.json') is False or os.path.isfile('password keeper setup.json') is False: # check if file exists
    raise Exception("Data file not found")

with open('password keeper setup.json') as setupFile: # open file
    setup = json.load(setupFile) # take data out of file and save it with json layout

    
def askPassword():
    print("\npassword keeper_")
    sleep(1)
    print("welcome back %s" % setup["name"])
    if setup["password"] != None:
        for i in range(3):
            appPassword = input("\napp password: ")
            if appPassword == setup["password"]:
                correct = True
                break
            correct = False
            print("password incorrect, try again")
        if correct == True:
            print("<password correct>\nopening app...")
            sleep(0.5)
        else:
            print("no more password guesses left\n\ntry again later...")
            exit()

def setupKeeper():
    setup["setup"] = False
    print("welcome to the password keeper setup")
    # naam
    name = input("name: ")
    setup["name"] = name

    # verdwijn wachtwoord na ... seconden
    hidetime = input("hide password after ... seconds / none for no time: ")
    if hidetime.lower() == "none":
        setup["hidetime"] = None
    else:
        if not valueError(hidetime, "input is not an int, part skipped"):
            setup["hidetime"] = int(hidetime)

    # wachtwoord app
    password = input("password for this app (Y/N): ")
    if password.lower() == "n":
        setup["password"] = None
    else:
        setup["password"] = passwordMaker()

    # beveiligingsvragen
    if setup["password"] != None:
        prompt = input("do you want safety questions in case you forget your password? (Y/N): ")
        if prompt.lower() == "y":
            safetyquestionDict = {}
            while True:
                print("\nyou can have as many safety questions as you want\nto stop making safety questions type 'stop'")
                vraag = input("QUESTION: ")
                if vraag.lower() == "stop":
                    break
                antwoord = input("ANSWER: ")
                if antwoord.lower() == "stop":
                    break
                safetyquestionDict[vraag] = antwoord
                
            setup["safetyquestion"] = safetyquestionDict
        else:
            setup["safetyquestion"] = None
    else:
        setup["safetyquestion"] = None

    print("you can change the setup later")
    setup["setup"] = True

    with open("password keeper setup.json", 'w') as json_file:
            json.dump(setup, json_file, indent = 4, separators=(',',': '))


if setup["setup"] == False:
    setupKeeper()

askPassword()
hidetime = setup["hidetime"]

with open('password keeper.json') as dataFile:
    data = json.load(dataFile)


while True:
    print("1. see passwords\n2. add password\n3. delete password\n4. account list\n5. setup\n6. quit")
    prompt = input("input field: ")
    if valueError(prompt, "input was not an int"):
        continue
    prompt = int(prompt)
    if prompt == 4:
        for key in data:
            print(key)
    if prompt == 5:
        setupKeeper()
    if prompt == 6:
        print("see you later")
        exit()



