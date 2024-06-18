import random 
import pygame, sys
import textwrap
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from scipy.io.wavfile import write as wavWrite
import time
import queue

class Screen():
    
    def __init__(self, screen_size = [16, 16]):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (140, 140, 140)
        self.PINK = (255, 0, 149)
        self.RED = (255, 0, 0)
    
        self.SCREEN_SIZE = screen_size
        self.GRID_SIZE = 16
        self.file_user_input = Path(__file__).parent / "user_input.wav"
        self.file_user_input.resolve()
        # if not self.file_user_input.exists():
        #     self.file_user_input.touch()
        self.q = queue.Queue()


    def callback(self,indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def setup_screen(self, screenNumber = 0):
        pygame.init()
        pygame.mixer.init()
        
        
        self.displaySizes = pygame.display.get_desktop_sizes()
        
        if len(self.displaySizes) >= screenNumber + 1:
            displaySizeX , displaySizeY = self.displaySizes[screenNumber]
        else:
            displaySizeX , displaySizeY = self.displaySizes[0]

        self.resize_to_resolution(displaySizeX, displaySizeY, screenNumber)

        pygame.display.set_caption("Chat_Leap")

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
        self.chat_line_offset = 18
        self.chat = ["  " for x in range(self.chat_max_len)]
        self.chat_color = [self.color_passive for x in range(self.chat_max_len)]
        self.input_rect_normal_height = 20
        self.input_rect = pygame.Rect(self.chat_horizontal_offset, self.maze_offset_y + 16 * self.CELL_SIZE - self.input_rect_normal_height, 140, self.input_rect_normal_height)
        self.maze_rect = pygame.Rect(self.maze_offset_x - 4, self.maze_offset_y - 4, 16 * self.CELL_SIZE + 6, 16 * self.CELL_SIZE + 6)
        
        self.return_text = False
        self.active = True
        self.restart_request = False
        self.reset_request = False

        self.backspace_hold = False
        
        self.author_to_color = {
            "System": self.color_active,
            "You": self.color_passive,
            "Error": self.RED
        }
        self.audio_mode = False

    def resize_to_resolution(self, res_x, res_y, monitorNumber):
        self.screen = pygame.display.set_mode([res_x, res_y], pygame.NOFRAME, display=monitorNumber)
        self.chat_horizontal_offset = round(res_x * 0.6)
        self.chat_max_len = round(res_y * 0.0375)
        self.maze_offset_x = round(res_x * 0.06)
        self.maze_offset_y = round(res_x * 0.06)
        self.CELL_SIZE = round(res_y * 0.05)
 
    def update_screen(self, maze=None, player=None, render = 17):

        self.restart_request = False
        self.reset_request = False
        self.record = False

        

        #Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.audio_mode: 
                if event.type == pygame.KEYDOWN: 
                    if event.mod & pygame.KMOD_LCTRL and event.key== pygame.K_SPACE:
                        print("ptt")
                        self.record = True
                        
                        self.record_audio()

                        self.return_text = True
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        if self.user_text != "":
                            self.return_text = True
                            self.message = self.user_text
                            self.last_response = self.response_text
                            self.add_chat_text(self.user_text, "You")
                            self.user_text = ""
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        self.backspace_hold = True
                    else:
                        self.user_text += event.unicode
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE: 
                    self.backspace_hold = False
            #Reset keys listener
            if not self.active:            
                keys = pygame.key.get_pressed()
                self.restart_request = keys[pygame.K_r]
                self.reset_request = self.restart_request and keys[pygame.K_LCTRL]

        if self.backspace_hold:
            self.user_text = self.user_text[:-1]
            time.sleep(0.1)
            
        self.screen.fill((0,0,0))
        
        if self.on_response_change():
            self.add_chat_text(self.response_text, "GPT-4")
        
        if (player and maze) != None:
            self.draw_maze(maze, player, render)
                
        pygame.draw.rect(self.screen, self.color, self.input_rect, 2)
        pygame.draw.rect(self.screen, self.color, self.maze_rect, 2)
        #self.text_surface = self.base_font.render(self.user_text, True, (255,255,255))
        self.text_title = self.title_font.render(self.title_text, True, self.color)
        self.cursor = self.base_font.render("_", True, (255,255,255))
        #self.screen.blit(self.text_surface,(self.input_rect.x + 5, self.input_rect.y + 5))
        self.screen.blit(self.text_title,(self.input_rect.x, self.input_rect.y - 15))
        #self.screen.blit(self.cursor,(self.input_rect.x + self.text_surface.get_width() + 5, self.input_rect.y + 5))
        #self.input_rect.w = max(250, self.text_surface.get_width() + 20)
        self.draw_chat_text()
        self.draw_input_text()


        pygame.display.flip()
        
    def record_audio(self):
        with sf.SoundFile(self.file_user_input, mode='wb', samplerate=44100,channels=2) as file:
            with sd.InputStream(samplerate=44100,channels=2, callback=self.callback):
                while self.record:
                    file.write(self.q.get())
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            print("end ptt")
                            self.record = False
                            
        
        
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
                    
                    
    def draw_maze(self, maze, player, render=17):
        #Maze
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                isRendered = (x - render < player.currentPosition[0] < x + render) and (y - render < player.currentPosition[1] < y + render)
                if not isRendered:
                    continue
                
                if maze[0][y][x] == 1:
                    #wall
                    pygame.draw.rect(self.screen, self.WHITE, (self.maze_offset_x + x * self.CELL_SIZE, self.maze_offset_y + y * self.CELL_SIZE, self.CELL_SIZE - 4, self.CELL_SIZE - 4))
                if player.currentPosition == [x, y] and (not player.isHidden):
                    #player
                    pygame.draw.rect(self.screen, self.color_active, (self.maze_offset_x + x * self.CELL_SIZE, self.maze_offset_y + y * self.CELL_SIZE, self.CELL_SIZE - 4, self.CELL_SIZE - 4))
                if maze[2] == [x, y]:
                    #finish
                    pygame.draw.rect(self.screen, self.RED, (self.maze_offset_x + x * self.CELL_SIZE, self.maze_offset_y + y * self.CELL_SIZE, self.CELL_SIZE - 4, self.CELL_SIZE - 4))
        
        
    def draw_chat_text(self):
        for i in range(0, self.chat_max_len):
            
            self.text_response = self.response_font.render(self.chat[i], True, self.chat_color[i])
            self.screen.blit(self.text_response, (self.chat_horizontal_offset, (self.maze_offset_y + i * self.chat_line_offset)))

    def draw_input_text(self): 
        lines = textwrap.wrap(self.user_text, 45)
        if lines == []:
            lines = [""]
        max_line = len(lines) - 1
        for i in range(len(lines)):
            rendered_line = self.base_font.render(lines[i], True, (255,255,255))
            self.screen.blit(rendered_line,(self.input_rect.x + 5, self.input_rect.y + 3 + i * self.input_rect_normal_height))
        current_line = self.base_font.render(lines[max_line], True, (255,255,255))
        first_line = self.base_font.render(lines[0], True, (255,255,255))
        self.screen.blit(self.cursor,(self.input_rect.x + current_line.get_width() + 5, self.input_rect.y + 5 + max_line * self.input_rect_normal_height))
        self.input_rect.w = max(200, first_line.get_width() + 15)
        self.input_rect.h = self.input_rect_normal_height * (max_line + 1) + 5

    def add_chat_text(self, raw_text, author):
        lines = textwrap.wrap(author + ": " + raw_text, 45)
        first_line = True
        color = self.author_to_color.get(author, self.PINK)
        for line in lines:
            for i in range(0, self.chat_max_len - 1):
                self.chat[i] = self.chat[i + 1]
                self.chat_color[i] = self.chat_color[i + 1]
            if first_line:
                self.chat[self.chat_max_len - 1] = line
                self.chat_color[self.chat_max_len - 1] = color
            else:
                self.chat[self.chat_max_len - 1] = line
                self.chat_color[self.chat_max_len - 1] = color
            first_line = False
            
    def clear_chat_text(self):
        self.chat = ["  " for x in range(self.chat_max_len)]

    def quit_screen(self): 
        pygame.quit()

    def get_user_input(self):
        return_message = self.message
        self.message = ""
        self.return_text = False
        return return_message
    
    def ppt(self):
        if not self.record:
            return True


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


    def play(self):
        file_tts_out = Path(__file__).parent / "tts_out.wav"
        file_tts_out.resolve()
        
        pygame.mixer.music.load(file_tts_out)
        
        pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(10)
        
        pygame.mixer.music.unload()

        
