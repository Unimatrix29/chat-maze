from pathlib import Path
import json, math, random

class MazeGenerator():
    """
    MazeGenerator provides an access to maze preset library along with
    rotation and searching points of mazes.
    
    Methods
    -----------
        get_preset (preset_id : str = "maze_0.1.0") -> list[list[int]]
            Returns a maze preset with the given id.
        get_preset_connections (preset_id : str = "maze_0.1.0") -> dict[str, list[int]]
            Returns all connections of the given maze preset.
        rotate_maze (maze : list[list[int]]) -> list[list[int]]
            Rotates the given maze 1x90° counterclockwise.
        get_random_point (maze : list[list[int]]) -> list[int]
            Searches and returns a random point of the given maze
            that isn't too close to the finish point.
    """
    def __init__(self):
        self._PRESET_LIBRARY = []
        # Loading maze presets' library
        _file_maze_preset = Path(__file__).parent / "assets" / "maze_presets.json"
        _file_maze_preset.resolve()
        with open(_file_maze_preset) as preset_file:
            data = json.load(preset_file)
            self._PRESET_LIBRARY = data
            
    def get_preset(self, preset_id: str = "maze_0.1.0") -> list[list[int]]:
        """
        Returns a maze preset according to given id.

        Parameters:
            preset_id : str = "maze_0.1.0"
                An id of wished preset.

        Raises:
            KeyError if the given id isn't in the preset library.
                
        Returns:
            maze_preset : list[list[int]]
                The requested maze preset.
        """
        section = preset_id[-1]
        preset = preset_id[:-2]

        return self._PRESET_LIBRARY[preset][section]
    
    def get_preset_connections(self, preset_id: str = "maze_0.1.0") -> dict[str, list[list[int]]]:
        """
        Returns all connections of the given maze preset
        
        Parameters:
            preset_id : str = "maze_0.1.0"
                An id of preset to get connections for.
            
        Returns:
            graph : dict[str, list[list[int]]]]
                A connection graph of the requested preset. The key is the start
                section, the value is a list of available bridges from the key.
        """
        preset = preset_id[:-2]
        
        graph = self._PRESET_LIBRARY[preset]["connections"]

        return graph
    
    def rotate_maze(self, maze: list[list[int]]) -> list[list[int]]:
        """
        Rotates maze by 1x90° counterclockwise.
        
        Parameters:
            maze : list[list[int]]
                A maze to rotate.
                
        Returns:
            rotatedMaze : list[list[int]]
                A new maze created by rotation every point including start and
                finish of the given maze.
        """
        # Generating an empty maze
        rotatedMaze = [[[0 for _ in range(16)] for _ in range(16)], [0, 0], [0, 0]]

        for i in range(0, 16):
            for j in range(0, 16):
                rotatedMaze[0][j][i] = maze[0][i][15 - j]
                
        rotatedMaze[1] = [maze[1][1], 15 - maze[1][0]]
        rotatedMaze[2] = [maze[2][1], 15 - maze[2][0]]
        
        return rotatedMaze
    
    def get_random_point(self, maze: list[list[int]]) -> list[int]:
        """
        Returns a random point of the maze that isn't too close to finish.
        
        Parameters:
            maze : list[list[int]]
                A maze to search a point in.

        Returns:
            point : list[int]
                A random point of the given maze with distance to the finish
                not less than 7.
        """
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
    
    def __get_distance(self, a: list[int], b: list[int]) -> int:
        """
        Returns the floor distance between two 2D points as int.
        
        Parameters:
            a : list[int]
                The start point of the line.
            b : list[int]
                The end point of the line.
        
        Returns:
            distance : int
                The floor distance between the given two points.
        """
        x = b[0] - a[0]
        y = b[1] - a[1]

        distance = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        return math.floor(distance)