import pygame

#setup pygame window
pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("chat_leap")

#16x16 display
screen_width = 16
screen_height = 16
screen = [[0 for x in range(screen_width)] for y in range(screen_height)] 
