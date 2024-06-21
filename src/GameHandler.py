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
            1: ["ROTATION", self.maze_rotation],
            2: ["BLINDNESS", self.blind],
            3: ["INVISIBILITY", self.set_invisible],
            4: ["RANDOM MOVE", self.random_move],
            5: ["TELEPORT", self.teleport]
            }
        self.PROMPT_LIBRARY = {}
        self.PROMPT = [] # [name, promptLine]
        
        file_prompts = Path(__file__).parent / "prompts.json"
        file_prompts.resolve()
        
        # Loading prompt library and choosing a start ChatGPT prompt
        with open(file_prompts) as json_file:
            data = json.load(json_file)
            self.PROMPT_LIBRARY = data
            # {"Name" : "Prompt"} pair
            item = data["TEST"][0]
            key = "TEST 1"
            
            self.PROMPT = [key, item[key]]
        
        self.moves = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        self.debuffDuration = 0
        self.renderDistance = 16
        self.rotationCounter = 0
        
        self.mazeGenerator = MazeGenerator()
        self.startMazePreset = "FINISH_2.0"
        self.activeMazePreset = "FINISH_2.0"
        self.maze = self.mazeGenerator.get_preset(self.startMazePreset)
        self.difficulty = self.DIFFICULTY["TEST"]
        
        self.gameOver = False        
        
    def set_level(self, level):
        self.difficulty = self.DIFFICULTY.get(level, False)
        if self.difficulty == False:
            return False
    
        print(f"Selected difficulty: {level}")
        
        self.__get_random_maze()
        self.__get_random_prompt()
        
        return True
    
    def __get_random_maze(self):
        preset = f"maze_{self.difficulty[0]}.{random.randint(1, 3)}.0"
        self.startMazePreset = preset
        self.activeMazePreset = preset
        self.maze = self.mazeGenerator.get_preset(self.startMazePreset)
        
        print(f"Getting maze preset: {self.startMazePreset}")
    
    def __get_random_prompt(self):
        options = ["TEST", "EASY", "NORMAL", "HARD"]
        
        promptPreset = options[self.difficulty[0]]
        promptNumber = random.choice([0, 1])
        
        key = list(self.PROMPT_LIBRARY[promptPreset][promptNumber].keys())[0]
        promptLine = self.PROMPT_LIBRARY[promptPreset][promptNumber][key]
        key = "Prinz Reginald"
        promptLine = self.PROMPT_LIBRARY["EASY"][0][key]

        self.PROMPT = [key, promptLine]
        print(f"In this round ChatGPT is {key}")

    """
    Returns True if player stucks against a wall
    """
    def check_wall(self, playerPosition):
        return self.maze[0][playerPosition[1]][playerPosition[0]] == 1
    """
    Returns True if player arrived the end point of a maze
    """
    def check_finish(self, playerPosition):
        return self.maze[2] == playerPosition
    """
    Rerurns True if player went out of maze (16x16 area)
    """
    def check_border(self, playerPosition):
        return not (playerPosition[0] in range(0, 16) and playerPosition[1] in range(0, 16))
    
    def maze_rotation(self, player, maze = 0):
        self.rotationCounter = (self.rotationCounter + 1) % 4 if maze != 0 else self.rotationCounter
        self.maze = self.mazeGenerator.rotate_maze(self.maze)
        
        newPosition = player.get_rotated_position()
        player.set_position(newPosition)
    
    def blind(self, player = 0, maze = 0):
        self.renderDistance = 4
        self.debuffDuration = self.difficulty[2]
    
    def random_move(self, player, maze):
        randOption = random.randint(0, 3)
        mVector = self.moves[randOption]
        player.move(mVector)
        while self.check_wall(player.currentPosition):
            player.move([-mVector[0], -mVector[1]])
            randOption = random.randint(0, 3)
            mVector = self.moves[randOption]
            player.move(mVector)
    
    def teleport(self, player, maze):
        player.set_position(self.mazeGenerator.get_random_point(maze))
    
    def set_invisible(self, player, maze = 0):
        player.hide(True)
        self.debuffDuration = self.difficulty[2]
    """
    Applying debuffs whether because of running against a wall (case = 1)
    or rough request (case = 3)
    """
    def apply_debuffs(self, player, maze):
        cases = 3 if self.startMazePreset[5:-2] == "3.3" else 5
        cases = 1
        for i in range(self.difficulty[1]):
            choice = random.randint(1, cases)
            self.DEBUFFS[choice][1](player, maze)
            
            print(f"{self.DEBUFFS[choice][0]} were applied")
    """
    Reducing debuff duration by 1 (every step)
    """
    def reduce_debuffs(self):
        self.debuffDuration = max(0, self.debuffDuration - 1)
    """
    Removing all temporary debuffs
    """
    def remove_debuffs(self, player):
        self.renderDistance = 16
        player.hide(False)
    """
    Switches maze preset's section according to preset connection setting (graph)
    """
    def switch_section(self, player):
        graph = self.mazeGenerator.get_preset_connections(self.activeMazePreset)
        
        # Last int of a preset
        startSection = self.activeMazePreset[-1]
        # Stock player position (in non-rotated maze)
        playerPosition = player.get_rotated_position(4 - self.rotationCounter);
        
        # bridge = [target_section, start_point (active section), end_point]
        for bridge in graph[startSection]:
            if bridge[1] == playerPosition:
                print(f"[Section switch]\nfrom: {self.activeMazePreset} : {playerPosition}")
                self.activeMazePreset = f"{self.activeMazePreset[:-1]}{bridge[0]}"
                self.maze = self.mazeGenerator.get_preset(self.activeMazePreset)
                
                player.set_position(bridge[2])
                print(f"to {self.activeMazePreset} : {bridge[2]}")
                break

        for i in range(self.rotationCounter):
            self.maze_rotation(player)
    """
    Restarts current session without changing difficulty and GPT prompt
    """
    def restart_game(self, player):
        self.remove_debuffs(player)
        self.gameOver = False
        
        self.activeMazePreset = self.startMazePreset
        self.maze = self.mazeGenerator.get_preset(self.startMazePreset)
        player.set_position(self.maze[1])

        self.debuffDuration = 0
        self.renderDistance = 16
        self.rotationCounter = 0
    """
    Resets all properties to initial values
    """
    def reset_game(self, player):
        self.restart_game(player)
        
        choice = random.randint(1, 2)
        self.startMazePreset = f"FINISH_{choice}.0"
        self.activeMazePreset = f"FINISH_{choice}.0"
        
        self.maze = self.mazeGenerator.get_preset(self.startMazePreset)
        player.set_position(self.maze[1])
    """
    Finishes the session depending on end event
    """
    def end_game(self, player, case = "FINISH"):
        if case == "DEATH":
            pass
        if case == "FINISH":
            self.remove_debuffs(player)
            player.hide(True)
            
            self.activeMazePreset = f"FINISH_{random.randint(0, 2)}.0"
            self.maze = self.mazeGenerator.get_preset(self.activeMazePreset)
            self.gameOver = True
    """
    Access function for use in GameLoop class
    """
    def get_game_stats(self):
        return [self.difficulty, self.maze, [self.debuffDuration, self.renderDistance, self.rotationCounter]]
    """
    Returns session's status (finish arrived)
    """
    def is_game_over(self):
        return self.gameOver
    """
    Returns selected prompt
    """
    def get_prompt(self):
        return self.PROMPT
    """
    Returns the name of active maze section
    """
    def get_active_maze_preset(self):
        return self.activeMazePreset
    """
    Returns the [nextFrame]th idle screen's frame
    !Only used with FINISH and IDLE presets!
    """
    def get_idle_maze(self, nextFrame):
        preset = self.activeMazePreset[-3]
        animationPreset = f"IDLE_{preset}"
        
        self.activeMazePreset = f"{animationPreset}.{nextFrame}"
        frame = self.mazeGenerator.get_preset(self.activeMazePreset)
        
        return frame