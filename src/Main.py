from Screen import Screen
from MazeGenerator import MazeGenerator
from Player import Player
from ChatGPT_Movment_Controller import chatgpt_movment
from ChatGPT_Client import ApiClientCreator
from ChatGPT_Controller import ChatGPT
import threading
import queue
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
GPT_MODEL = "gpt-4o"
TEMPERATURE = 0.25

screen = Screen()
mazeGenerator = MazeGenerator()

apiClient = ApiClientCreator.get_client(CONFIG_FILE_NAME)

        
# difficulty = set_level()
difficulty = DIFFICULTY["TEST"]
#mazePreset = f"maze_{difficulty[0]}.{random.randint(1, 4)}.0"
#maze = mazeGenerator.get_preset(mazePreset)
maze = mazeGenerator.get_preset("maze_1.1.0")

player = Player(maze)

screen.setup_screen()

running = True
gameOver = False
debuffDuration = 0
renderDistance = 16

ready_for_input_event = threading.Event()
gameOver_event = threading.Event()

chatgpt_queue = queue.Queue()
screen_queue = queue.Queue()


def console_input():
    
    global chatgpt_queue, screen_queue, ready_for_input_event, gameOver_event

    chatgpt = ChatGPT(apiClient, GPT_MODEL)
    
    movmentChatGPT = chatgpt_movment(chatgpt=chatgpt, system_prompt=PROMPT)
    
    while not gameOver_event.is_set():

        #ready_for_input_event.wait()

        msg = screen_queue.get()
        
        try:        
            #chatGPT call
            move_Vector, content = movmentChatGPT.get_vector(msg, TEMPERATURE)

            chatgpt_queue.put(item=[move_Vector, content])
        except Exception as e:
            #Let the user now that something went wrong
            pass



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
            #mVector = controller.random_input()
            mVector = [0,0]
            player.move(mVector)
            while screen.check_wall(maze, player.currentPosition):
                player.move([-mVector[0], -mVector[1]])
                #mVector = controller.random_input()
                mVector = [0,0]
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
    
    screen.update_screen(maze, player)
    
    if(screen.on_return()):
        user_input = screen.get_user_input()
        print(user_input)
        screen_queue.put(user_input)
        
        #ready_for_input_event.set()
        #ready_for_input_event.clear()

    try: 
        data = chatgpt_queue.get(False)
        player.move(data[0])
        screen.response_text = data[1]
    except queue.Empty:
        pass
    
    
screen.quit_screen()
gameOver_event.set()
input_thread.join()