from pathlib import Path
import json, math, random

class MazeGenerator():

    def __init__(self):
        self.PRESET_LIBRARY = []
        # Loading maze presets' library
        file_maze_preset = Path(__file__).parent / "maze_presets.json"
        file_maze_preset.resolve()
        with open(file_maze_preset) as preset_file:
            data = json.load(preset_file)
            self.PRESET_LIBRARY = data
    """
    Returns a maze preset according to given (str) key
    """
    def get_preset(self, preset_id: str = "maze_0.1.0"):
        section = preset_id[-1]
        preset = preset_id[:-2]

        return self.PRESET_LIBRARY[preset][section]
    """
    Returns a dictionary {"start section": [connections]}
    of a given preset
    """
    def get_preset_connections(self, preset_id: str = "maze_0.1.0"):
        preset = preset_id[:-2]
        
        graph = self.PRESET_LIBRARY[preset]["connections"]

        return graph
    """
    Rotates maze by 90° counterclockwise
    """
    def rotate_maze(self, maze):
        # Generating an empty maze
        rotatedMaze = [[[0 for _ in range(16)] for _ in range(16)], [0, 0], [0, 0]]

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
            # (reversed)End of searching
            searching = distance < 7 or maze[0][point[1]][point[0]] == 1
            
        return point
    """
    Returns the floor distance between two 2D points as int
    """
    def __get_distance(self, a, b):
        x = b[0] - a[0]
        y = b[1] - a[1]

        distance = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        return math.floor(distance)