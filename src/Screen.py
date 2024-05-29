import random 
import pygame, sys

class Screen():
    
    def __init__(self, screen_size = [16, 16]):
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (127, 127, 127)
    
        self.SCREEN_SIZE = screen_size
        self.GRID_SIZE = 16
        self.CELL_SIZE = 30

    def setup_screen(self):
        pygame.init()

        #Maze
        self.screen = pygame.display.set_mode([480, 560])
        pygame.display.set_caption("Chat_Leap")

        #Input
        self.title_font = pygame.font.Font(None, 16)
        self.base_font = pygame.font.Font(None, 32)
        self.user_text = "bitte geh nach unten"
        self.title_text = "Input your message to ChatGPT:"

        self.input_rect = pygame.Rect(10, 520, 140, 32)
        self.color_active = pygame.Color('limegreen')
        self.color_passive = pygame.Color('gray15')
        self.color = self.color_passive
        self.message = ""
        
        self.return_text = False
        self.active = True

    def draw_wall(self, surface, color, x, y, size, maze):
        half = size / 2
        quarter = size / 4
        pygame.draw.circle(surface, color, (x * size + half, y * size + half), half)
        
        
        pygame.draw.rect(surface, color, (x + quarter, y + quarter, half, half))
        
 
    def update_screen(self, maze, player, render = 16):

        #Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.return_text = True
                        self.message = self.user_text
                        self.user_text = ""
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode

            self.screen.fill((0,0,0))
            
            
            #Maze
            for y in range(self.GRID_SIZE):
                for x in range(self.GRID_SIZE):
                    isRendered = (x - render < player.currentPosition[0] < x + render) and (y - render < player.currentPosition[1] < y + render)
                    if not isRendered:
                        continue
                    
                    if maze[0][y][x] == 1:
                        #pygame.draw.rect(self.screen, self.WHITE, (x * self.CELL_SIZE, y * self.CELL_SIZE, self.PIXEL_SIZE, self.PIXEL_SIZE))
                        self.draw_wall(self.screen, self.WHITE, x, y, self.CELL_SIZE, maze)
                    if player.currentPosition == [x, y] and (not player.isHidden):
                        pygame.draw.rect(self.screen, self.GREY, (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

                if self.active:
                    self.color = self.color_active
                else:
                    self.color = self.color_passive

            pygame.draw.rect(self.screen, self.color, self.input_rect, 2)
            self.text_surface = self.base_font.render(self.user_text, True, (255,255,255))
            self.text_title = self.title_font.render(self.title_text, True, self.color)
            self.screen.blit(self.text_surface,(self.input_rect.x + 5, self.input_rect.y + 5))
            self.screen.blit(self.text_title,(10, 500))
            self.input_rect.w = max(10, self.text_surface.get_width() + 10)

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

    def get_user_input(self):
        return self.message
    
    def on_return(self):
        if self.return_text:
            self.return_text = False
            return True
        return False
    
    
