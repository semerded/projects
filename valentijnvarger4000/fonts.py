import pygame
pygame.font.init()

class Font:
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

    def customFont(size, font=None):
        if font == None:
            return pygame.font.SysFont(pygame.font.get_default_font(), size)
        else:
            return pygame.font.SysFont(font, size)
