import random 
import pygame, sys
import textwrap
import sounddevice as sd
import soundfile as sf
from Colors import Colors
from pathlib import Path
from scipy.io.wavfile import write as wavWrite
import time
import queue

class Screen():
    
    def __init__(self):

        # setup tts-file
        self.file_user_input = Path(__file__).parent / "user_input.wav"
        self.file_user_input.resolve()
        self.q = queue.Queue()

    def update_screen(self, maze=None, player=None, render = 17):
        
        self.restart_request = False
        self.reset_request = False
        self.record = False
        
        # makes background black
        self.screen.fill(Colors.BLACK.value)

        self.__trigger_game_events()
        self.__delete_input_listener()
        self.__chatgpt_response_listener()
        self.__draw_maze(maze, player, render)  
        self.__draw_maze_border()
        self.__draw_chat_text()
        self.__draw_input_text()



        # updates pygame
        pygame.display.flip()

    def __draw_maze_border(self):

        # draws border around the maze
        pygame.draw.rect(self.screen, Colors.WHITE.value, self.maze_rect, 2)

    def __draw_input_border(self):

        # draws border around the input field
        pygame.draw.rect(self.screen, Colors.WHITE.value, self.input_rect, 2)

    def __chatgpt_response_listener(self):

        # detects a change in chatgpts response 
        if self.__on_response_change():

            # adds the new response to the chat with a "author" as parameter, that translates to a certain color
            self.add_chat_text(self.response_text, "GPT-4")

    def __trigger_game_events(self):

        # pygame event loop that detects the ingame-inputs from the user, than triggers associated methods
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit_game()
                
            if event.type == pygame.KEYDOWN:
                if self.audio_mode:
                    if event.mod & pygame.KMOD_LCTRL and event.key== pygame.K_SPACE:
                        self.__record_audio()
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.__return_input()
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        self.__on_backspace(True)
                    else:
                        self.add_char_to_input(event.unicode)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE: 
                    self.__on_backspace(False)
    
    def __quit_game(self):

        # quits pygame app and game logic
        self.__quit_screen()
        sys.exit()

    def add_char_to_input(self, char):

        # adds handed over char to the current input text in the input box
        self.user_text += char

    def __on_backspace(self, state):

        # sets backspace hold switch
        self.backspace_hold = state

    def __delete_input_listener(self, interval = 0.05):
        # detects if backspace is hold, than deletes last char in input box every [interval] seconds
        if self.backspace_hold:
            self.user_text = self.user_text[:-1]
            time.sleep(0.05)
    
    def __return_input(self):

        # checks if there is input text to return
        if self.user_text != "":

            # sets return_text so __on_return()-method can transfer return event to other classes
            self.return_text = True

            # message stores user input to hand over to chatgpt
            self.message = self.user_text

            # stores last chatgpt response so _on_response_change() can detect changes
            self.last_response = self.response_text

            # displays returned input in chat
            self.add_chat_text(self.user_text, "You")

            # resets input field
            self.user_text = ""

    def __callback(self,indata, frames, time, status):

        # This is called (from a separate thread) for each audio block
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def setup_screen(self, screenNumber = 0):

        pygame.init()
        pygame.mixer.init()
        
        # get size of all connected screens
        self.displaySizes = pygame.display.get_desktop_sizes()
        
        # choosing the right screen based on the screen number and the number of connected screens
        if len(self.displaySizes) >= screenNumber + 1:
            displaySizeX , displaySizeY = self.displaySizes[screenNumber]
        else:
            displaySizeX , displaySizeY = self.displaySizes[0]
            screenNumber = 0

        # adapts UI Elements to current screen resolution
        self.__resize_to_resolution(displaySizeX, displaySizeY, screenNumber)

        pygame.display.set_caption("Chat_Leap")

        # declares fonts
        self.title_font = pygame.font.SysFont('monospace821', 14)
        self.base_font = pygame.font.SysFont('monospace821', 16)
        self.response_font = pygame.font.SysFont('monospace821', 16)
        
        # declares dynamic text holders as empty
        self.user_text = ""
        self.response_text = ""
        self.message = ""
        self.last_response = ""

        # UI Elements Design
        self.chat_line_offset = 18
        self.chat = ["  " for x in range(self.chat_max_len)]
        self.chat_color = [Colors.GREY.value for x in range(self.chat_max_len)]
        self.input_rect_normal_height = 20
        self.input_rect = pygame.Rect(self.chat_horizontal_offset, self.maze_offset_y + 16 * self.CELL_SIZE - self.input_rect_normal_height, 140, self.input_rect_normal_height)
        self.maze_rect = pygame.Rect(self.maze_offset_x - 4, self.maze_offset_y - 4, 16 * self.CELL_SIZE + 6, 16 * self.CELL_SIZE + 6)
        
        # sets up state systems for event-methods and overlap prevention
        self.return_text = False
        self.active = True
        self.restart_request = False
        self.reset_request = False
        self.backspace_hold = False

        # text above Input Box
        self.title_text = "User Input:"
        self.__draw_input_box_title()
        
        # Dictionary that associates Authors with colors displayed in the chat
        self.personality_to_color = {
            "##### ": Colors.PINK.value,
            "System": Colors.LIMEGREEN.value,
            "You"   : Colors.GREY.value,
            "Prinz Reginald": Colors.YELLOW.value,
            "Larry" : Colors.CYAN.value,
            "Clyde" : Colors.BLUE.value,
            "Lawrie": Colors.ORANGE.value,
            "Imane" : Colors.PINK.value,
            "Sophia": Colors.GREEN.value,
            "Error" : Colors.RED.value
        }
        self.audio_mode = False

    def __resize_to_resolution(self, res_x, res_y, monitorNumber):

        # calculates UI Elements offsets and parameters based on screen resolution
        self.screen = pygame.display.set_mode([res_x, res_y], pygame.NOFRAME, display=monitorNumber)
        self.chat_horizontal_offset = round(res_x * 0.6)
        self.chat_max_len = round(res_y * 0.0375)
        self.maze_offset_x = round(res_x * 0.06)
        self.maze_offset_y = round(res_x * 0.06)
        self.CELL_SIZE = round(res_y * 0.05)

    def __draw_input_box_title(self):
        self.text_title = self.title_font.render(self.title_text, True, Colors.GREY.value)
        self.screen.blit(self.text_title,(self.input_rect.x, self.input_rect.y - 15))
    
    def __record_audio(self):

        # writes recorded audio in push-to-talk file
        print("ptt")
        self.record = True
        with sf.SoundFile(self.file_user_input, mode='wb', samplerate=44100,channels=2) as file:
            with sd.InputStream(samplerate=44100,channels=2, callback=self.callback):
                while self.record:
                    file.write(self.q.get())
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            print("end ptt")
                            self.record = False    
        self.return_text = True                     
                    
    def __draw_maze(self, maze, player, render=17):
        
        # checks if player and maze were handed over
        if (player and maze) != None:

            # iterates over every field in maze
            for y in range(16):
                for x in range(16):

                    # calculates whether field is in render distance or not
                    isRendered = (x - render < player.currentPosition[0] < x + render) and (y - render < player.currentPosition[1] < y + render)

                    # if not, leave it black; do nothing
                    if not isRendered:
                        continue
                    
                    # if field is declared as wall, draw white square
                    if maze[0][y][x] == 1:
                        pygame.draw.rect(self.screen, Colors.WHITE.value, (self.maze_offset_x + x * self.CELL_SIZE, self.maze_offset_y + y * self.CELL_SIZE, self.CELL_SIZE - 4, self.CELL_SIZE - 4))

                    # draws player if field has player coordinates
                    if player.currentPosition == [x, y] and (not player.isHidden):
                        pygame.draw.rect(self.screen, self.personality_to_color.get(player.name, Colors.LIMEGREEN.value), (self.maze_offset_x + x * self.CELL_SIZE, self.maze_offset_y + y * self.CELL_SIZE, self.CELL_SIZE - 4, self.CELL_SIZE - 4))

                    # draws finish point
                    if maze[2] == [x, y]:                      
                        pygame.draw.rect(self.screen, Colors.RED.value, (self.maze_offset_x + x * self.CELL_SIZE, self.maze_offset_y + y * self.CELL_SIZE, self.CELL_SIZE - 4, self.CELL_SIZE - 4))   

    # draws the chat history  
    def __draw_chat_text(self):
        for i in range(0, self.chat_max_len):
            self.text_response = self.response_font.render(self.chat[i], True, self.chat_color[i])
            self.screen.blit(self.text_response, (self.chat_horizontal_offset, (self.maze_offset_y + i * self.chat_line_offset)))

    # draws the cursor in the users input box
    def __draw_input_cursor(self, current_line, max_line):
        self.cursor = self.base_font.render("_", True, Colors.WHITE.value)
        self.screen.blit(self.cursor,(self.input_rect.x + current_line.get_width() + 5, self.input_rect.y + max_line * self.input_rect_normal_height))
        
    # displays the currently written user input inside the box
    def __draw_input_text(self): 

        # splits raw input text into 45 chars long lines and displays them in the input box
        lines = textwrap.wrap(self.user_text, 45)
        if lines == []:
            lines = [""]
        max_line = len(lines) - 1
        for i in range(len(lines)):
            rendered_line = self.base_font.render(lines[i], True, Colors.WHITE.value)
            self.screen.blit(rendered_line,(self.input_rect.x + 5, self.input_rect.y + 3 + i * self.input_rect_normal_height))
        current_line = self.base_font.render(lines[max_line], True, Colors.WHITE.value)
        first_line = self.base_font.render(lines[0], True, Colors.WHITE.value)

        # updates the cursor to the input text, where current line contains the width of the bottom line and max_line tells which line is the bottom one
        self.__draw_input_cursor(current_line, max_line)
        
        # adapts the input border width and height to the currently written input text
        self.input_rect.w = max(200, first_line.get_width() + 15)
        self.input_rect.h = self.input_rect_normal_height * (max_line + 1) + 5

    # adds text to the chat (optional with author)
    def add_chat_text(self, raw_text, author = ""):

        # if there is an author attached to the text that is added, it will be displayed 
        if author == "":
            paragraphs = str(raw_text).split("|") 
        else:
            paragraphs = str(author + ": " + raw_text).split("|")

        # paragraphs are created by line breaks "|" in the handed over text
        for paragraph in paragraphs:

            # each paragraph is splitted in 45 chars long parts
            lines = textwrap.wrap(paragraph, 45)
            first_line = True

            # chooses text color based on author if registrated
            color = self.personality_to_color.get(author, Colors.GREY.value)

            # scrolls the chat up so there is space for the new entry 
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


    def __quit_screen(self): 
        pygame.quit()

    # transfers stored message after return to chatgpt and resets it 
    def get_user_input(self):
        return_message = self.message
        self.message = ""
        self.return_text = False
        return return_message

    def __ppt(self):
        if not self.record:
            return True

    # true in the moment in which input is returned / enter pressed
    def __on_return(self):
        if self.return_text:
            self.return_text = False
            return True
        return False 
    
    # true in the moment in which chatgpts response is changed
    def __on_response_change(self):
        if self.response_text != self.last_response:
            self.last_response = self.response_text
            return True
        return False

    # triggers text_to_speech on the current response 
    def __play(self):
        file_tts_out = Path(__file__).parent / "tts_out.wav"
        file_tts_out.resolve()
        
        pygame.mixer.music.load(file_tts_out)
        
        pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(10)
        
        pygame.mixer.music.unload()