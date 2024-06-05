import json, math, random

class MazeGenerator():

    def __init__(self):
        self.PRESET_LIBRARY = []
        with open('src/maze_presets.json') as preset_file:
            data = json.load(preset_file)
            
            self.PRESET_LIBRARY = data

    def random_maze(self):
        maze = [[[random.choice([0, 1]) for _ in range(16)] for _ in range(16)], [0,0], [15, 15]]
        return maze

    def get_preset(self, preset_id: str = "maze_0.0.0"):
        section = preset_id[-1]
        preset = preset_id[:-2]

        return self.PRESET_LIBRARY[preset][section]
    
    def get_random_preset(self, difficulty: int = 1):
        randomPreset = f"maze_{difficulty}.{random.randint(0, 0)}"
        
        return self.PRESET_LIBRARY[randomPreset]["0"]
    
    def get_preset_connections(self, preset_id: str = "maze_0.0.0"):
        section = preset_id[-1]
        preset = preset_id[:-2]
        
        graph = self.PRESET_LIBRARY[preset]["connections"]

        return graph
    """
    Rotates maze by 90° counter clockwise
    """
    def rotate_maze(self, maze):
        rotatedMaze = self.random_maze()

        for i in range(0, 16):
            for j in range(0, 16):
                rotatedMaze[0][j][i] = maze[0][i][15 - j]
                
        rotatedMaze[1] = [maze[1][1], 15 - maze[1][0]]
        rotatedMaze[2] = [maze[2][1], 15 - maze[2][0]]
        
        return rotatedMaze
    """
    Returns a random point of maze
    that isn't too close to finish
    """
    def get_random_point(self, maze):
        finish = maze[2]
        searching = True
        point = [0, 0]
        
        while searching:
            point[0] = random.randrange(0, 16)
            point[1] = random.randrange(0, 16)
            
            distance = self.__get_distance(finish, point)
            searching = distance < 7 or maze[0][point[1]][point[0]] == 1    # (reverse)End of searching
            
        return point
    """
    Returns the floor distance between two 2D points as int
    """
    def __get_distance(self, a, b):
        x = b[0] - a[0]
        y = b[1] - a[1]

        distance = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        return math.floor(distance)