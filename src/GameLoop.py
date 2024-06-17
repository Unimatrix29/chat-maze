#from AutoPlayer import AutoPlayer
from ChatGPT_Client import ApiClientCreator
from ChatGPT_Controller import ChatGPT
from CommandHandler import Command
from GameHandler import GameHandler
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
        
        # Game session set up
        #self.bot = AutoPlayer()
        self.autoPlay = False
        self.running = True
        
        self.screen = Screen()
        self.screen.setup_screen()
        
        self.gameHandler = GameHandler()
        # Setting start idle frame (maze)
        self.maze = self.gameHandler.get_game_stats()[1]
        self.player = Player(self.maze)
        # A timer for switching idle frames
        self.idleTimer = threading.Timer(self.maze[3], self.switch_idle_frame)
        
        self.choose_difficulty()
        
        self.prompt = self.gameHandler.get_prompt()
        self.gameStats = self.gameHandler.get_game_stats() #[difficulty, (active)maze, [debuffDuration, renderDistance], promptName]
        self.maze = self.gameStats[1]
        self.player.set_position(self.maze[1])

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
        
        self.commandHandler = Command(self)
        
        self.chatGPT_thread.start()
    """
    Game loop
    """
    def run(self):
        while self.running:
            # Processing user input
            if self.audio_event.is_set():
                self.screen.audio_mode=True
            if(self.screen.on_return()):
                if self.screen.ppt():
                    audio_input=self.chatgpt.audio_to_text()
                user_input = self.screen.get_user_input()
                print(user_input)

                if not self.commandHandler.execute(user_input):
                    if self.audio_event.is_set():
                        self.screen.add_chat_text(audio_input, "You")
                        self.screen_queue.put(audio_input)
                        print(audio_input)
                    else:
                        self.screen_queue.put(user_input)

            # Getting a movement vector from chatGPT
            mVector = [0, 0]
            # if self.autoPlay:
            #     mVector = self.bot.make_random_move()
            try: 
                data = self.chatgpt_queue.get(False)
                mVector = data.get("mVector")
                
                clear_text = data.get("content")
                
                if data.get("role") == "Error":
                    self.screen.add_chat_text(clear_text, "Error")
                else:
                    self.screen.add_chat_text(clear_text, self.gameStats[3])
                
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
                        self.gameOver_event.set()
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
        # Programm finish
        self.screen.quit_screen()
        self.gameOver_event.set()
        self.chatGPT_thread.join()
    """
    Resets the game to the start instance
    """
    def reset(self):
        self.stop_idle()
        self.gameHandler.reset_game(self.player)
        # Updating active maze to a FINISH preset
        self.update_game_stats()

        self.choose_difficulty()
        # Getting new maze
        self.update_game_stats()
        self.prompt = self.gameHandler.get_prompt()
        self.player.set_position(self.maze[1])
        
        self.audio_event.clear()

        self.clear_queues()
        self.restart_chatGPT_thread()
    """
    Lets the user retry the current maze with the current prompt
    Dosen't reset chatgpt history
    """
    def restart(self):
        self.stop_idle()
        self.gameHandler.restart_game(self.player)
        
        self.update_game_stats()

        self.screen.update_screen(self.maze, self.player, self.gameStats[2][1])
        
        self.clear_queues()
        self.restart_chatGPT_thread()       
       
    def choose_difficulty(self):
        self.screen.clear_chat_text()
        level = ""
        
        self.screen.add_chat_text("#################### : #####", "##### ")
        self.screen.add_chat_text("Welcome to Chat Leap : #####", "##### ")
        self.screen.add_chat_text("#################### : #####", "##### ")
        self.screen.add_chat_text("                            ", "##### ")
        self.screen.add_chat_text("Please chose a difficulty: EASY, NORMAL, HARD", "System")
        
        while level == "":    
            level = self.screen.get_user_input()
            level = level.strip().upper()
            # Drawing idle frame (maze)
            self.run_idle()
            self.screen.update_screen(self.maze, self.player)
            if level != "":
                if not self.gameHandler.set_level(level):
                    self.screen.add_chat_text("A vaild one, please.", "System")
                    level = ""
                    print(f"<{level}>")
                
        self.stop_idle()
        self.screen.clear_chat_text()
        
       
    def __get_chatgpt_response(self, chatgpt, prompt):
        from ChatGPT_Movment_Controller import chatgpt_movment
        import openai
        
        gpt_model = "gpt-4o"
        temperatur = 0.25
        data = {
            "content": "",
            "role": "GPT-4o",
            "mVector": [0, 0]
        }

        movmentChatGPT = chatgpt_movment(chatgpt=chatgpt, model=gpt_model)

        while not self.gameOver_event.is_set():
            try:        
                msg = self.screen_queue.get(False)
                #chatGPT call
                data["mVector"], data["content"] = movmentChatGPT.get_vector(msg, temperatur, prompt)
                
                if self.audio_event.is_set():
                    name = self.gameStats[3]
                    chatgpt.text_to_audio(data["content"],name=name)
                    self.audio_is_ready_event.set()
                
                data["role"] = "GPT-4o" 
                self.chatgpt_queue.put(data)
            except queue.Empty:
                pass
            except OSError as e:
                #This is a huge problem. We most certainly need to restart the entire program.
                print("FATAL ERROR")
                pass
            except openai.APIError as e: 
                data["mVector"] = [0, 0]
                data["content"] = "I'm sorry, it appears that I can't reach the OpenAI server right now."
                data["role"] = "Error"
                self.chatgpt_queue.put(data)
                print("API CALL ERROR")
                pass
    """
    Updates idleTimer by it's expiring
    according to time stamp of current idle frame
    """
    def run_idle(self):
        if self.idleTimer.is_alive():
            return
        
        runTime = self.maze[3]
        
        self.idleTimer = threading.Timer(runTime, self.switch_idle_frame)
        self.idleTimer.start()
    """
    Stops idle animations
    """
    def stop_idle(self):
        self.idleTimer.cancel()
        self.idleTimer.join()
        # Avoiding saving idle frame
        self.update_game_stats()
    """
    Switches active maze (idle frame) to the next one
    every frameTicks' amount of game ticks
    !Only used with FINISH and IDLE presets!
    """
    def switch_idle_frame(self):
        nextFrame = self.maze[4]
        
        self.maze = self.gameHandler.get_idle_maze(nextFrame)
    """
    Gets new gameStats[] with active(switched/rotated) maze
    as well as debuff's infos
    """
    def update_game_stats(self):
        self.gameStats = self.gameHandler.get_game_stats()      #[[difficulty], [(active)maze], [debuffDuration, renderDistance]]
        self.maze = self.gameStats[1]

    def clear_queues(self):
        self.chatgpt_queue.queue.clear()
        self.screen_queue.queue.clear()
        
    def restart_chatGPT_thread(self):
        self.gameOver_event.set()
        self.chatGPT_thread.join()
        self.gameOver_event.clear()

        self.chatGPT_thread = threading.Thread(target=self.__get_chatgpt_response,
                                               kwargs={
                                                "chatgpt"   : self.chatgpt,
                                                "prompt"    : self.prompt
                                                })
        self.chatGPT_thread.start()