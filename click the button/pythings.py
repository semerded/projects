import random




klinkers = "aeuio"
alphabet = "abcdefghijklmnopqrstuvwxyz"
nummers = "1234567890"




def kleiner_dan(getal, kleiner_dan_getal):
    """
zal True terug geven als getal2 kleiner is dan getal1
    """
    if kleiner_dan_getal < getal:
        return True
    else:
        return False


def groter_dan(getal, groter_dan_getal):
    """
zal True terug geven als getal2 groter is dan getal1
    """
    if groter_dan_getal > getal:
        return True
    else:
        return False
    

def gelijk_aan(getal, gelijk_aan_getal):
    """
zal True terug geven als beide getallen gelijk zijn
    """
    if gelijk_aan_getal == getal:
        return True
    else: 
        return False
    

def value_error(waarde):
    """
zal True terug geven als de waarde geen integer is
zal False terug geven als de waarde wel een integer is
    """
    try:
        int(waarde)
    except ValueError:
        return True
    else:
        return False

 
def Y_N(input):
    """
zal True terug geven als de input y of Y is
zal False terug geven bij elk ander antwoord
    """
    if input.upper() == "Y":
        return True
    else:
        return False
    

def change(input: bool):
    """
geeft de ingegeven bool terug in de tegenovergestelde status    
    """
    if input:
        return False
    else:
        return True


def random_string(*string: str):
    """
geeft een random string terug uit de gegeven strings
    """
    r_getal = random.randint(1,len(string))
    return string[r_getal - 1]


def random_string_uitzondering(uitzondering_lijst: list, *string: str): 
    """
geeft een random string terug uit de gevegen strings als deze niet in de lijst zit\n
zal False terug geven als alle strings in de lijst aanwezig zijn
    """
    while True:
        r_getal = truerandom(1, len(string))
        if not string[r_getal - 1] in uitzondering_lijst:
            return string[r_getal - 1]            
        if all(item in uitzondering_lijst for item in list(string)):
            return False
        

def random_lijst(lijst: list):
    """
geeft een random waarde in de lijst terug
    """
    random_lijst = random.randint(1, len(lijst))
    return lijst[random_lijst - 1]

  
def list_contains(List1, List2): 
    """
zoekt of er een of meerdere waardes van lijst 1 in lijst 2 aanwezig is
    """
    check = False
    for m in List1: 
        for n in List2: 
            if m == n: 
                check = True
                return check  
    return check 
      
 
def random_lijst_uitzondering(lijst: list, uitzondering_lijst: list):
    """
geeft een random waarde uit de lijst terug als deze niet voorkomt in de uitzonderingslijst
    """
    while True:
        r_getal = truerandom(1,len(lijst))
        if not lijst[r_getal - 1] in uitzondering_lijst:
            return lijst[r_getal - 1]
        if all(item in uitzondering_lijst for item in lijst):
            return False
        


def truerandom(begingetal: int, eindgetal: int):
    """
geef een getal terug dat zeer random is door het getal een random aantal keer te randomizen    
    """
    getal = 0
    aantal = random.randint(1, random.randint(1,10))
    for i in range(aantal):
        getal = random.randint(begingetal, eindgetal)
    return getal


def snelheid(afstand_kilometer: float, tijd_minuten: float):
    """
geef de afstand in kilometer in en de tijd in minuten en berekent de km/h
gebruik voor kommagetallen een punt ipv een komma!
    """
    x = 60 / tijd_minuten
    kmh = x * afstand_kilometer
    return kmh

    

"""----------------------"""
"""temperatuur conversies"""
"""----------------------"""

def F_to_C(temperatuur: float):
    """
zet graden Farenheit naar graden Celcius om
    """
    return((temperatuur - 32) * (5/9))

def C_to_F(temperatuur: float):
    """
zet graden Celcius naar graden Farenheit om
    """
    return((temperatuur * 9/5) + 32)

def C_to_K(temperatuur: float):
    """
zet graden Celcius naar Kelvin om
    """
    return(temperatuur + 273.15)

def K_to_C(temperatuur: float):
    """
zet Kelvin om naar graden Celcius
    """
    return(temperatuur - 273.15)

def F_to_K(temperatuur: float):
    """
zet graden Farenheit om naar Kelvin
    """
    temp = F_to_C(temperatuur)
    return(C_to_K(temp))

def K_to_F(temperatuur: float):
    """
zet Kelvin om naar graden Farenheit
    """
    temp = K_to_C(temperatuur)
    return(C_to_F(temp))



