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

def getIntNumber(min: int, max: int, inputText: str, errorText: str):
    prompt = input(inputText)
    try:
        int(prompt)
    except ValueError:
        print(errorText)
        return True
    else:
        if int(prompt) >= min and int(prompt) <= max:
            return int(prompt)

    
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
    print("-~"*20)
    print("\nwelcome to password maker\n")
    while True:
        password = passwordGenerator()
        print("suggested password: %s"% password)
        while True:
            prompt = input("\n1. use suggested password\n2. new suggested password\n3. write own password\n>> ")
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

def askSafetyQuestions():
    print(setup["safetyquestion"][0])
    answer = input("answer: ")
    if answer == decript(setup["safetyquestion"][1]):
        return True
    return False
    
    
    
    
def askPassword():
    print("\npassword keeper_")
    for i in range(5):
        print("loading.  \033[A")
        sleep(0.2)
        print("loading.. \033[A")
        sleep(0.2)
        print("loading...\033[A")
        sleep(0.2)
 
      

    print("welcome back %s" % setup["name"])
    if setup["password"] != None:
        for i in range(3):
            appPassword = input("\napp password: ")
            if appPassword == decript(setup["password"]):
                correct = True
                break
            correct = False
            print("password incorrect, try again")
        if correct == True:
            print("<password correct>\nopening app...")
            sleep(0.5)
            return
        else:
            print("no more password guesses left")
            if input("do you want to reset your password? (Y/N) ").lower() == "y":
                if setup["safetyquestion"] != None:
                    if askSafetyQuestions():
                        print("safety question correct")
                        print("starting paswordMaker")
                        setup["password"] = passwordMaker()
                    else:
                        print("\nsafety question incorrect")
        print("\n\ntry again later")
        exit()
                
            

def getKeyByNumber(keyNumber):
    for index, key in enumerate(data):
        if index == keyNumber:
            return key
    return False

def makeByte(byteinput: str):
    while len(byteinput) != 8:
        byteinput = "0" + byteinput
    return byteinput


def encript(decriptedPassword):
    if not decriptedPassword:
        return False
    bytes = []
    byteString = ""
    switchNumber = random.randint(0, len(decriptedPassword) - 1)
    
    decriptedPassword = decriptedPassword[switchNumber:] + decriptedPassword[:switchNumber]
    bytes.extend(ord(num) for num in str(switchNumber))
    for ascii in bytes:
        ascii *= 2
        byteString += bin(ascii)[2:]
        byteString = makeByte(byteString)

        
    byteString += "11111111"
    
    bytes = []
    for index, char in enumerate(decriptedPassword):
        bytes.extend(ord(num) for num in char)
        ascii = bytes[index] * 2
        bytes[index] = bin(ascii)[2:]
        if len(bytes[index]) != 8:
            bytes[index] = "0" + bytes[index]
    
    for byte in bytes:
        byteString += byte
    return byteString
    
    # shift letters by random number
    # convert to ascii
    # convert to binary
    # add together to get int

def decript(encriptedPassword):
    if not encriptedPassword:
        return False
    # 8 bits
    counter = 0
    bytes = []
    byteString = ""
    for index, bit in enumerate(encriptedPassword):
        byteString += bit
        counter += 1
        if counter == 8:
            bytes.append(byteString)
            counter = 0
            byteString = ""
    for index, byte in enumerate(bytes):
        bytes[index] = int(int(byte, 2) / 2)
        bytes[index] = chr(bytes[index])
        
    switchNumber = ""
    while True:
        if bytes[0] != "\x7f":   
            switchNumber += bytes.pop(0)
        else:
            bytes.pop(0)
            break
    decritpedPassword = ""
    for letter in bytes:
        decritpedPassword += letter
    switchNumber = len(decritpedPassword) - int(switchNumber)
    decritpedPassword = decritpedPassword[switchNumber:] + decritpedPassword[:switchNumber]
    
    return decritpedPassword
    
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
        setup["password"] = encript(passwordMaker())
        
    # beveiligingsvraag
    if setup["password"] != None:
        prompt = input("do you want safety questions in case you forget your password? (Y/N): ")
        if prompt.lower() == "y":
            safetyQuestionList = []
            safetyQuestionList.append(input("QUESTION: "))
            safetyQuestionList.append(encript(input("ANSWER: ")))
  
            setup["safetyquestion"] = safetyQuestionList
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
    print("\n1. see passwords\n2. add password\n3. delete password\n4. account list\n5. setup\n6. quit")
    prompt = input("input field: ")
    if valueError(prompt, "input was not an int"):
        continue
    prompt = int(prompt)
    if prompt == 1:
        counter = 0
        print()
        print("-~"*20)
        print("\naccounts saved: \n")
        for key in data:
            counter += 1
            print(f"\t{counter}. {key}")
        print("see password of which account?")
        accountName = input(">>> ") 
        if accountName in data:
            password = decript(data[accountName])
            print(password)
            if setup["hidetime"] != None:
                sleep(setup["hidetime"])
                whitespace = " " * len(password)
                print (f"\033[A{whitespace}\033[A")

        else:
            print("\naccount not found\n")

    if prompt == 2:
        accountName = input("accountName: ")
        password = encript(passwordMaker())
        data[accountName] = password
        with open("password keeper.json", 'w') as json_file:
            json.dump(data, json_file, indent = 4, separators=(',',': '))
        
    if prompt == 3:
        counter = 0
        print()
        for key in data:
            counter += 1
            print(f"{counter}. {key}")
        print("password list")
        accountName = input("delete account: ")
        print(f"password to delete: {accountName}")
        password = input(">>> ")
        if password == decript(data[accountName]):
            data.pop(accountName)
            print(f"\n{accountName} deleted")
        else:
            print("password incorrect\naborting...")
        with open("password keeper.json", 'w') as json_file:
            json.dump(data, json_file, indent = 4, separators=(',',': '))
        print("---------------------------------------------------------")
        
    if prompt == 4:
        counter = 0
        print()
        print("-~"*20)
        print("\naccounts saved: \n")
        for key in data:
            counter += 1
            print(f"\t{counter}. {key}")
        input("\npress enter to continue")
    if prompt == 5:
        setupKeeper()
    if prompt == 6:
        print("see you later")
        exit()



