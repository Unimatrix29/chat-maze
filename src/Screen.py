import pygame
import random

class Screen():
    
    def __init__(self, screen_size = [16, 16]):
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (127, 127, 127)
    
        self.SCREEN_SIZE = screen_size
        self.GRID_SIZE = 16
        self.CELL_SIZE = 30
        self.PIXEL_SIZE = 24

    def setup_screen(self):
        global screen
        pygame.init()
        screen = pygame.display.set_mode([480, 480])
        pygame.display.set_caption("Chat_Leap")
 
    def update_screen(self, maze, player, render = 16):
        screen.fill(self.BLACK)
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                isRendered = (x - render < player.currentPosition[0] < x + render) and (y - render < player.currentPosition[1] < y + render)
                if not isRendered:
                    continue
                
                if maze[0][y][x] == 1:
                    pygame.draw.rect(screen, self.WHITE, (x * self.CELL_SIZE, y * self.CELL_SIZE, self.PIXEL_SIZE, self.PIXEL_SIZE))
                if player.currentPosition == [x, y] and (not player.isHidden):
                    pygame.draw.rect(screen, self.GREY, (x * self.CELL_SIZE, y * self.CELL_SIZE, self.PIXEL_SIZE, self.PIXEL_SIZE))

        pygame.display.flip()

    """
    Returns True if player stucks against a wall
    """
    def check_wall(self, maze, playerPosition):
        return maze[0][playerPosition[1]][playerPosition[0]] == 1
    """
    Returns True if player arrived the end point of a maze
    """
    def check_finish(self, maze, playerPosition):
        if maze[2] == playerPosition:
            return True
        return False

    def quit_screen(self): 
        pygame.quit()


    def quit_screen(self):
        pygame.quit()
