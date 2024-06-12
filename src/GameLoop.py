from ChatGPT_Client import ApiClientCreator
from ChatGPT_Controller import ChatGPT
from GameHandler import GameHandler
from Commands import Command
from Player import Player
from Screen import Screen
import queue, threading, time


class Game():
    
    def __init__(self):
        ###################################################################################################
        #The ChatGPT_Controller expects the json file to be in the same directory as ChatGPT_Controller.py
        #and it musst contain a key-value-pair where the key is called: "api_key"
        ###################################################################################################
        config_file_name = "config.json"
        
        """
        Game session set up
        """
        self.running = True

        self.gameHandler = GameHandler()
        self.gameHandler.set_level()
        self.prompt = self.gameHandler.get_prompt()
        self.gameStats = self.gameHandler.get_game_stats() #[difficulty, (active)maze, [debuffDuration, renderDistance]]
        self.maze = self.gameStats[1]
        self.player = Player(self.maze)
        
        apiClient = ApiClientCreator.get_client(file_name=config_file_name)

        self.chatgpt = ChatGPT(apiClient)
        
        self.gameOver_event = threading.Event()
        self.screen_queue = queue.Queue()
        self.chatgpt_queue = queue.Queue()
        self.chatGPT_thread = threading.Thread(target=self.__get_chatgpt_response, kwargs={
            "chatgpt"   : self.chatgpt,
            "prompt"    : self.prompt
        })

        """
        Output window set up
        """
        self.screen = Screen()
        self.screen.setup_screen()
        self.commandHandler = Command(self)
        
        self.chatGPT_thread.start()
        
 
    def run(self):
        """
        Game loop
        """
        while self.running:

            if(self.screen.on_return()):
                user_input = self.screen.get_user_input()
                print(user_input)

                if not self.commandHandler.execute(user_input):
                    self.screen_queue.put(user_input)

            mVector = [0, 0]
            try: 
                data = self.chatgpt_queue.get(False)
                mVector = data[0]
                
                # BITTE NOCH ANPASSEN
                clear_text = str(data[1]).split("|")
                self.screen.response_text = clear_text[1]

            except queue.Empty:
                pass

            if not self.gameHandler.is_game_over():
                # Running till a wall
                while not mVector == [0, 0]:
                    # Showing end screen if finish arrived
                    if self.gameHandler.check_finish(self.player.currentPosition):
                        self.gameHandler.end_game(self.player)
                        break

                    nextStep = [self.player.currentPosition[0] + mVector[0], self.player.currentPosition[1] + mVector[1]]
                    # Going to the next section
                    # of the maze preset if reached the border
                    if self.gameHandler.check_border(nextStep):
                        self.gameHandler.switch_section(self.player)
                        nextStep = [self.player.currentPosition[0] + mVector[0], self.player.currentPosition[1] + mVector[1]]

                    gameStats = self.gameHandler.get_game_stats()
                    maze = gameStats[1]

                    # Stop moving in front of a wall
                    if self.gameHandler.check_wall(nextStep):
                        break

                    self.player.move(mVector)

                    self.screen.update_screen(maze, self.player, gameStats[2][1])
                    time.sleep(0.3)

                # TODO: Rework debuff system
                # # Removing debuffs by expiring their's duration
                # if not mVector == [0, 0]:
                #     gameHandler.reduce_debuffs()
                # if gameStats[2][0] == 0:
                #     gameHandler.remove_debuffs(player)
                # # Applying debuffs in case of rough request
                # if mVector == [-1, -1]:
                #     gameHandler.apply_debuffs(player, maze, 3)

                gameStats = self.gameHandler.get_game_stats()    #[[difficulty], [(active)maze], [debuffDuration, renderDistance]]
                maze = gameStats[1]

            self.screen.update_screen(maze, self.player, gameStats[2][1])
    
        """
        Programm finish
        """
        self.screen.quit_screen()
        self.gameOver_event.set()
        self.chatGPT_thread.join()
        
        
    def restart(self):
        self.screen.quit_screen()
        self.gameOver_event.set()
        self.chatGPT_thread.join()
        
        self.__init__()
       
       
    def __get_chatgpt_response(self, chatgpt, prompt):
        from ChatGPT_Movment_Controller import chatgpt_movment
        import openai
        
        gpt_model = "gpt-4o"
        temperatur = 0.25

        movmentChatGPT = chatgpt_movment(chatgpt=chatgpt, model=gpt_model)

        while not self.gameOver_event.is_set():
            try:        
                msg = self.screen_queue.get(False)
                #chatGPT call
                move_Vector, content = movmentChatGPT.get_vector(msg, temperatur, prompt)

                self.chatgpt_queue.put(item=[move_Vector, content])
            except queue.Empty:
                pass
            except OSError as e:
                #This is a huge problem. We most certainly need to restart the entire program.
                print("FATAL ERROR")
                pass
            except openai.APIError as e: 
                #Let the user now that something went wrong
                print("API CALL ERROR")
                pass

   