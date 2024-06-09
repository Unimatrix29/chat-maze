import random 
import pygame, sys

class Screen():
    
    def __init__(self, screen_size = [16, 16]):
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (127, 127, 127)
        self.PINK = (199,21,133)
        self.RED = (255, 0, 0)
    
        self.SCREEN_SIZE = screen_size
        self.GRID_SIZE = 16
        self.CELL_SIZE = 30
        self.maze_offset_x = 60
        self.maze_offset_y = 30

    def setup_screen(self):
        pygame.init()

        #Maze
        self.screen = pygame.display.set_mode([600, 600], pygame.NOFRAME)

        pygame.display.set_caption("Chat_Leap")

        #Input
        self.title_font = pygame.font.Font(None, 16)
        self.base_font = pygame.font.Font(None, 24)
        self.response_font = pygame.font.Font(None, 16)
        self.user_text = ""
        self.title_text = "Input your message to ChatGPT:"
        self.response_text = "-----"

        self.input_rect = pygame.Rect(10, 540, 140, 24)
        self.color_active = pygame.Color('limegreen')
        self.color_passive = pygame.Color('gray15')
        self.color = self.color_passive
        self.message = ""
        
        self.return_text = False
        self.active = True
        self.restart_request = False
        self.reset_request = False

    def draw_wall(self, surface, color, x, y, size, maze):
        half = size / 2
        quarter = size / 4
        if maze[0][x][y] == 1:
            pygame.draw.circle(surface, color, (x * size + half, y * size + half), half)
            if x < 15:
                if maze[0][x+1][y] == 1:
                    pygame.draw.rect(surface, color, (x * size + size, y * size, half, size))
            if x > 0:        
                if maze[0][x-1][y] == 1:
                    pygame.draw.rect(surface, color, (x * size - half, y * size, half, size))
            if y < 15:
                if maze[0][x][y+1] == 1:
                    pygame.draw.rect(surface, color, (x * size, y * size + size, size, half))
            if y > 0:        
                if maze[0][x][y-1] == 1:
                    pygame.draw.rect(surface, color, (x * size , y * size - half, size, half))

        
 
    def update_screen(self, maze, player, render = 16):

        #Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        if self.user_text != "":
                            self.return_text = True
                            self.message = self.user_text
                            self.user_text = ""
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode
            #Reset keys listener
            if not self.active:            
                keys = pygame.key.get_pressed()
                self.restart_request = keys[pygame.K_r]
                self.reset_request = self.restart_request and keys[pygame.K_LCTRL]
            
        self.screen.fill((0,0,0))
            
            
        #Maze
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                isRendered = (x - render < player.currentPosition[0] < x + render) and (y - render < player.currentPosition[1] < y + render)
                if not isRendered:
                    continue
                
                if maze[0][y][x] == 1:
                    pygame.draw.rect(self.screen, self.WHITE, (self.maze_offset_x + x * self.CELL_SIZE, self.maze_offset_y + y * self.CELL_SIZE, self.CELL_SIZE - 4, self.CELL_SIZE - 4))
                #self.draw_wall(self.screen, self.WHITE, x, y, self.CELL_SIZE, maze)
                if player.currentPosition == [x, y] and (not player.isHidden):
                    pygame.draw.rect(self.screen, self.color_active, (self.maze_offset_x + x * self.CELL_SIZE, self.maze_offset_y + y * self.CELL_SIZE, self.CELL_SIZE - 4, self.CELL_SIZE - 4))
                if maze[2] == [x, y]:
                    pygame.draw.rect(self.screen, self.RED, (self.maze_offset_x + x * self.CELL_SIZE, self.maze_offset_y + y * self.CELL_SIZE, self.CELL_SIZE - 4, self.CELL_SIZE - 4))
            #for y in range(self.GRID_SIZE):
            #    for x in range(self.GRID_SIZE):
                
        pygame.draw.rect(self.screen, self.color, self.input_rect, 2)
        self.text_surface = self.base_font.render(self.user_text, True, (255,255,255))
        self.text_title = self.title_font.render(self.title_text, True, self.color)
        self.screen.blit(self.text_surface,(self.input_rect.x + 5, self.input_rect.y + 5))
        self.screen.blit(self.text_title,(10, 520))
        self.input_rect.w = max(10, self.text_surface.get_width() + 20)
        self.write_response()

        pygame.display.flip()

    def quit_screen(self): 
        pygame.quit()

    def get_user_input(self):
        return self.message
    
    def on_return(self):
        if self.return_text:
            self.return_text = False
            return True
        return False
    
    def write_response(self):
        self.text_response = self.response_font.render("ChatGPT: " + self.response_text, True, self.PINK)
        self.screen.blit(self.text_response,(10, 580))
    
    def has_restart_request(self):
        return self.restart_request
    
    def has_reset_request(self):
        return self.reset_request