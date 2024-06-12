import random 
import pygame, sys
import textwrap

class Screen():
    
    def __init__(self, screen_size = [16, 16]):
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (140, 140, 140)
        self.PINK = (255, 0, 149)
        self.RED = (255, 0, 0)
    
        self.SCREEN_SIZE = screen_size
        self.GRID_SIZE = 16
        self.CELL_SIZE = 30
        self.maze_offset_x = 60
        self.maze_offset_y = 30

    def setup_screen(self):
        pygame.init()

        #Maze
        self.screen = pygame.display.set_mode([1000, 600], pygame.NOFRAME)

        pygame.display.set_caption("Chat_Leap")
        pygame.transform.scale2x

        #Input
        self.title_font = pygame.font.SysFont('monospace821', 10)
        self.base_font = pygame.font.SysFont('monospace821', 12)
        self.response_font = pygame.font.SysFont('monospace821', 12)
        self.user_text = ""
        self.title_text = "User Input:"
        self.response_text = ""

        self.color_active = pygame.Color('limegreen')
        self.color_passive = (100, 100, 100)
        self.color = self.color_passive
        self.message = ""
        self.last_response = ""
        self.chat_line_offset = 20
        self.chat_horizontal_offset = 600
        self.chat_max_len = 24
        self.chat = ["  " for x in range(self.chat_max_len)]
        self.input_rect = pygame.Rect(self.chat_horizontal_offset, 570, 140, 24)
        self.maze_rect = pygame.Rect(self.maze_offset_x - 4, self.maze_offset_y - 4, 16 * self.CELL_SIZE + 6, 16 * self.CELL_SIZE + 6)
        
        self.help_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        self.duck_text = "____________________________________________$$$$$$______________________________________$$_____$$___________________________________$__(•)____$$_______________________________$$__________$___________________________________$$_____$____________________________________$____$______________________________________$____$__$$$__$$______$_____________________$$_____$_____$$__$$__$$$_____________________$______$___________$$__$_____________________$$_______$______$$_____$_____________________$$________$$$$$$______$_______________________$$$________________$___________________________$$$$__________$$_______________________________$$$$$$$$$$$$__________________________"

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

        self.restart_request = False
        self.reset_request = False

        #Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        if self.user_text != "":
                            self.add_chat_text(self.user_text, "You")
                            if self.user_text == "/help":
                                self.add_chat_text(self.help_text, "System")                                
                            elif self.user_text == "/restart":                                
                                self.add_chat_text("Game restarting", "System")
                                self.restart_request = True                                
                            elif self.user_text == "/reset":
                                self.add_chat_text("Game reset", "System")
                                self.reset_request = True                               
                            elif self.user_text == "/duck":
                                self.add_chat_text(self.duck_text, "System")
                            else:
                                self.return_text = True
                                self.message = self.user_text
                                self.last_response = self.response_text
                                self.add_chat_text(self.user_text, "You")
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
        
        if self.on_response_change():
            self.add_chat_text(self.response_text, "GPT-4")
            
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
        pygame.draw.rect(self.screen, self.color, self.maze_rect, 2)
        self.text_surface = self.base_font.render(self.user_text, True, (255,255,255))
        self.text_title = self.title_font.render(self.title_text, True, self.color)
        self.cursor = self.base_font.render("_", True, (255,255,255))
        self.screen.blit(self.text_surface,(self.input_rect.x + 5, self.input_rect.y + 5))
        self.screen.blit(self.text_title,(self.input_rect.x, self.input_rect.y - 15))
        self.screen.blit(self.cursor,(self.input_rect.x + self.text_surface.get_width() + 5, self.input_rect.y + 5))
        self.input_rect.w = max(250, self.text_surface.get_width() + 20)
        self.draw_chat_text()


        pygame.display.flip()

    def draw_chat_text(self):
        color = self.color_passive
        for i in range(0, self.chat_max_len):
            if self.chat[i][0] == "Y":
                color = self.color_passive
            if self.chat[i][0] == "G": 
                color = self.PINK
            if self.chat[i][0] == "S": 
                color = self.color_active
            self.text_response = self.response_font.render(self.chat[i], True, color)
            self.screen.blit(self.text_response, (self.chat_horizontal_offset, (self.maze_offset_y + i * self.chat_line_offset)))

    def add_chat_text(self, raw_text, author):
        lines = textwrap.wrap(author + ": " + raw_text, 45)
        first_line = True
        for line in lines:
            for i in range(0, self.chat_max_len - 1):
                self.chat[i] = self.chat[i + 1]
            if first_line:
                self.chat[self.chat_max_len - 1] = line
            else:
                self.chat[self.chat_max_len - 1] = line
            first_line = False
            
    def clear_chat_text(self):
        self.chat = ["  " for x in range(self.chat_max_len)]

    def quit_screen(self): 
        pygame.quit()

    def get_user_input(self):
        return self.message
    
    def on_return(self):
        if self.return_text:
            self.return_text = False
            return True
        return False
    
    
    def has_restart_request(self):
        return self.restart_request
    
    def has_reset_request(self):
        return self.reset_request
    
    def on_response_change(self):
        if self.response_text != self.last_response:
            self.last_response = self.response_text
            return True
        return False

