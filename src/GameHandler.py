from MazeGenerator import MazeGenerator 
import random
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
        self.debuffDuration = 0
        self.renderDistance = 16
        
        self.mazeGenerator = MazeGenerator()
        self.preset = "maze_0"
        self.maze = []
        self.difficulty = self.DIFFICULTY["TEST"]
        
        self.gameOver = False
    """
    Asking for difficulty choice
    """
    def set_level(self):
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
                
        self.difficulty = self.DIFFICULTY[options[int(level)]]

        # preset = f"maze_{self.difficulty[0]}.{random.randint(1, 5)}.0"
        self.preset = f"maze_{self.difficulty[0]}.1.0"
        self.maze = self.mazeGenerator.get_preset(self.preset)
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
    
    def maze_rotation(self, player, maze):
        self.maze = self.mazeGenerator.rotate_maze(maze)
        newPosition = [player.currentPosition[1], 15 - player.currentPosition[0]]
        player.set_position(newPosition)
    
    def blind(self, player = 0, maze = 0):
        self.renderDistance = 4
        self.debuffDuration = self.difficulty[2]
    
    def random_move(self, player, maze):
        #mVector = controller.random_input()
        mVector = [0,0]
        player.move(mVector)
        while self.check_wall(player.currentPosition):
            player.move([-mVector[0], -mVector[1]])
            #mVector = controller.random_input()
            mVector = [0,0]
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
    Finishes the session depending on end event
    """
    def end_game(self, case = "FINISH"):
        if case == "DEATH":
            pass
        if case == "FINISH":
            self.maze = self.mazeGenerator.get_preset("FINISH")
            self.gameOver = True
    """
    Returns session's status (finish arrived)
    """
    def is_game_over(self):
        return self.gameOver