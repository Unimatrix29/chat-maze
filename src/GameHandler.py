from MazeGenerator import MazeGenerator 
from pathlib import Path
from Player import Player
import json, random

class GameHandler():
    """
    GameHandler class implies debuffing functionality,
    difficulty selection based on user input and
    maze presets' transition including start and end presets screens.

    Attributes
    -----------
        prompt : [name : str, prompt_line : str]
            A prompt with name and role description for ChatGPT setup.
        maze : [maze_map : list[16x16 int],
                    start_point : [int, int],
                    finish_point : [int, int],
                    next_frame : int (optional)
                    frame_duration : int (optional)]
            A maze object represented as list of lists of int.
            Optional indexes are used in idle frames.
        debuffDuration : int = 0
            Applied debuffs last this amount of moves.
            Updates every time a new debuff is applied (doesn't stack).
        renderDistance : int = 17
            A range of tiles around player to be displayed.
        rotationCounter : int = 0
            Amount of rotations by 90 degrees counterclockwise
            applied to the current maze.
        isGameOver : bool = False
            A flag to be set when finish is arrived.

    Methods
    -----------
        set_level (player : Player, level : str = "TEST")
            Sets a maze preset and prompt according to given level (difficulty).
        check_wall (position : [int, int]) -> bool
            Checks if there's a wall on the given position.
        check_finish (position : [int, int]) -> bool
            Checks if the given position is the finish of the maze.
        check_border (position : [int, int]) -> bool
            Checks if the given position lays outside the maze.
        apply_debuffs (player : Player) -> list[str]
            Applies single or multiple debuffs to the given player instance
            depending on selected difficulty.
        reduce_debuffs (player : Player)
            Reduces current debuffDuration by 1 and cleares all temporary debuffs
            applied by their expiration.
        switch_section (player : Player)
            Switches active maze to another one according to pre-defined
            preset connections.
        restart_game (player : Player)
            Restarts current game session without changing selected
            difficulty, maze or ChatGPT prompt.
        reset_game (player : Player, isFinished : bool = False)
            Sets the current session to initial/end state.
        switch_idle_maze (nextFrame : int)
            Returns (the next) idle screen's frame.
        get_game_stats () -> list[list[int]]
            Returns all game related variables such as active maze and debuffs. 
    """
    
    def __init__(self):
        self._DIFFICULTY = {
            "TEST"  :   [0, 1, 1],
            "EASY"  :   [1, 0, 2], #[maze_preset_level, wall_penalties, debuff_duration]
            "NORMAL":   [2, 1, 5],
            "HARD"  :   [3, 3, 10]
            }
        
        self._DEBUFFS = {
            1: ["ROTATION",     self.__maze_rotation],
            2: ["BLINDNESS",    self.__blind],
            3: ["INVISIBILITY", self.__set_invisible],
            4: ["RANDOM MOVE",  self.__random_move],
            5: ["TELEPORT",     self.__teleport]
            }
        self._DEBUFF_INFOS = {}
        
        # Loading debuffs' descriptions
        _file_debuffsTexts = Path(__file__).parent / "debuffs_texts.json"
        _file_debuffsTexts.resolve()       
        with open(_file_debuffsTexts) as json_file:
            data = json.load(json_file)
            
            self._DEBUFF_INFOS = data

        self._PROMPT_LIBRARY = {}
        self.prompt = [] # [name, promptLine]
        
        # Loading prompt library and choosing a start ChatGPT prompt
        _file_prompts = Path(__file__).parent / "prompts.json"
        _file_prompts.resolve()
        with open(_file_prompts) as json_file:
            data = json.load(json_file)
            
            self._PROMPT_LIBRARY = data
            
            # {"Name" : "Prompt line"} pair
            key = "TEST 1"
            item = data["TEST"][key]
            self.prompt = [key, item]
        
        # Maze generation's variables
        self._difficulty = self._DIFFICULTY["TEST"]
        self._mazeGenerator = MazeGenerator()
        self._startMazePreset = "FINISH_2.0"
        self._activeMazePreset = "FINISH_2.0"
        self.maze = self._mazeGenerator.get_preset(self._startMazePreset)
        
        # Debuffing variables
        self.debuffDuration = 0
        self.renderDistance = 17
        self.rotationCounter = 0
        
        # Finish flag
        self.isGameOver = False        
        
    def set_level(self, player: Player, level: str = "TEST"):
        """
        Sets difficulty to a given level, maze preset
        and ChatGPT prompt as well as configures the player
        according to selections.
        
        Parameters:
            player : Player
                An instance of a player to configure.
            level : str = "TEST"
                The chosen difficulty to set GameHandler class to.
        
        Returns:
            None : Doesn't return any value.
        """
        self._difficulty = self._DIFFICULTY[level]
    
        print(f"Selected difficulty: {level}")
        
        self.__set_random_maze(level)
        self.__set_random_prompt(level)

        player.change_name(self.prompt[0])
        player.set_position(self.maze[1])
        
        self.isGameOver = False
    
    def __set_random_maze(self, level: str = "TEST"):
        presetList = [1, 2, 3] if level != "TEST" else [1]
        preset = f"maze_{self._difficulty[0]}.{random.choice(presetList)}.0"
        
        self._startMazePreset = preset
        self._activeMazePreset = preset
        self.maze = self._mazeGenerator.get_preset(self._startMazePreset)
        
        print(f"Setting maze preset: {self._startMazePreset}")
    
    def __set_random_prompt(self, level: str = "TEST"):        
        keyList = list(self._PROMPT_LIBRARY[level].keys())
        key = random.choice(keyList)
        
        promptLine = self._PROMPT_LIBRARY[level][key]

        self.prompt = [key, promptLine]
        print(f"In this round ChatGPT is {key}")
        
    def check_wall(self, position: list[int]) -> bool:
        """
        Checks if there's a wall on the given position.
        
        Parameters:
            position: [int, int]
                The point of the maze to be checked.
        
        Returns:
            bool : True if there's a wall on a given position, False otherwise.
        """
        return self.maze[0][position[1]][position[0]] == 1
    
    def check_finish(self, position: list[int]) -> bool:
        """
        Checks if the given position is the finish of the maze.
        
        Parameters:
            position: [int, int]
                The point of the maze to be checked.
        
        Returns:
            bool : True if the given position is the finish, False otherwise.
        """
        return self.maze[2] == position
    
    def check_border(self, position: list[int]) -> bool:
        """
        Checks if the given position is inside the maze.
        
        Parameters:
            position: [int, int]
                The point to be checked.
        
        Returns:
            bool : True if both coordinates of the given position,
                       are in range of 0 to 15, False otherwise.
        """
        return not (position[0] in range(0, 16) and position[1] in range(0, 16))
    
    def __maze_rotation(self, player: Player, debuffApplied: bool = True):
        """
        Rotates active maze 1 time using MazeGenerator.rotate_maze()
        including setting new player position.
        
        Parameters:
            player : Player
                An instance of a player to rotate with the maze.
            debuffApplied : bool = True
                A flag to increment rotationCounter if rotation was applied as a debuff.
            
        Returns:
            None : Doesn't return any value.
        """
        # Increment rotationCounter if debuff was applied
        self.rotationCounter = (self.rotationCounter + 1) % 4 if debuffApplied else self.rotationCounter
        self.maze = self._mazeGenerator.rotate_maze(self.maze)
        
        newPosition = player.get_rotated_position()
        player.set_position(newPosition)
    
    def __blind(self, player: Player = None):
        """
        Reduces render distance and updates current debuffDuration.
        
        Parameters:
            player : Player = None
                Optional. Used to fit in delegate calls in apply_debuffs().
        
        Returns:
            None : Doesn't return any value.
        """
        self.renderDistance = 4
        self.debuffDuration = self._difficulty[2]
    
    def __random_move(self, player: Player):
        """
        Moves the player in a random direction onto the next field
        that's not a wall.
        
        Parameters:
            player : Player
                An instance of a player to move.
        
        Returns:
            None : Doesn't return any value.
        """
        moves = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        while True:    
            randOption = random.randint(0, 3)
            mVector = moves[randOption]
            nextStep = [player.currentPosition[0] + mVector[0], player.currentPosition[1] + mVector[1]]
            
            if not self.check_wall(nextStep):
                break
                
        player.move(mVector)
    
    def __teleport(self, player: Player):
        """
        Sets the player's current position to a random point of the maze.
        
        Parameters:
            player : Player
                An instance of a player to teleport.
        
        Returns:
            None : Doesn't return any value.
        """
        player.set_position(self._mazeGenerator.get_random_point(self.maze))
    
    def __set_invisible(self, player: Player):
        """
        Hides the player so it won't be rendered and updates
        the current debuffDuration.
        
        Parameters:
            player : Player
                An instance of a player to hide.
        
        Returns:
            None : Doesn't return any value.
        """
        player.hide(True)
        self.debuffDuration = self._difficulty[2]
    
    def apply_debuffs(self, player: Player) -> list[str]:
        """
        Applies debuffs to a player. The amount of applied debuffs 
        is defined by selected difficulty. Every debuff can be applied
        maximum 1 time pro this function's call.
        
        Parameters:
            player : Player
                An instance of a player to apply debuffs onto.
        
        Returns:
            debuffInfosList : list[str]
                A list with applied debuffs' descriptions.
        """
        # Avoiding teleporting and random moving in maze_3.3 (start in void)
        cases = 3 if self._startMazePreset[5:-2] == "3.3" else 5
        
        debuffList = []
        
        while not len(debuffList) == self._difficulty[1]:
            choice = random.randint(1, cases)
            if choice in debuffList:
                continue
            
            debuffList.append(choice)
            self._DEBUFFS[choice][1](player)
            
            print(f"{self._DEBUFFS[choice][0]} were applied")
        
        # Packing applied debuffs' descriptions
        debuffInfosList = []
        for debuff in debuffList:
            debuffName = self._DEBUFFS[debuff][0]
            debuffInfosList.append(self._DEBUFF_INFOS[debuffName])
            
        return debuffInfosList
    
    def reduce_debuffs(self, player: Player):
        """
        Reduces debuffs' duration by 1 and clearing them if expired.
        Only player visibility and render distance will be restored by
        this method.
        
        Parameters:
            player : Player
                An instance of a player to clear from debuffs.
        
        Returns:
            None : Doesn't return any value.
        """
        # A flag to avoid unnecessary debuff clearance
        isDebuffExpired = self.debuffDuration == 1
        
        self.debuffDuration = max(0, self.debuffDuration - 1)
        # Removing all temporary debuffs by expiring their duration
        if isDebuffExpired:
            
            self.renderDistance = 17
            player.hide(False)
            
    def restart_game(self, player: Player):
        """
        Restarts current session without changing difficulty, maze
        or ChatGPT prompt. Removes all debuffs including maze rotations
        and returns the player to the beginning of the maze.
        
        Parameters:
            player : Player
                An instance of a player in current session to reset.
        
        Returns:
            None : Doesn't return any value.
        """
        # Removing debuffs
        self.debuffDuration = 1
        self.reduce_debuffs(player)
        self.rotationCounter = 0
        
        # Restarting active maze preset
        self._activeMazePreset = self._startMazePreset
        self.maze = self._mazeGenerator.get_preset(self._activeMazePreset)
        player.set_position(self.maze[1])
        
        self.isGameOver = False
    
    def reset_game(self, player: Player, isFinished: bool = False):
        """
        Restarts the game an sets the current maze to an idle frame.
        Removes all debuffs including maze rotations.
        Doesn't clear chosen difficulty or ChatGPT prompt.
        
        Parameters:
            player : Player
                An instance of a player in current session to reset.
            isFinished : bool = False
                An end game flag. If set True, the game will be considered
                as finished.
        
        Returns:
            None : Doesn't return any value.
        """
        # Removing debuffs
        self.restart_game(player)
        
        # Choosing a start(end)screen
        presetList = [0, 1, 2] if isFinished else [1, 2]
        self._activeMazePreset = f"FINISH_{random.choice(presetList)}.0"
                
        self.maze = self._mazeGenerator.get_preset(self._activeMazePreset)
        player.set_position(self.maze[1])

        self.isGameOver = isFinished
    
    def switch_section(self, player: Player):
        """
        Switches active maze according to preset's connection
        setting (graph) to the next one. Works only if the player
        is on a key point of a connection.
        
        Parameters:
            player : Player
                An instance of a player, that went to the next section.
        
        Returns:
            None : Doesn't return any value.
        """
        graph = self._mazeGenerator.get_preset_connections(self._activeMazePreset)
        sectionSwitched = False
        
        startSection = self._activeMazePreset[-1]
        # Stock player position (in non-rotated maze)
        playerPosition = player.get_rotated_position(4 - self.rotationCounter);
        
        # bridge = [target_section, start_point (active section), end_point]
        for bridge in graph[startSection]:
            if bridge[1] != playerPosition:
                continue
            
            print(f"[Section switch]\nfrom: {self._activeMazePreset} : {playerPosition}")
            self._activeMazePreset = f"{self._activeMazePreset[:-1]}{bridge[0]}"
            self.maze = self._mazeGenerator.get_preset(self._activeMazePreset)
                
            player.set_position(bridge[2])
            print(f"to {self._activeMazePreset} : {bridge[2]}")
            
            sectionSwitched = True
            break

        if not sectionSwitched:
            return
        
        for i in range(self.rotationCounter):
            # Rotating target_section by same angle as start_section
            self.__maze_rotation(player= player, debuffApplied= False)
    
    def switch_idle_maze(self):
        """
        Switches the current idle maze to the next one connected to it.
        !Used with FINISH and IDLE presets only!
        
        Returns:
            None : Doesn't return any value.
        """
        preset = self._activeMazePreset[-3]
        nextFrame = self.maze[4]
        
        self._activeMazePreset = f"IDLE_{preset}.{nextFrame}"
        self.maze = self._mazeGenerator.get_preset(self._activeMazePreset)
           
    def get_game_stats(self):
        """
        Access function for getting all game related variables such as
        active maze and debuffs.
        
        Returns:
            list[maze, [debuffDuration : int, renderDistance : int, rotationCounter : int]]
                List of all by debuffs affected variables.
        """
        return [self.maze, [self.debuffDuration, self.renderDistance, self.rotationCounter]]