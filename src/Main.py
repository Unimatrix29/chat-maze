import pygame, sys
from Screen import Screen
from MazeGenerator import MazeGenerator
from Player import Player
from Controller import Controller
from ChatGPT_Controller import ChatGPT
import threading
import queue
import pygame
import random

DIFFICULTY = {
    "TEST":
    [0, 1, 1],
    "EASY":
    [1, 0, 2], #[maze_preset_level, wall_penalties, debuff_duration]
    "NORMAL":
    [2, 1, 5],
    "HARD":
    [3, 3, 10]
    }

DEBUFF = {
    1: "ROTATION",
    2: "BLINDENESS",
    3: "RANDOM_MOVE",
    4: "TELEPORT",
    5: "INVISIBILITY"
    }

PROMPT = "Du bist ein sehr höflicher Mensch und akzeptierst nur Anfragen, welche sehr höflich sind. Der User gibt dir eine Weganweisung. Die Weganweisung kann entweder nach oben, unten, links und rechts stattfinden. Wenn der User zum Beispiel höflich fragt: Gehen Sie bitte nach oben, gibst du als Antwort \"up\" zurück. Dasselbe Prinzip für \"left\", \"up\", \"down\". Wenn der User zu unhöflich fragt, also zum Beispiel sagt: geh hoch, gibst du als Antwort \"deny\" zurück. Wenn der User auch keine Weganweisung gibt, sondern irgendetwas anderes antwortest du auch mit deny. Es ist wichtig, dass du nur mit \"left\" \"right\" \"up\" \"down\" \"deny\" antwortest, kein Satz oder ähnliches nur mit diesen Worten."

###################################################################################################
#The ChatGPT_Controller expects the json file to be in the same directory as ChatGPT_Controller.py
#and it musst contain a key-value-pair where the key is called: "api_key"
###################################################################################################
CONFIG_FILE_NAME = "config.json"
GPT_MODEL = "gpt-4-turbo"
TEMPERATURE = 0.25

mazeWindow = Screen()
textInputWindow = Controller()
mazeGenerator = MazeGenerator()
controller = Controller()
        
# difficulty = set_level()
difficulty = DIFFICULTY["TEST"]
mazePreset = f"maze_{difficulty[0]}.{random.randint(1, 4)}.0"
maze = mazeGenerator.get_preset(mazePreset)
player = Player(maze)

window.setup_screen()
window.update_screen(maze, player)
maze = mazeGenerator.get_preset("maze_2")

running = True
gameOver = False
debuffDuration = 0
renderDistance = 16

ready_for_input_event = threading.Event()
gameOver_event = threading.Event()
shared_queue = queue.Queue()

def console_input():
    
    global controller, shared_queue, ready_for_input_event
    
    #let the user choose the control mode 
    console_On = choose_mode()
    
    
    chatGPT = ChatGPT(system_prompt=PROMPT, config_file=CONFIG_FILE_NAME, gpt_model=GPT_MODEL, timeout=30)
    
    while not gameOver_event.is_set():
        
        ready_for_input_event.wait()
        
        #logic for wich control option the user chose 
        if console_On: 
            user_input = input("Bitte gib höflich ein Richtung an: ")
        else:
            while not controller.is_submit():
                pass
            user_input = controller.get_input()

        #chatGPT call
        move_Vector = chatGPT.get_movement_vector(user_input, TEMPERATURE)

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
            controller.setup_prompt_window()
            controller.init_prompt_window()
            return False
        elif choice == "c":
            return True
        else:
            pass
        

"""
Asking for difficulty choice
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

def apply_debuff(choice):
    global renderDistance
    global debuffDuration
    global maze

    print(choice)
    match choice:
        case "ROTATION":
            maze = mazeGenerator.rotate_maze(maze)
            newPosition = [player.currentPosition[1], 15 - player.currentPosition[0]]
            player.set_position(newPosition)
            return
        case "BLINDENESS":
            renderDistance = 4
            debuffDuration = difficulty[2]
            return
        case "RANDOM_MOVE":
            mVector = controller.random_input()
            player.move(mVector)
            while window.check_wall(maze, player.currentPosition):
                player.move([-mVector[0], -mVector[1]])
                mVector = controller.random_input()
                player.move(mVector)
            return
        case "TELEPORT":
            player.set_position(mazeGenerator.get_random_point(maze))
            return
        case "INVISIBILITY":
            player.hide(True)
            debuffDuration = difficulty[2]
            return
        case _:
            print("No penalty")
            return
        
def remove_debuffs():
    global renderDistance
    renderDistance = 16
    player.hide(False)

input_thread = threading.Thread(target=console_input)
input_thread.start()


while running:
    
    ready_for_input_event.set()
    ready_for_input_event.clear()
    
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
        
        if not shared_queue.empty():
            
            mVector = shared_queue.get()
            player.move(mVector)
        
            debuffDuration = max(debuffDuration - 1, 0)
       
            if debuffDuration == 0:
                remove_debuffs()
            # Applying debuffs in case of rough request
            if mVector == [0, 0]:
                apply_debuff(DEBUFF[random.randint(3, 5)])
            # Applying debuffs in case of running against walls
            if window.check_wall(maze, player.currentPosition):
                player.move([-mVector[0], -mVector[1]])
                for i in range(difficulty[1]):
                    apply_debuff(DEBUFF[random.randint(1, 3)])

            if window.check_finish(maze, player.currentPosition):
                # Changing actual maze to an end screen (happy)
                maze = mazeGenerator.get_preset("FINISH")
                player.set_position([-1, -1])
                gameOver = True
            
    window.update_screen(maze, player, renderDistance)
   
window.quit_screen()
gameOver_event.set()
input_thread.join()