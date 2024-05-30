from ChatGPT_Client import ApiClientCreator
from ChatGPT_Controller import chatgpt_text
from Controller import Controller
from GameHandler import GameHandler
from Player import Player
from Screen import Screen
import pygame, random, queue, threading

PROMPT = "Du bist ein sehr höflicher Mensch und akzeptierst nur Anfragen, welche sehr höflich sind. Der User gibt dir eine Weganweisung. Die Weganweisung kann entweder nach oben, unten, links und rechts stattfinden. Wenn der User zum Beispiel höflich fragt: Gehen Sie bitte nach oben, gibst du als Antwort \"up\" zurück. Dasselbe Prinzip für \"left\", \"up\", \"down\". Wenn der User zu unhöflich fragt, also zum Beispiel sagt: geh hoch, gibst du als Antwort \"deny\" zurück. Wenn der User auch keine Weganweisung gibt, sondern irgendetwas anderes antwortest du auch mit deny. Es ist wichtig, dass du nur mit \"left\" \"right\" \"up\" \"down\" \"deny\" antwortest, kein Satz oder ähnliches nur mit diesen Worten."

###################################################################################################
#The ChatGPT_Controller expects the json file to be in the same directory as ChatGPT_Controller.py
#and it musst contain a key-value-pair where the key is called: "api_key"
###################################################################################################
CONFIG_FILE_NAME = "config.json"
GPT_MODEL = "gpt-4-turbo"
TEMPERATURE = 0.25
"""
Chat-GPT client initialization
"""
clientCreator = ApiClientCreator(file_name=CONFIG_FILE_NAME)
apiClient = clientCreator.get_client()
"""
Game session set up
"""
gameHandler = GameHandler()

gameHandler.set_level()
gameStats = gameHandler.get_game_stats() #[difficulty, (active)maze, [debuffDuration, renderDistance]]

startMaze = gameStats[1]
maze = gameStats[1]

player = Player(startMaze)
"""
Output window set up
"""
mazeWindow = Screen()
mazeWindow.setup_screen()
mazeWindow.update_screen(startMaze, player)
"""
Game loop variables
"""
running = True

ready_for_input_event = threading.Event()
gameOver_event = threading.Event()
shared_queue = queue.Queue()

def console_input():
    
    global shared_queue, ready_for_input_event
    
    #let the user choose the control mode 
    console_On = choose_mode()
    
    textInputWindow = Controller()
    textChatGPT = chatgpt_text(client=apiClient, system_prompt=PROMPT, gpt_model=GPT_MODEL)
    
    while not gameOver_event.is_set():
        
        #logic for wich control option the user chose 
        if console_On: 
            ready_for_input_event.wait()
            user_input = input("Bitte gib höflich ein Richtung an: ")
        else:
            print("Sorry but the GUI is not working at the moment :(")
            #textInputWindow.setup_screen()
            #textInputWindow.update_screen()
            #if textInputWindow.on_return():
            #    user_input = textInputWindow.get_user_input()
            

        #chatGPT call
        move_Vector = textChatGPT.get_movement_vector(user_input, TEMPERATURE)

        if move_Vector is Exception:
           #Let the User know, that something went wrong and he should try again 
           pass
        else: 
            shared_queue.put(move_Vector)

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

input_thread = threading.Thread(target=console_input)
input_thread.start()
"""
Game loop
"""
while running:
    
    ready_for_input_event.set()
    ready_for_input_event.clear()
    
    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            # Game restart by pressing R key (Problem with maze reseting)
            if event.key == pygame.K_r:
                pass
                # maze = startMaze
                # player.set_position(maze[1])
                
        if event.type == pygame.QUIT:
            running = False
    
    if not (gameHandler.is_game_over() or shared_queue.empty()):

        mVector = shared_queue.get()
        player.move(mVector)
        # Removing debuffs by expiring their's duration
        gameHandler.reduce_debuffs()
        if gameStats[2][0] == 0:
            gameHandler.remove_debuffs(player)
        # Applying debuffs in case of rough request
        if mVector == [0, 0]:
            gameHandler.apply_debuffs(player, maze, 3)
        # Applying debuffs in case of running against walls
        if gameHandler.check_wall(player.currentPosition):
            player.move([-mVector[0], -mVector[1]])
            for i in range(gameStats[0][1]):
                gameHandler.apply_debuffs(player, maze, 1)
        # Showing end screen if finish arrived
        if gameHandler.check_finish(player.currentPosition):
            player.set_position([-1, -1])
            gameHandler.end_game()
            
    gameStats = gameHandler.get_game_stats()    #[[difficulty], [(active)maze], [debuffDuration, renderDistance]]
    maze = gameStats[1]
        
    mazeWindow.update_screen(maze, player, gameStats[2][1])
"""
Programm finish
"""
mazeWindow.quit_screen()
gameOver_event.set()
input_thread.join()