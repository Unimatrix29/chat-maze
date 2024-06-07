from ChatGPT_Client import ApiClientCreator
from ChatGPT_Movment_Controller import chatgpt_movment
from ChatGPT_Client import ApiClientCreator
from ChatGPT_Controller import ChatGPT
from GameHandler import GameHandler
from Player import Player
from Screen import Screen
import pygame, random, queue, threading, time
import numpy as np

<<<<<<< HEAD

window = Screen()
mazeGenerator = MazeGenerator()
window.setup_screen()
maze = mazeGenerator.get_preset("maze_2")
player = Player(mazeGenerator.PRESET_LIBRARY["maze_1"], window) 





controller = Controller()


=======
###################################################################################################
#The ChatGPT_Controller expects the json file to be in the same directory as ChatGPT_Controller.py
#and it musst contain a key-value-pair where the key is called: "api_key"
###################################################################################################
CONFIG_FILE_NAME = "config.json"
GPT_MODEL = "gpt-4o"
TEMPERATURE = 0.25
"""
Game session set up
"""
gameHandler = GameHandler()

gameHandler.set_level()
PROMPT = gameHandler.get_prompt()
>>>>>>> main

gameStats = gameHandler.get_game_stats() #[difficulty, (active)maze, [debuffDuration, renderDistance]]

<<<<<<< HEAD

#player.move(maze[1])




while True:
=======
maze = gameStats[1]

player = Player(maze)
"""
Output window set up
"""
screen = Screen()
screen.setup_screen()
screen.update_screen(maze, player)
"""
Game loop variables
"""
running = True

ready_for_input_event = threading.Event()
gameOver_event = threading.Event()

chatgpt_queue = queue.Queue()
screen_queue = queue.Queue()


def get_chatgpt_response():
    
    global chatgpt_queue, screen_queue, ready_for_input_event, gameOver_event, PROMPT
    
    """
    Chat-GPT client initialization
    """
    apiClient = ApiClientCreator.get_client(file_name=CONFIG_FILE_NAME)
>>>>>>> main

    chatgpt = ChatGPT(apiClient, GPT_MODEL)
        
    movmentChatGPT = chatgpt_movment(chatgpt=chatgpt, system_prompt=PROMPT)
    
    while not gameOver_event.is_set():

        #ready_for_input_event.wait()

        msg = screen_queue.get()
        
        movmentChatGPT.update_prompt(PROMPT)
        try:        
            #chatGPT call
            move_Vector, content = movmentChatGPT.get_vector(msg, TEMPERATURE)

            chatgpt_queue.put(item=[move_Vector, content])
        except Exception as e:
            #Let the user now that something went wrong
            print(e)

#choose if you want to control the program via console or GUI
def choose_mode():
    while True:
        choice = input("Wie wollen sie mit chtaGPT interagieren? Für die Konsole drücken sie [C]. Für die GUI drücken sie [G]: ").strip().lower()

        if choice == "g":
            return False
        elif choice == "c":
            return True
        else:
            pass
        
chatGPT_thread = threading.Thread(target=get_chatgpt_response)
chatGPT_thread.start()
"""
Game loop
"""
while running:
        
    if(screen.on_return()):
        user_input = screen.get_user_input()
        print(user_input)
        screen_queue.put(user_input)
        
        #ready_for_input_event.set()
        #ready_for_input_event.clear()

    mVector = [0, 0]
    try: 
        data = chatgpt_queue.get(False)
        mVector = data[0]
        screen.response_text = data[1]
    except queue.Empty:
        pass

    if not gameHandler.is_game_over():
        # Running till a wall
        while not gameHandler.check_wall(list(np.array(player.currentPosition) + np.array(mVector))) and mVector != [0, 0]:
            player.move(mVector)
            screen.update_screen(maze, player, gameStats[2][1])
            time.sleep(0.3)

        # Removing debuffs by expiring their's duration
        if not mVector == [0, 0]:
            gameHandler.reduce_debuffs()
        if gameStats[2][0] == 0:
            gameHandler.remove_debuffs(player)
        # Applying debuffs in case of rough request
        if mVector == [-1, -1]:
            gameHandler.apply_debuffs(player, maze, 3)
        # Going to the next section (start point) of the maze preset
        if gameHandler.check_border(player.currentPosition):
            gameHandler.switch_section(player)
        # Applying debuffs in case of running against walls
        elif gameHandler.check_wall(player.currentPosition):
            player.move([-mVector[0], -mVector[1]])
            gameHandler.apply_debuffs(player, maze, 1)
        # Showing end screen if finish arrived
        if gameHandler.check_finish(player.currentPosition):
            gameHandler.end_game(player)
            
        gameStats = gameHandler.get_game_stats()    #[[difficulty], [(active)maze], [debuffDuration, renderDistance]]
        maze = gameStats[1]
        
    screen.update_screen(maze, player, gameStats[2][1])
    # Restarting game upon request
    if screen.has_restart_request():
        resetRequest = screen.has_reset_request()
        
        line = "Game reset" if resetRequest else "Session restart"
        print(line)
        
        gameHandler.restart_game(player, resetRequest)
        PROMPT = gameHandler.get_prompt()
"""
Programm finish
"""
screen.quit_screen()
gameOver_event.set()
chatGPT_thread.join()