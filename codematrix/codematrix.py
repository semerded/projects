from time import sleep
from random import randint
import os
nonlist = [127,129,141,143,144,157,160,173,182]
while True:
    os.system('color 2')
    string = ""
    bereik_teller = 0
    bereik = randint(10,200)
    while bereik_teller < bereik:
        rand = randint(0,255)
        if rand > 32 and not rand in nonlist:
            string += chr(rand)
            bereik_teller += 1
    print(string)
    sleep(0.07)