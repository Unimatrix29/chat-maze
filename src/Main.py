import pygame
import random
from Screen import Screen
from MazeGenerator import MazeGenerator
from Player import Player
from Controller import Controller
from ChatGPT_Controller import ChatGPT

DIFFICULTY = {
    "TEST":
    [0, 0],
    "EASY":
    [1, 0], #[maze_preset_level, wall_penalties]
    "NORMAL":
    [2, 1],
    "HARD":
    [3, 3]
    }

PROMPT = "Du bist ein sehr höflicher Mensch und akzeptierst nur Anfragen, welche sehr höflich sind. Der User gibt dir eine Weganweisung. Die Weganweisung kann entweder nach oben, unten, links und rechts stattfinden. Wenn der User zum Beispiel höflich fragt: Gehen Sie bitte nach oben, gibst du als Antwort \"up\" zurück. Dasselbe Prinzip für \"left\", \"up\", \"down\". Wenn der User zu unhöflich fragt, also zum Beispiel sagt: geh hoch, gibst du als Antwort \"deny\" zurück. Wenn der User auch keine Weganweisung gibt, sondern irgendetwas anderes antwortest du auch mit deny. Es ist wichtig, dass du nur mit \"left\" \"right\" \"up\" \"down\" \"deny\" antwortest, kein Satz oder ähnliches nur mit diesen Worten."

####################################################################################
#The ChatGPT_Controller expects the json file to be in the same directory as ChatGPT_Controller.py
#and it musst contain a key-value-pair where the key is called: "api_key"
#################################################################################### 
CONFIG_FILE_NAME = "config.json"

GPT_MODEL = "gpt-4-turbo"
TEMPERATURE = 0.25

window = Screen()
mazeGenerator = MazeGenerator()
controller = Controller()

# chatGPT = ChatGPT(system_prompt=PROMPT, config_file=CONFIG_FILE_NAME, gpt_model=GPT_MODEL, timeout=30)
"""
TEST FUNCTION
"""
def set_level():
    options = ["TEST", "EASY", "NORMAL", "HARD"]
    level = ""
    while not (isinstance(level, int)):
        try:
            level = int(input("Choose difficulty:\n 1 - Easy | 2 - Normal | 3 - Hard\n"))
            if level < 0 or level > 3:
                level = ""
                raise ValueError
        except ValueError:
            print("Bad input >:( Enter the number of chosen difficulty")
        
    return DIFFICULTY[options[level]]
        
difficulty = set_level()
mazePreset = f"maze_{difficulty[0]}.{random.randint(1, 4)}.0"

maze = mazeGenerator.get_preset(mazePreset)
player = Player(maze, window)

running = True
gameOver = False

window.setup_screen()
window.update_screen(maze, player)
#controller.setup_prompt_window()
#controller.init_prompt_window()

while running:

    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            # Game restart by pressing R key
            if event.key == pygame.K_r:
                gameOver = False
                maze = mazeGenerator.get_preset(mazePreset)
                player.set_position(maze[1])
                
        if event.type == pygame.QUIT:
            running = False
            
    if not gameOver:
        mVector = controller.console_input()
        player.move(mVector)

    isOnWall = window.check_wall(maze, player.currentPosition)
    player.hide(isOnWall)
        
    if window.check_finish(maze, player.currentPosition):
        # Changing actual maze to an end screen (happy)
        maze = mazeGenerator.get_preset("FINISH")
        player.set_position([-1, -1])
        gameOver = True

    # if not gameOver:
    #     console_input = input("Bitte gib höflich ein Richtung an: ")
    #     mVector = chatGPT.get_movement_vector(console_input, TEMPERATURE)
    #     if mVector is Exception:
    #        #Let the User know, that something went wrong and he should try again 
    #        pass
    #     else: 
    #         player.move(mVector)
            
    window.update_screen(maze, player)
   
window.quit_screen()