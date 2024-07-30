#from AutoPlayer import AutoPlayer
from ChatGPT_Client import ApiClientCreator
from ChatGPT_Controller import ChatGPT
from CommandHandler import Command
from GameHandler import GameHandler
from Player import Player
from Screen import Screen
import queue, threading, time, traceback, openai


class Game():
    
    def __init__(self):
        ###################################################################################################
        #The ChatGPT_Controller expects the json file to be in the same directory as ChatGPT_Controller.py
        #and it musst contain a key-value-pair where the key is called: "api_key"
        ###################################################################################################
        config_file_name = "config.json"
        
        # Game session set up
        # Debug variable to track player position
        self.movementStopped = False
        # Main while loop variable
        self.running = True
        
        self.screen = Screen()
        self.screen.setup_screen(1)
        
        self.gameHandler = GameHandler()
        # Setting start idle frame (maze)
        # and a timer for switching idle frames
        self.maze = self.gameHandler.get_game_stats()[0]
        self.idleTimer = threading.Timer(self.maze[3], self.switch_idle_frame)
        self.player = Player(self.maze)
        
        self.apiClient = ApiClientCreator.get_client(file_name=config_file_name)

        self.chatgpt = ChatGPT(self.apiClient)
        # Print welcome message by initializing CommandHandler
        self.commandHandler = Command(self)
        
        self.choose_difficulty()
        # Print start message
        self.commandHandler.execute("__/start")
        
        self.prompt = self.gameHandler.get_prompt()        # [name, promptLine]
        self.gameStats = self.gameHandler.get_game_stats() # [[(active)maze], [debuffDuration, renderDistance, rotationCounter]]
        
        self.maze = self.gameStats[0]
        self.player.change_name(self.prompt[0])
        self.player.set_position(self.maze[1])
        
        self.audio_event = threading.Event()
        self.audio_is_ready_event = threading.Event()
        self.gameOver_event = threading.Event()
        self.screen_queue = queue.Queue()
        self.chatgpt_queue = queue.Queue()
        self.chatGPT_thread = threading.Thread(target=self.__get_chatgpt_response, kwargs={
            "chatgpt"   : self.chatgpt,
            "prompt"    : self.prompt[1]
        })
        
        self.chatGPT_thread.start()
    """
    Game loop
    """
    def run(self):
        while self.running:
            # Processing user input
            if self.audio_event.is_set():
                self.screen.audio_mode=True
            else:
                self.screen.audio_mode=False
                
            if self.screen.on_return():
                
                if self.screen.ppt() and self.audio_event.is_set():
                    try:
                        audio_input = self.chatgpt.audio_to_text()
                    except openai.BadRequestError as e:
                        print("Audio to text Api call failed!")
                        print(e)
                        self.screen.add_chat_text("Ups, es scheint als könnte ich dich nicht verstehen. Versuch es doch einfach nochmal :)", "Error")
                        audio_input = ""
                        pass
                user_input = self.screen.get_user_input()
                
                print(f"[Interaction]\nUser: {user_input}")

                if not self.commandHandler.execute(user_input):
                    
                    if self.audio_event.is_set():
                        print(audio_input)
                        
                        if audio_input.strip() != "":
                            self.screen.add_chat_text(audio_input, "You")
                            self.screen_queue.put(audio_input)
                    elif user_input.strip() != "":
                        self.screen_queue.put(user_input)

            # Getting a movement vector from chatGPT
            mVector = [0, 0]
            try: 
                data = self.chatgpt_queue.get(False)
                mVector = data.get("mVector")
                
                clear_text = data.get("content")
                
                if data.get("role") == "Error":
                    self.screen.add_chat_text(clear_text, "Error")
                else:
                    self.screen.add_chat_text(clear_text, self.prompt[0])
                
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
                if self.gameStats[1][0] == 0:
                    self.gameHandler.remove_debuffs(self.player)
                # Applying debuffs in case of rough request
                if mVector == [-1, -1]:
                    self.gameHandler.apply_debuffs(self.player, self.maze)
                    debuffInfos = self.gameHandler.get_applied_debuffs()
                    for debuff in debuffInfos:
                        self.screen.add_chat_text(debuff, "System")
                    
                # Running till a wall
                while not mVector in [[0, 0], [-1, -1]]:
                    # Showing end screen if finish arrived
                    if self.gameHandler.check_finish(self.player.currentPosition):
                        self.gameHandler.end_game(self.player)
                        self.gameOver_event.set()
                        # Print end message
                        self.commandHandler.execute("__/finish")
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
                        self.movementStopped = True
                        break

                    self.player.move(mVector)

                    self.screen.update_screen(self.maze, self.player, self.gameStats[1][1])
                    time.sleep(0.3)
                    
                if self.movementStopped:
                    self.movementStopped = False
                    # Stock player position (in non-rotated maze)
                    position = self.player.get_rotated_position(4 - self.gameStats[1][2])
                    print(f"[Movement stopped]\nPlayer position: {position}")

                self.update_game_stats()
                
            self.screen.update_screen(self.maze, self.player, self.gameStats[1][1])
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
        self.player.change_name(self.prompt[0])
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

        self.screen.update_screen(self.maze, self.player, self.gameStats[1][1])
        
        self.clear_queues()
        self.restart_chatGPT_thread()       
       
    def choose_difficulty(self):
        level = ""
        
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
                    name = self.prompt[0]
                    chatgpt.text_to_audio(data["content"],name=name)
                    self.audio_is_ready_event.set()
                
                data["role"] = "GPT-4o" 
                self.chatgpt_queue.put(data)
            except queue.Empty:
                pass
            except OSError as e:
                #This is a huge problem. We most certainly need to restart the entire program.
                data["mVector"] = [0, 0]
                data["content"] = "Ohhhhhh, da ist etwas gewaltig schiefgelaufen, wenden sie sich bitte an die betreuenden Studenten :("
                data["role"] = "Error"
                print("FATAL ERROR")
                pass
            except openai.APIError as e: 
                data["mVector"] = [0, 0]
                data["content"] = "Ups es scheint als könnte ich die OpenAI Server nicht erreichen. Versuch es doch einfach nochmal :)"
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
        self.gameStats = self.gameHandler.get_game_stats()      #[[(active)maze], [debuffDuration, renderDistance, rotationCounter]]
        self.maze = self.gameStats[0]

    def clear_queues(self):
        self.chatgpt_queue.queue.clear()
        self.screen_queue.queue.clear()
        
    def restart_chatGPT_thread(self):
        self.gameOver_event.set()
        self.chatGPT_thread.join()
        self.gameOver_event.clear()
        
        self.chatgpt = ChatGPT(self.apiClient)

        self.chatGPT_thread = threading.Thread(target=self.__get_chatgpt_response,
                                               kwargs={
                                                "chatgpt"   : self.chatgpt,
                                                "prompt"    : self.prompt[1]
                                                })
        self.chatGPT_thread.start()