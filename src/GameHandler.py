from MazeGenerator import MazeGenerator 
from pathlib import Path
import json, random, time

"""
GameHandler class implies debuffing functionality
and selecting difficulty
"""
class GameHandler():
    
    def __init__(self):
        self.DIFFICULTY = {
            "TEST":
            [0, 1, 1],
            "EASY":
            [1, 0, 2], #[maze_preset_level, wall_penalties, debuff_duration]
            "NORMAL":
            [2, 1, 5],
            "HARD":
            [3, 3, 10]
            }
        self.PROMPT_LIBRARY = {}
        self.PROMPT = ""
        
        file_prompts = Path(__file__).parent / "prompts.json"
        file_prompts.resolve()
        
        # Loading prompt library and chosing a start ChatGPT prompt
        with open(file_prompts) as json_file:
            data = json.load(json_file)
            self.PROMPT_LIBRARY = data
            # {"Name" : "Prompt"} pair
            item = data["TEST"][0]
            key = "TEST 1"
            
            self.PROMPT = item[key]
        
        self.moves = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        self.debuffDuration = 0
        self.renderDistance = 16
        self.rotationCounter = 0
        
        self.mazeGenerator = MazeGenerator()
        self.startMazePreset = ""
        self.activeMazePreset = ""
        self.maze = []
        self.difficulty = self.DIFFICULTY["TEST"]
        
        self.gameOver = False
    """
    Asking for difficulty choice
    """
    def set_level(self):
        options = ["TEST", "EASY", "NORMAL", "HARD"]
        level = ""
        # Waiting for correct input (int)
        while not (isinstance(level, int)):
            try:
                level = int(input("Choose difficulty:\n 1 - Easy | 2 - Normal | 3 - Hard\n"))
                if level < 0 or level > 3:
                    level = ""
                    raise ValueError
            except ValueError:
                print("Bad input >:( Enter the number of chosen difficulty")
        # Translating user input into difficulty preset
        userChoice = options[int(level)]
        self.difficulty = self.DIFFICULTY[userChoice]
        
        # Getting a (random) maze preset
        preset = f"maze_{self.difficulty[0]}.{random.randint(1, 3)}.0"
        self.startMazePreset = preset
        self.activeMazePreset = preset
        self.maze = self.mazeGenerator.get_preset(self.startMazePreset)
        
        # Getting a (random) GPT prompt
        promptNumber = random.choice([0, 1])
        key = list(self.PROMPT_LIBRARY[userChoice][promptNumber].keys())[0]
        self.PROMPT = self.PROMPT_LIBRARY[userChoice][promptNumber][key]
            
        print(f"Selected difficulty: {userChoice}")
        print(f"Getting maze preset: {self.startMazePreset}")
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
    
    def maze_rotation(self, player, maze):
        self.rotationCounter = (self.rotationCounter + 1) % 4
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
    def apply_debuffs(self, player, maze, case):
        DEBUFF = {
            1: ["ROTATION", self.maze_rotation],
            2: ["BLINDNESS", self.blind],
            3: ["RANDOM MOVE", self.random_move],
            4: ["TELEPORT", self.teleport],
            5: ["INVISIBILITY", self.set_invisible]
            }
        
        for i in range(self.difficulty[1]):
            choice = random.randint(case, case + 2)
            DEBUFF[choice][1](player, maze)
            
            print(f"{DEBUFF[choice][0]} were applied")
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
    Access function for use in game loop (Main.py)
    """
    def get_game_stats(self):
        return [self.difficulty, self.maze, [self.debuffDuration, self.renderDistance]]
    """
    Returns session's status (finish arrived)
    """
    def is_game_over(self):
        return self.gameOver
    """
    Switches maze preset's section according to preset connection setting (graph)
    """
    def switch_section(self, player):
        graph = self.mazeGenerator.get_preset_connections(self.activeMazePreset)
        
        # Last int of a preset
        startSection = self.activeMazePreset[-1]
        # Stock player position (in non-rotated maze)
        playerPosition = player.get_rotated_position((4 - self.rotationCounter) % 4);
        
        # bridge = [target_section, start_point (active section), end_point]
        for bridge in graph[startSection]:
            if bridge[1] == playerPosition:
                self.activeMazePreset = f"{self.activeMazePreset[:-1]}{bridge[0]}"
                self.maze = self.mazeGenerator.get_preset(self.activeMazePreset)
                
                player.set_position(bridge[2])

        for i in range(self.rotationCounter):
            self.maze_rotation(player, self.maze)
    """
    Finishes the session depending on end event
    """
    def end_game(self, player, case = "FINISH"):
        if case == "DEATH":
            pass
        if case == "FINISH":
            player.hide(True)
            
            preset = f"FINISH.0.{random.randint(0, 1)}"
            self.maze = self.mazeGenerator.get_preset(preset)
            self.gameOver = True
    """
    Returns selected prompt
    """
    def get_prompt(self):
        return self.PROMPT