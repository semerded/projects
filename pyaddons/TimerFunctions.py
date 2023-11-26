import time, threading


def ctime():
    return time.ctime()



def setTimeOut(delay: float, function, args: tuple = None):
    if args == None:
        timer = threading.Timer(delay, function)
    else:
        timer = threading.Timer(delay, function, args=args)
    timer.start()
   


def repeatInit(delay, function, *args):
    while True:
        function(*args)
        time.sleep(delay)    

def repeatEvery(seconds: float, function, args: tuple = None):
    if args == None:
        repeatThread = threading.Thread(target=repeatInit, args=(seconds, function))
    else:
        repeatThread = threading.Thread(target=repeatInit, args=(seconds, function, args))
    repeatThread.start()


def hello(name):
    print("fgjfkfhjdgsfqddshgdjfghsdgfhdjg;hjfdgs ", name)
# repeatEvery(1, hello)

setTimeOut(3, hello, ("sem"))