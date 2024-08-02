from MazeGenerator import MazeGenerator 
from pathlib import Path
import json, random

"""
GameHandler class implies debuffing functionality,
difficulty selection based on user input and
presets' transition including start and end presets
"""
class GameHandler():
    
    def __init__(self):
        self.DIFFICULTY = {
            "TEST"  :   [0, 1, 1],
            "EASY"  :   [1, 0, 2], #[maze_preset_level, wall_penalties, debuff_duration]
            "NORMAL":   [2, 1, 5],
            "HARD"  :   [3, 3, 10]
            }
        
        self.DEBUFFS = {
            1: ["ROTATION",     self.__maze_rotation],
            2: ["BLINDNESS",    self.__blind],
            3: ["INVISIBILITY", self.__set_invisible],
            4: ["RANDOM MOVE",  self.__random_move],
            5: ["TELEPORT",     self.__teleport]
            }
        self.DEBUFF_INFOS = {}
        
        # Loading debuffs' descriptions
        _file_debuffsTexts = Path(__file__).parent / "debuffs_texts.json"
        _file_debuffsTexts.resolve()       
        with open(_file_debuffsTexts) as json_file:
            data = json.load(json_file)
            
            self.DEBUFF_INFOS = data

        self.PROMPT_LIBRARY = {}
        self.prompt = [] # [name, promptLine]
        
        # Loading prompt library and choosing a start ChatGPT prompt
        _file_prompts = Path(__file__).parent / "prompts.json"
        _file_prompts.resolve()
        with open(_file_prompts) as json_file:
            data = json.load(json_file)
            
            self.PROMPT_LIBRARY = data
            
            # {"Name" : "Prompt line"} pair
            item = data["TEST"][0]
            key = "TEST 1"
            self.prompt = [key, item[key]]
        
        # Debuffing variables
        self._moves = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        self._debuffList = []
        self._isDebuffExpired = True
        self.debuffDuration = 0
        self.renderDistance = 16
        self.rotationCounter = 0
        
        # Maze generation's variables
        self._difficulty = self.DIFFICULTY["TEST"]
        self._mazeGenerator = MazeGenerator()
        self._startMazePreset = "FINISH_2.0"
        self._activeMazePreset = "FINISH_2.0"
        self.maze = self._mazeGenerator.get_preset(self._startMazePreset)
        
        # Finish flag
        self.isGameOver = False        
        
    def set_level(self, level):
        self._difficulty = self.DIFFICULTY[level]
    
        print(f"Selected difficulty: {level}")
        
        self.__set_random_maze()
        self.__set_random_prompt()
    
    def __set_random_maze(self):
        preset = f"maze_{self._difficulty[0]}.{random.randint(1, 3)}.0"
        self._startMazePreset = preset
        self._activeMazePreset = preset
        self.maze = self._mazeGenerator.get_preset(self._startMazePreset)
        
        print(f"Setting maze preset: {self._startMazePreset}")
    
    def __set_random_prompt(self):
        options = ["TEST", "EASY", "NORMAL", "HARD"]
        
        promptPreset = options[self._difficulty[0]]
        promptNumber = random.choice([0, 1])
        
        key = list(self.PROMPT_LIBRARY[promptPreset][promptNumber].keys())[0]
        promptLine = self.PROMPT_LIBRARY[promptPreset][promptNumber][key]

        self.prompt = [key, promptLine]
        print(f"In this round ChatGPT is {key}")
    """
    Returns True if the player stucks against a wall
    """
    def check_wall(self, playerPosition):
        return self.maze[0][playerPosition[1]][playerPosition[0]] == 1
    """
    Returns True if the player arrived the end point of a maze
    """
    def check_finish(self, playerPosition):
        return self.maze[2] == playerPosition
    """
    Rerurns True if the player went out of maze (16x16 area)
    """
    def check_border(self, playerPosition):
        return not (playerPosition[0] in range(0, 16) and playerPosition[1] in range(0, 16))
    """
    Rotates active maze 1 time using MazeGenerator.rotate_maze()
    including setting new player position
    """
    def __maze_rotation(self, player, maze = 0):
        # Increment rotationCounter if debuff was applied
        self.rotationCounter = (self.rotationCounter + 1) % 4 if maze != 0 else self.rotationCounter
        self.maze = self._mazeGenerator.rotate_maze(self.maze)
        
        newPosition = player.get_rotated_position()
        player.set_position(newPosition)
    """
    Reduces render distance
    """
    def __blind(self, player = 0, maze = 0):
        self.renderDistance = 4
        self.debuffDuration = self._difficulty[2]
    """
    Moves the player in a random direction
    onto a next field that's not a wall
    """
    def __random_move(self, player, maze):
        while True:    
            randOption = random.randint(0, 3)
            mVector = self._moves[randOption]
            nextStep = [player.currentPosition[0] + mVector[0], player.currentPosition[1] + mVector[1]]
            
            if not self.check_wall(nextStep):
                break
                
        player.move(mVector)
    """
    Moves the player to a random point of the maze
    """
    def __teleport(self, player, maze):
        player.set_position(self._mazeGenerator.get_random_point(maze))
    """
    Hides the player so it won't be rendered
    """
    def __set_invisible(self, player, maze = 0):
        player.hide(True)
        self.debuffDuration = self._difficulty[2]
    """
    Applying debuffs in case of rough request
    """
    def apply_debuffs(self, player, maze):
        # Avoiding teleporting and random moving in maze_3.3 (start in void)
        cases = 3 if self._startMazePreset[5:-2] == "3.3" else 5
        
        while not len(self._debuffList) == self._difficulty[1]:
            choice = random.randint(1, cases)
            if choice in self._debuffList:
                continue
            
            self._debuffList.append(choice)
            self.DEBUFFS[choice][1](player, maze)
            
            print(f"{self.DEBUFFS[choice][0]} were applied")
    """
    Reducing debuffs' duration by 1 and clearing them if expired
    """
    def reduce_debuffs(self, player):
        # A flag to avoid unnecessary debuff clearance
        self._isDebuffExpired = self.debuffDuration == 1
        
        self.debuffDuration = max(0, self.debuffDuration - 1)
        # Removing all temporary debuffs by expiring their duration
        if self._isDebuffExpired:
            self._isDebuffExpired = False
            
            self.renderDistance = 17
            player.hide(False)
    """
    Switches maze preset's section according to preset connection setting (graph)
    """
    def switch_section(self, player):
        graph = self._mazeGenerator.get_preset_connections(self._activeMazePreset)
        
        # Last int of a preset
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
            break

        for i in range(self.rotationCounter):
            # Rotating targetSection by same angle as startSection
            self.maze_rotation(player)
    """
    Restarts current session without changing difficulty and GPT prompt
    """
    def restart_game(self, player):
        # Removing debuffs
        self.debuffDuration = 1
        self.reduce_debuffs(player)
        self.rotationCounter = 0
        
        # Restarting active maze preset
        self._activeMazePreset = self._startMazePreset
        self.maze = self._mazeGenerator.get_preset(self._startMazePreset)
        player.set_position(self.maze[1])
        
        self.isGameOver = False
    """
    Resets all properties to initial values
    """
    def reset_game(self, player):
        # Removing debuffs
        self.restart_game(player)
        
        # Choosing a start(end)screen
        choice = random.randint(1, 2)
        self._startMazePreset = f"FINISH_{choice}.0"
        self._activeMazePreset = f"FINISH_{choice}.0"
        
        self.maze = self._mazeGenerator.get_preset(self._startMazePreset)
        player.set_position(self.maze[1])
    """
    Finishes the session
    """
    def end_game(self, player):
        # Removing blindness and keep the player hidden
        self.renderDistance = 17
        player.hide(True)
        
        # Choosing an endscreen
        self._activeMazePreset = f"FINISH_{random.randint(0, 2)}.0"
        self.maze = self._mazeGenerator.get_preset(self._activeMazePreset)
        
        self.isGameOver = True
    """
    Access function for use in GameLoop class
    """
    def get_game_stats(self):
        return [self.maze, [self.debuffDuration, self.renderDistance, self.rotationCounter]]
    """
    Returns session's status (finish arrived)
    """
    def is_game_over(self):
        return self.isGameOver
    """
    Returns selected prompt
    """
    def get_prompt(self):
        return self.prompt
    """
    Returns the [nextFrame]th idle screen's frame
    !Only used with FINISH and IDLE presets!
    """
    def get_idle_maze(self, nextFrame):
        preset = self._activeMazePreset[-3]
        animationPreset = f"IDLE_{preset}"
        
        self._activeMazePreset = f"{animationPreset}.{nextFrame}"
        frame = self._mazeGenerator.get_preset(self._activeMazePreset)
        
        return frame
    """
    Returns an array with applied debuff's descriptions
    """
    def get_applied_debuffs(self):
        debuffInfos = []
        for debuff in self._debuffList:
            debuffName = self.DEBUFFS[debuff][0]
            debuffInfos.append(self.DEBUFF_INFOS[debuffName])
            
        self._debuffList.clear()
        return debuffInfos