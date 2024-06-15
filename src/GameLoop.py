from ChatGPT_Client import ApiClientCreator
from ChatGPT_Controller import ChatGPT
from GameHandler import GameHandler
from CommandHandler import Command
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
        
        self.screen = Screen()
        self.screen.setup_screen()
        
        self.gameHandler = GameHandler()
        
        self.chose_difficulty()
        
        self.prompt = self.gameHandler.get_prompt()
        self.gameStats = self.gameHandler.get_game_stats() #[difficulty, (active)maze, [debuffDuration, renderDistance]]
        self.maze = self.gameStats[1]
        self.player = Player(self.maze)

        apiClient = ApiClientCreator.get_client(file_name=config_file_name)

        self.chatgpt = ChatGPT(apiClient)
        
        
        self.audio_event = threading.Event()
        self.audio_is_ready_event = threading.Event()
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
        self.commandHandler = Command(self)
        
        self.chatGPT_thread.start()

        self.idleAnimationTicks = 0
        
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
                
                clear_text = data[1]
                self.screen.response_text = clear_text
                
                if self.audio_event.is_set():
                    self.audio_is_ready_event.wait()
                    self.screen.play()
                    self.audio_is_ready_event.clear()
            except queue.Empty:
                pass

            if self.gameHandler.is_game_over():
                self.run_idle()
            else:
                # # Removing debuffs by expiring their's duration
                if self.gameStats[2][0] == 0:
                    self.gameHandler.remove_debuffs(self.player)
                # Applying debuffs in case of rough request
                if mVector == [-1, -1]:
                    self.gameHandler.apply_debuffs(self.player, self.maze)
                    
                # Running till a wall
                while not mVector in [[0, 0], [-1, -1]]:
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

                    self.update_game_stats()

                    # Stop moving in front of a wall
                    if self.gameHandler.check_wall(nextStep):
                        self.gameHandler.reduce_debuffs()
                        break

                    self.player.move(mVector)

                    self.screen.update_screen(self.maze, self.player, self.gameStats[2][1])
                    time.sleep(0.3)

                self.update_game_stats()
                
            self.screen.update_screen(self.maze, self.player, self.gameStats[2][1])
    
        """
        Programm finish
        """
        self.screen.quit_screen()
        self.gameOver_event.set()
        self.chatGPT_thread.join()
        
    #sets up a new game with new maze and Prompt     
    def reset(self):
        self.screen.quit_screen()
        self.gameOver_event.set()
        self.chatGPT_thread.join()
        
        self.__init__()
        
    #lets the user retry the current maze with the current prompt, dosent reset chatgpt history 
    def restart(self):
        self.gameHandler.restart_game(self.player)
        
        self.update_game_stats()
                
        self.screen.update_screen(self.maze, self.player, self.gameStats[2][1])
       
       
    def chose_difficulty(self):
        level = ""
        
        self.screen.add_chat_text("#################### : #####", "##### ")
        self.screen.add_chat_text("Welcome to Chat Leap : #####", "##### ")
        self.screen.add_chat_text("#################### : #####", "##### ")
        self.screen.add_chat_text("                            ", "##### ")
        self.screen.add_chat_text("Please chose a difficulty: EASY, NORMAL, HARD", "System")
        
        while level == "":    
            level = self.screen.get_user_input()
            level = level.strip().upper()
            
            self.screen.update_screen()
            if level != "":
                if not self.gameHandler.set_level(level):
                    self.screen.add_chat_text("A vaild one, please.", "System")
                    level = ""
                    print(f"<{level}>")
                
        self.screen.clear_chat_text()
        
       
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
                
                if self.audio_event.is_set():
                    chatgpt.text_to_audio(content)
                    self.audio_is_ready_event.set()

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
            
    def update_game_stats(self):
        self.gameStats = self.gameHandler.get_game_stats()      #[[difficulty], [(active)maze], [debuffDuration, renderDistance]]
        self.maze = self.gameStats[1]
        
    def run_idle(self):
        self.idleAnimationTicks += 1
        frameTicks = self.maze[3]
        if not self.idleAnimationTicks == frameTicks:
            return

        self.idleAnimationTicks = 0
        
        nextFrame = self.maze[4]

        self.maze = self.gameHandler.get_idle_maze(nextFrame)