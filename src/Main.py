import pygame
from Screen import Screen
from MazeGenerator import MazeGenerator
from Player import Player
from Controller import Controller
from ChatGPT_Controller import ChatGPT

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

maze = mazeGenerator.get_preset("maze_1")
player = Player(maze, window)

running = True
gameOver = False

window.setup_screen()
window.update_screen(maze, player.currentPosition)
#controller.setup_prompt_window()
#controller.init_prompt_window()

while running:

    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            # Game restart by pressing R key
            if event.key == pygame.K_r:
                gameOver = False
                maze = mazeGenerator.get_preset("maze_1")
                player.set_position(maze[1])
                
        if event.type == pygame.QUIT:
            running = False
            
    if not gameOver:
        mVector = controller.console_input()
        player.move(mVector)

    if window.check_wall(maze, player.currentPosition):
        # Changing actual maze to an end screen (sad)
        maze = mazeGenerator.get_preset("LOST")
        player.set_position([-1, -1])
        gameOver = True
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
            
    window.update_screen(maze, player.currentPosition)
   
window.quit_screen()