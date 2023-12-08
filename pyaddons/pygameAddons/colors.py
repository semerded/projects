import random
class Color:
    # TODO add argb
    RED = (255, 0, 0)
    LAVARED = (255, 40, 0)
    ORANGE = (255, 80, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    OLIVEGREEN = (0, 150, 0)
    DARKGREEN = (0, 100, 0)
    TURQUISE = (0, 255, 255)
    PINK = (255, 0, 100)
    BLUE = (0, 0, 255)
    LIGHTBLUE = (0, 120, 255)
    PURPLE = (255, 0, 255)
    WHITE = (255, 255, 255)
    LESSWHITE = (200, 200, 200)
    LESSRED = (200, 0, 0)
    LESSYELLOW = (200, 200, 0)
    LESSGREEN = (0, 200, 0)
    LESSTURQUISE = (0, 200, 200)
    LESSBLUE = (0, 0, 200)
    LIGHTGRAY = LIGHTGREY = (150, 150, 150)
    GRAY = GREY = (100, 100, 100)
    DARKGRAY = DARKGREY = (50, 50, 50)
    DARKMODEGRAY = DARKMODEGREY = (30, 30, 30)
    BLACK = (0, 0, 0)

    def random():
        tuple = []
        for i in range(3):
            tuple.append(random.randint(0, 255))
        return (tuple[0], tuple[1], tuple[2])