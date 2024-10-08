from ChatGPT_Client import ApiClientCreator
from ChatGPT_Controller import ChatGPT
from CommandHandler import Command
from GameHandler import GameHandler
from Player import Player
from Screen import Screen
import queue, threading, time, openai


class Game():
    """
    Game class is a general class that combines all other classes\n
    together in one single restart- and resettable session.

    Attributes
    ----------
    screen : Screen
        An instance of the Screen class that is responsible for\n
        drawing the GUI and receiving user inputs (voice and text).
    chatGPT : ChatGPT
        An instance of the ChatGPT_Controller class that is responsible\n
        for processing the conversation between user and OpenAI's GPT models.
    prompt : list[str]
        The current prompt to set a ChatGPT model onto.\n
        Contains the name of the associated character at [0] and the prompt line at [1].
    maze : list[list[int]]
        The current maze preset's section the player is on.
    audio_event : threading.Event
        A flag to switch between text and audio input/output.
    _gameHandler : GameHandler
        An instance of the GameHandler class that manages game logic and state.
    player : Player
        An instance of the Player class representing the player in the game.
    _apiClient : ApiClientCreator
        An instance of the ApiClientCreator class to create a access point to OpenAI's API.
    _commandHandler : Command
        An instance of the Command class to handle user commands.
    _idleTimer : threading.Timer
        A timer for switching idle frames.
    _audio_is_ready_event : threading.Event
        An event to signal when audio is ready.
    _gameOver_event : threading.Event
        An event to signal when the game is over.
    _screen_queue : queue.Queue
        A queue to handle screen inputs.
    _chatgpt_queue : queue.Queue
        A queue to handle ChatGPT responses.
    _chatGPT_thread : threading.Thread
        A thread to handle ChatGPT responses.

    Methods
    -------
    run()
        The main loop of the game. Starts the current session after setup.
    reset()
        Resets the current session to initial state. Lets the user select
        new difficulty.
    restart()
        Resets the current session to the start state. Lets the user retry
        current maze from the beginning.
    close()
        Closes the game with finishing pygame and used threads.
    __move_until_wall(mVector)
        Moves the player towards the given move vector till the next wall
        or finish point.
    __rough_request_debuff()
        Lets GameHandler apply debuffs and print them in chat afterwards.
    __get_movement()
        Retrieves the movement vector from the ChatGPT response.
    __get_audio_user_input()
        Retrieves the user's audio input as text.
    __is_command(user_input)
        Checks if the user input is a command and executes it.
    __choose_difficulty()
        Lets the user choose the next difficulty and start a new game.
    __get_chatgpt_response(chatgpt, prompt)
        Retrieves and processes responses from the ChatGPT model.
    __run_idle()
        Updates idleTimer if expired according to time stamp of current idle frame.
    __stop_idle()
        Stops idle animations by cancelling and finishing active idleTimers.
    __switch_idle_frame()
        Switches active maze (idle frame) to the next one.
    __update_game_stats()
        Gets new gameStats[] with active(switched/rotated) maze as well as debuff's infos.
    __clear_queues()
        Clears the ChatGPT and screen input queues.
    __restart_chatGPT_thread()
        Restarts the ChatGPT response handling thread.
    """
    
    
    def __init__(self):
        ###################################################################################################
        #The ChatGPT_Controller expects the json file to be in the same directory as ChatGPT_Controller.py
        #and it musst contain a key-value-pair where the key is called: "api_key"
        ###################################################################################################
        _CONFIG_FILE_NAME = "config.json"
                
        self.screen = Screen()
        self.screen.setup_screen(1)
        
        self._gameHandler = GameHandler()
        # Setting start idle frame (maze)
        self.maze = self._gameHandler.get_game_stats()[0]
        # and a timer for switching idle frames
        self._idleTimer = threading.Timer(self.maze[3], self.__switch_idle_frame)
        self.player = Player(self.maze[1])
        
        self._apiClient = ApiClientCreator.get_client(file_name=_CONFIG_FILE_NAME)
        self.chatgpt = ChatGPT(self._apiClient)
        
        # Print welcome message by initializing CommandHandler
        self._commandHandler = Command(self)
        
        self.__choose_difficulty()
        # Print start message
        self._commandHandler.execute("__/start")
        
        self.prompt = self._gameHandler.prompt               # [name, promptLine]
        self._gameStats = self._gameHandler.get_game_stats() # [[(active)maze], [debuffDuration, renderDistance, rotationCounter]]
        self.maze = self._gameStats[0]
        
        self.audio_event = threading.Event()
        self._audio_is_ready_event = threading.Event()
        self._gameOver_event = threading.Event()
        self._screen_queue = queue.Queue()
        self._chatgpt_queue = queue.Queue()
        self._chatGPT_thread = threading.Thread(target=self.__get_chatgpt_response, kwargs={
            "chatgpt"   : self.chatgpt,
            "prompt"    : self.prompt[1]
        })
        
        self._chatGPT_thread.start()
    
    
    def run(self):
        """
        The main game loop related to the current Game instance.

        Returns:
            None : Doesn't return any value.
        """
        running = not self.screen.isQuit
        while running:    
            self.screen.update_screen(maze= self.maze, player= self.player, render= self._gameStats[1][1])
            running = not self.screen.isQuit
            
            user_input = ""
            
            user_input = self.__get_audio_user_input()
            
            if self.screen.on_return():
                user_input = self.screen.get_user_input()
            
            user_input = user_input.strip()
            
            if user_input != "":
                print(f"[Interaction]\nUser: {user_input}")
                self.screen.add_chat_text(user_input, "You")
            
                if not self.__is_command(user_input):
                    self._screen_queue.put(user_input)
            
            mVector = self.__get_movement()
           
            if self._gameHandler.isGameOver:
                self.__run_idle()                
                continue
            
            if mVector == [-1, -1]:
                self.__rough_request_debuff()
            
            if not mVector in [[0, 0], [-1, -1]]:
                self.__move_until_wall(mVector)

            self.__update_game_stats()    
        
    
    def close(self):
        """
        Closes the game with finishing pygame and used threads.
        
        Returns:
            None : Doesn't return any value.
        """
        if self._idleTimer.is_alive():
            self.__stop_idle()
        self._gameOver_event.set()
        self._chatGPT_thread.join()
        self.screen.quit_game()


    def __move_until_wall(self, mVector: list[int]):
        """
        Moves the player towards the given move vector till the next wall\n
        or finish point. If the player runs out of maze, it'll be switched to\n
        the next one according to maze preset's connection.
        
        Parameters
        ----------
            mVector : list[int]
                The movement vector to add to player's position.
        
        Returns:
            None : Doesn't return any value.
        """
        while True:
            # Showing end screen if finish arrived
            if self._gameHandler.check_finish(self.player.currentPosition):
                print(f"[Session ended]\nPlayer successfully arrived the finish at {self.maze[2]} (~ UwU)~")
                
                self._gameHandler.reset_game(player = self.player, isFinished = True)
                self._gameOver_event.set()
                # Print end message
                self._commandHandler.execute("__/finish")
                break
            
            nextStep = [self.player.currentPosition[0] + mVector[0], self.player.currentPosition[1] + mVector[1]]

            # Going to the next section of the maze preset if reached the border
            if self._gameHandler.check_border(nextStep):
                self._gameHandler.switch_section(self.player)
                self.__update_game_stats()
                nextStep = [self.player.currentPosition[0] + mVector[0], self.player.currentPosition[1] + mVector[1]]
            
            # Stop moving in front of a wall
            if self._gameHandler.check_wall(nextStep):
                self._gameHandler.reduce_debuffs(self.player)
                break
            
            self.player.move(mVector)
            self.screen.update_screen(self.maze, self.player, self._gameStats[1][1])
            time.sleep(0.3)
        
        # Console output of player position for debugging
        position = self.player.get_rotated_position(4 - self._gameStats[1][2])   # Stock player position (in non-rotated maze)
        print(f"[Movement stopped]\nPlayer position: {position}")


    def __rough_request_debuff(self):
        """
        Lets GameHandler apply debuffs and print them in chat afterwards.
        
        Returns:
            None : Doesn't return any value.
        """
        debuffInfos = self._gameHandler.apply_debuffs(self.player)
        for debuff in debuffInfos:
            self.screen.add_chat_text(debuff, "System")

    
    def __get_movement(self):
        """
        Retrieves the movement vector from the ChatGPT response.

        This method fetches the movement vector from the ChatGPT response queue.
        It also calls the display/audio methods of the screen class in order to display/playback the ChatGPT response.

        Parameters
        ----------
        None

        Returns
        -------
        list[int]
            The movement vector indicating the direction of movement.
        """
        mVector = [0, 0]
        try: 
            data = self._chatgpt_queue.get(False)
            mVector = data.get("mVector")
            
            chatGPt_content = data.get("content")
            
            if data.get("role") == "Error":
                self.screen.add_chat_text(chatGPt_content, "Error")
            else:
                self.screen.add_chat_text(chatGPt_content, self.prompt[0])
                
            if self.audio_event.is_set():
                self._audio_is_ready_event.wait()
                self.screen.play()
                self._audio_is_ready_event.clear()
        except queue.Empty:
            pass
        
        return mVector
    
    
    def __get_audio_user_input(self):
        """
        Retrieves the user's audio input as text.

        This method checks if the audio mode is enabled and processes the
        push-to-talk (PTT) and audio return events to capture the user's
        audio input and convert it to text.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The user's audio input converted to text.
        """
        audio_input_as_text = ""

        if self.audio_event.is_set():
            
            self.screen.audio_mode=True
            
            if self.screen.ptt() and self.screen.on_audio_return():
                print("Audio input is ready")
                try:
                    audio_input_as_text = self.chatgpt.audio_to_text()
                except openai.APIError as e:
                    print("Audio to text Api call failed!")
                    print(e)
                    self.screen.add_chat_text("Ups, es scheint als könnte ich dich nicht verstehen. Versuch es doch einfach nochmal :)", "Error")
                    audio_input_as_text = ""
                    pass
        else:
            self.screen.audio_mode=False  
        
        return audio_input_as_text
        
    
    def __is_command(self, user_input):
        """
        This method checks if the user input is a command and executes it
        using the CommandHandler instance.

        Parameters
        ----------
        user_input : str
            The input provided by the user.

        Returns
        -------
        bool
            True if the input was a command and was executed, False otherwise.
        """    
        return self._commandHandler.execute(user_input)

    
    def reset(self):
        """
        Resets the game to the start instance (selecting difficulty).

        Returns:
            None : Doesn't return any value.
        """
        self.__stop_idle()
        self._gameHandler.reset_game(self.player)
        self.__update_game_stats()
        
        self.__choose_difficulty()    # gameStats will be additionally updated here
        
        self.audio_event.clear()

        self.__clear_queues()
        self.__restart_chatGPT_thread()

    
    def restart(self):
        """
        Lets the user retry the current maze with the current prompt.
        Doesn't reset chatgpt history.

        Returns:
            None : Doesn't return any value.
        """
        self.__stop_idle()
        self._gameHandler.restart_game(self.player)

        self.__update_game_stats()

        self.screen.update_screen(self.maze, self.player, self._gameStats[1][1])
        
        self.__clear_queues()
        self.__restart_chatGPT_thread()       

       
    def __choose_difficulty(self):
        """
        Lets the user choose the next difficulty and start a new game.\n
        The choice is given to GameHandler instance to receive\n
        a ChatGPT prompt and selected maze.

        Returns:
            None : Doesn't return any value.
        """
        self.screen.add_chat_text("Please chose a difficulty: EASY, NORMAL, HARD", "System")
        options = ["TEST", "EASY", "NORMAL", "HARD"]
        level = ""
        
        while level == "":    
            level = self.screen.get_user_input()
            level = level.strip().upper()
            
            # Drawing idle frame (maze)
            self.__run_idle()
            self.screen.update_screen(self.maze, self.player)
            
            if level == "":
                continue
            if not level in options:
                self.screen.add_chat_text("A valid one, please.", "System")
                level = ""
                print(f"<{level}>")
        
        self._gameHandler.set_level(self.player, level)
        self.__update_game_stats()
        self.prompt = self._gameHandler.prompt

        self.__stop_idle()
        self.screen.clear_chat_text()
        
       
    def __get_chatgpt_response(self, chatgpt, prompt):
        """
        Retrieves and processes responses from the ChatGPT model.

        This method runs in a separate thread and continuously fetches user inputs
        from the screen queue and sends them to the ChatGPT model. 

        Parameters
        ----------
        chatgpt : ChatGPT
            An instance of the ChatGPT class used to interact with the ChatGPT model.
        prompt : str
            The initial prompt to set the context for the ChatGPT model.

        Returns
        -------
        data : dict
            A dictionary containing the movement vector and the ChatGPT response.
            In order to be processed by the main game loop the data is put into the chatGPT queue.
        """
        from ChatGPT_Movment_Controller import chatgpt_movment
        
        #map character names to voices
        #for reference, see the OpenAI API documentation: https://platform.openai.com/docs/guides/text-to-speech/overview        
        voices={ "Prinz Reginald":"onyx", "Larry":"echo","Clyde":"shimmer","Lawrie":"fable", "Imane":"alloy","Sophia":"nova"}
        
        gpt_model = "gpt-4o"
        temperatur = 0.25
        data = {
            "content": "",
            "role": "GPT-4o",
            "mVector": [0, 0]
        }

        movmentChatGPT = chatgpt_movment(chatgpt=chatgpt, model=gpt_model)

        while not self._gameOver_event.is_set():
            try:        
                msg = self._screen_queue.get(False)
                #chatGPT call
                data["mVector"], data["content"] = movmentChatGPT.get_vector(msg, temperatur, prompt)
                
                if self.audio_event.is_set():
                    name = self.prompt[0]
                    current_voice = voices.get(name, "onyx")
                    chatgpt.text_to_audio(data["content"],voice=current_voice)
                    self._audio_is_ready_event.set()
                
                data["role"] = "GPT-4o" 
                self._chatgpt_queue.put(data)
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
                self._chatgpt_queue.put(data)
                print("API CALL ERROR")
                pass

            
    def __run_idle(self):
        """
        Updates idleTimer if expired according to time stamp\n
        of current idle frame.
        
        Returns:
            None : Doesn't return any value.
        """
        if self._idleTimer.is_alive():
            return
        # Duration of current frame
        runTime = self.maze[3]
        
        self._idleTimer = threading.Timer(runTime, self.__switch_idle_frame)
        self._idleTimer.start()

    
    def __stop_idle(self):
        """
        Stops idle animations by cancelling and finishing active idleTimers.
        
        Returns:
            None : Doesn't return any value.
        """
        self._idleTimer.cancel()
        self._idleTimer.join()

    
    def __switch_idle_frame(self):
        """
        Switches active maze (idle frame) to the next one.\n
        ! **Only used in idleTimer threads** !\n
        ! **Only used with FINISH and IDLE presets** !
        
        Returns:
            None : Doesn't return any value.
        """
        self._gameHandler.switch_idle_maze()
        self.__update_game_stats()

    
    def __update_game_stats(self):
        """
        Gets new gameStats[] with active(switched/rotated) maze\n
        as well as debuff's infos.
                
        Returns:
            None : Doesn't return any value.
        """
        self._gameStats = self._gameHandler.get_game_stats()      #[[(active)maze], [debuffDuration, renderDistance, rotationCounter]]
        self.maze = self._gameStats[0]


    def __clear_queues(self):
        """
        Clears the ChatGPT and screen input queues.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._chatgpt_queue.queue.clear()
        self._screen_queue.queue.clear()

        
    def __restart_chatGPT_thread(self):
        """
        Restarts the ChatGPT response handling thread.

        This method stops the current ChatGPT thread, waits for it to finish,
        and then starts a new thread to handle ChatGPT responses. It also
        reinitializes the ChatGPT instance.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._gameOver_event.set()
        self._chatGPT_thread.join()
        self._gameOver_event.clear()
        
        self.chatgpt = ChatGPT(self._apiClient)

        self._chatGPT_thread = threading.Thread(target=self.__get_chatgpt_response,
                                               kwargs={
                                                "chatgpt"   : self.chatgpt,
                                                "prompt"    : self.prompt[1]
                                                })
        self._chatGPT_thread.start()