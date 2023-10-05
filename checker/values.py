import pygame

WIDTH, HEIGHT = 800, 800 #board size
ROWS, COLUMNS = 8,8 # board pattern 8x8
SQUARE = WIDTH//COLUMNS #square size


#colors(RGB)
BLACK = (0,0,0)
WHITE = (245,255,250)
SILK = 	(245,222,179)
BLUE = (65,105,225)
DARKBLUE = (0,0,156)
GREEN = (0,250,154)
GREY = (169,169,169)
CASTANHO = (160,82,45)
BROWN = (160,82,45)
RED = (140,23,23)
MADEIRA = (210,180,140)

KING = pygame.transform.scale(pygame.image.load('assets/coroa4.png'), (90,50)) #crow.png
