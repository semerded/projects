try:
    import pygame
except ImportError:
    raise ImportError("import pygame")
import random, sys

pygame.init()
pygame.font.init()
screenInfo = pygame.display.Info()

class color:
    RED = (255,0,0)
    LAVARED = (255,40,0)
    ORANGE = (255,80,0)
    YELLOW = (255,255,0)
    GREEN = (0,255,0)
    OLIVEGREEN = (0,150,0)
    DARKGREEN = (0,100,0)
    TURQUISE = (0,255,255)
    PINK = (255,0,100)
    BLUE = (0,0,255)
    LIGHTBLUE = (0,120,255)
    PURPLE = (255,0,255)
    WHITE = (255,255,255)
    LESSWHITE = (200,200,200)
    LESSRED = (200,0,0)
    LESSYELLOW = (200,200,0)
    LESSGREEN = (0,200,0)
    LESSTURQUISE = (0,200,200)
    LESSBLUE = (0,0,200)
    LIGHTGRAY = LIGHTGREY = (150,150,150)
    GRAY = GREY = (100,100,100)
    DARKGRAY = DARKGREY = (50,50,50)
    DARKMODEGRAY = DARKMODEGREY = (30,30,30)
    BLACK = (0,0,0)
    
    def random():
        tuple = []
        for i in range(3):
            tuple.append(random.randint(0, 255))
        return (tuple[0], tuple[1], tuple[2])
    
class font:
    H1 = pygame.font.SysFont(pygame.font.get_default_font(), 34)
    H2 = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    H3 = pygame.font.SysFont(pygame.font.get_default_font(), 24)
    H4 = pygame.font.SysFont(pygame.font.get_default_font(), 20)
    H5 = pygame.font.SysFont(pygame.font.get_default_font(), 18)
    H6 = pygame.font.SysFont(pygame.font.get_default_font(), 16)
    XXSMALL = pygame.font.SysFont(pygame.font.get_default_font(), 8)
    XSMALL = pygame.font.SysFont(pygame.font.get_default_font(), 12)
    SMALL = pygame.font.SysFont(pygame.font.get_default_font(), 14)
    MEDIUM = pygame.font.SysFont(pygame.font.get_default_font(), 28)
    LARGE = pygame.font.SysFont(pygame.font.get_default_font(), 38)
    XLARGE = pygame.font.SysFont(pygame.font.get_default_font(), 46)
    XXLARGE = pygame.font.SysFont(pygame.font.get_default_font(), 60)
    XXXLARGE = pygame.font.SysFont(pygame.font.get_default_font(), 72)
    FONT50 = pygame.font.SysFont(pygame.font.get_default_font(), 50)
    FONT100 = pygame.font.SysFont(pygame.font.get_default_font(), 100)
    FONT150 = pygame.font.SysFont(pygame.font.get_default_font(), 150)
    
    def customFont(size, font = None):
        if font == None:
            return pygame.font.SysFont(pygame.font.get_default_font(), size)
        else:
            return pygame.font.SysFont(font, size)


class App():
    def __init__(self, screenWidth, screenHeight, *flags) -> None:
        self.APPdisplay = pygame.display.set_mode((screenWidth, screenHeight) ,*flags)
        self.__userInputs = {"keyDown": None, "keyUp": None, "mouseAction": None, "mouseUp": None, "controller": None}
        self.__mouseAction = {"click": False, "motion": False, "scroll": False}
        self.__callkeys = {
            "keyboard": {
                pygame.K_a: ["a", "A", "key_a", "key_A", "KEY_a", "KEY_A", "keya", "keyA", "k_a", "k_A", "K_a", "K_A"],
                pygame.K_b: ["b", "B", "key_b", "key_B", "KEY_b", "KEY_B", "keyb", "keyB", "k_b", "k_B", "K_b", "K_B"],
                pygame.K_c: ["c", "C", "key_c", "key_C", "KEY_c", "KEY_C", "keyc", "keyC", "k_c", "k_C", "K_c", "K_C"],
                pygame.K_d: ["d", "D", "key_d", "key_D", "KEY_d", "KEY_D", "keyd", "keyD", "k_d", "k_D", "K_d", "K_D"],
                pygame.K_e: ["e", "E", "key_e", "key_E", "KEY_e", "KEY_E", "keye", "keyE", "k_e", "k_E", "K_e", "K_E"],
                pygame.K_f: ["f", "F", "key_f", "key_F", "KEY_f", "KEY_F", "keyf", "keyF", "k_f", "k_F", "K_f", "K_F"],
                pygame.K_g: ["g", "G", "key_g", "key_G", "KEY_g", "KEY_G", "keyg", "keyG", "k_g", "k_G", "K_g", "K_G"],
                pygame.K_h: ["h", "H", "key_h", "key_H", "KEY_h", "KEY_H", "keyh", "keyH", "k_h", "k_H", "K_h", "K_H"],
                pygame.K_i: ["i", "I", "key_i", "key_I", "KEY_i", "KEY_I", "keyi", "keyI", "k_i", "k_I", "K_i", "K_I"],
                pygame.K_j: ["j", "J", "key_j", "key_J", "KEY_j", "KEY_J", "keyj", "keyJ", "k_j", "k_J", "K_j", "K_J"],
                pygame.K_k: ["k", "K", "key_k", "key_K", "KEY_k", "KEY_K", "keyk", "keyK", "k_k", "k_K", "K_k", "K_K"],
                pygame.K_l: ["l", "L", "key_l", "key_L", "KEY_l", "KEY_L", "keyl", "keyL", "k_l", "k_L", "K_l", "K_L"],
                pygame.K_m: ["m", "M", "key_m", "key_M", "KEY_m", "KEY_M", "keym", "keyM", "k_m", "k_M", "K_m", "K_M"],
                pygame.K_n: ["n", "N", "key_n", "key_N", "KEY_n", "KEY_N", "keyn", "keyN", "k_n", "k_N", "K_n", "K_N"],
                pygame.K_o: ["o", "O", "key_o", "key_O", "KEY_o", "KEY_O", "keyo", "keyO", "k_o", "k_O", "K_o", "K_O"],
                pygame.K_p: ["p", "P", "key_p", "key_P", "KEY_p", "KEY_P", "keyp", "keyP", "k_p", "k_P", "K_p", "K_P"],
                pygame.K_q: ["q", "Q", "key_q", "key_Q", "KEY_q", "KEY_Q", "keyq", "keyQ", "k_q", "k_Q", "K_q", "K_Q"],
                pygame.K_r: ["r", "R", "key_r", "key_R", "KEY_r", "KEY_R", "keyr", "keyR", "k_r", "k_R", "K_r", "K_R"],
                pygame.K_s: ["s", "S", "key_s", "key_S", "KEY_s", "KEY_S", "keys", "keyS", "k_s", "k_S", "K_s", "K_S"],
                pygame.K_t: ["t", "T", "key_t", "key_T", "KEY_t", "KEY_T", "keyt", "keyT", "k_t", "k_T", "K_t", "K_T"],
                pygame.K_u: ["u", "U", "key_u", "key_U", "KEY_u", "KEY_U", "keyu", "keyU", "k_u", "k_U", "K_u", "K_U"],
                pygame.K_v: ["v", "V", "key_v", "key_V", "KEY_v", "KEY_V", "keyv", "keyV", "k_v", "k_V", "K_v", "K_V"],
                pygame.K_w: ["w", "W", "key_w", "key_W", "KEY_w", "KEY_W", "keyw", "keyW", "k_w", "k_W", "K_w", "K_W"],
                pygame.K_x: ["x", "X", "key_x", "key_X", "KEY_x", "KEY_X", "keyx", "keyX", "k_x", "k_X", "K_x", "K_X"],
                pygame.K_y: ["y", "Y", "key_y", "key_Y", "KEY_y", "KEY_Y", "keyy", "keyY", "k_y", "k_Y", "K_y", "K_Y"],
                pygame.K_z: ["z", "Z", "key_z", "key_Z", "KEY_z", "KEY_Z", "keyz", "keyZ", "k_z", "k_Z", "K_z", "K_Z"],
            }
        }
        self.__event = None
        
    def __center__(self):
        pass
    
    def keyboard(self, callkey, keyDown: bool = True):
        direction = "keyDown" if keyDown else "keyUp"
        if self.__event.key == callkey:
            for call in self.__callkeys['keyboard'][callkey]:
                if call in self.__userInputs[direction]:
                    self.__fire__(call, direction)
                    break  
        
    def eventHandeler(self, events, *inputs):
        """
        handles all events in game
        checks if a key is pressed or the mouse has moved
        """
  
        for event in events:
            self.__event = event

            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and self.__userInputs["keyDown"] != None:
                self.keyboard(pygame.K_a)
                self.keyboard(pygame.K_b)
                self.keyboard(pygame.K_c)
                self.keyboard(pygame.K_d)
                self.keyboard(pygame.K_e)
                self.keyboard(pygame.K_f)
                self.keyboard(pygame.K_g)
                self.keyboard(pygame.K_h)
                self.keyboard(pygame.K_i)
                self.keyboard(pygame.K_j)
                self.keyboard(pygame.K_k)
                self.keyboard(pygame.K_l)
                self.keyboard(pygame.K_m)
                self.keyboard(pygame.K_n)
                self.keyboard(pygame.K_o)
                self.keyboard(pygame.K_p)
                self.keyboard(pygame.K_q)
                self.keyboard(pygame.K_r)
                self.keyboard(pygame.K_s)
                self.keyboard(pygame.K_t)
                self.keyboard(pygame.K_u)
                self.keyboard(pygame.K_v)
                self.keyboard(pygame.K_w)
                self.keyboard(pygame.K_x)
                self.keyboard(pygame.K_y)
                self.keyboard(pygame.K_z)
            
            if event.type == pygame.KEYUP and self.__userInputs["keyUp"] != None:
                self.keyboard(pygame.K_a, False)
                self.keyboard(pygame.K_b, False)
                self.keyboard(pygame.K_c, False)
                self.keyboard(pygame.K_d, False)
                self.keyboard(pygame.K_e, False)
                self.keyboard(pygame.K_f, False)
                self.keyboard(pygame.K_g, False)
                self.keyboard(pygame.K_h, False)
                self.keyboard(pygame.K_i, False)
                self.keyboard(pygame.K_j, False)
                self.keyboard(pygame.K_k, False)
                self.keyboard(pygame.K_l, False)
                self.keyboard(pygame.K_m, False)
                self.keyboard(pygame.K_n, False)
                self.keyboard(pygame.K_o, False)
                self.keyboard(pygame.K_p, False)
                self.keyboard(pygame.K_q, False)
                self.keyboard(pygame.K_r, False)
                self.keyboard(pygame.K_s, False)
                self.keyboard(pygame.K_t, False)
                self.keyboard(pygame.K_u, False)
                self.keyboard(pygame.K_v, False)
                self.keyboard(pygame.K_w, False)
                self.keyboard(pygame.K_x, False)
                self.keyboard(pygame.K_y, False)
                self.keyboard(pygame.K_z, False)
                
            if self.__userInputs["mouseAction"] != None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and "LMB" in self.__userInputs["mouseAction"]:
                        self.__fire__("LMB", "mouseAction")
                    
                    elif event.button == 2 and "p":
                        pass
                    
            
                if event.type == pygame.MOUSEBUTTONUP and "up" in self.__userInputs["mouseAction"]:
                    self.__fire__("up", "mouseAction")
                
                if event.type == pygame.MOUSEMOTION and "motion" in self.__userInputs["mouseAction"]:
                    self.__fire__("motion", "mouseAction")
                
                if event.type == pygame.MOUSEWHEEL and "scroll" in self.__userInputs["mouseAction"]:
                    self.__fire__("scroll", "mouseAction")
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__mouseAction["click"] = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                self.__mouseAction["click"] = False
            
            if event.type == pygame.MOUSEMOTION:
                self.__mouseAction["motion"] = True
            else:
                self.__mouseAction["motion"] = False
            
            if event.type == pygame.MOUSEWHEEL:
                self.__mouseAction["scroll"] = True
            else:
                self.__mouseAction["scroll"] = False
            
            
    def __fire__(self, input: str, type: str):
        try:
            self.__userInputs[type][input]()
        except:
            print("function on input '%s' could not be fired" % input)
    
                
    def __assembler__(self, type:str, kwargs):
        self.__userInputs[type] = kwargs
    
    def keyDown(self, **kwargs):
        self.__assembler__("keyDown", kwargs)
        
    def keyUp(self, **kwargs):
        self.__assembler__("keyUp", kwargs)
    
    def mouseAction(self, **kwargs):
        self.__assembler__("mouseAction", kwargs)

    

    @property
    def maindisplay(self) -> pygame.surface:
        return self.APPdisplay            
    
    @property
    def mouseButton(self) -> bool:
        return self.__mouseAction["click"]
    
    class text:
        def __init_subclass__(cls,
                              ) -> None:
            pass
        
        def place(self):
            pass
        
    class update:
        pass


class screenUnit:
    pass
    
class button:
    def __init__(self,
                 size: tuple[screenUnit,screenUnit],
                 textColor: tuple[int,int,int] = color.BLACK,
                 bgColor: tuple[int,int,int] = color.LESSWHITE,
                 borderTickness: int = 2,
                 borderColor: tuple[int,int,int] = color.BLACK,
                 borderRadius: int = 0,
                 onClick = ...,
                 onHold = ...,
                 onHover = ...,
                 colorOnHover: tuple[int,int,int] = ...,
                 
                 
                 ) -> None:
        print(onClick)

    def __text__(self):
        ...
        
    def __border__(self):
        ...
    
    def __radius__(self):
        ...
        
    def __resize__(self):
        ...
    
    def __recolor__(self):
        ...
        
    def onMouseOver(self):
        ...
        
    def onMouseClick(self):
        ...
        
    def onMouseHold(self):
        ...
    
    def changeColorOnHover(self):
        ...
        
    def place(self):
        ...
        
    
        
    
class text:
    def __init__(self) -> None:
        pass
    
    def centerd(self):
        ...
        
    

class textbox:
    def __init__(self) -> None:
        pass
    
 
    
