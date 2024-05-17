import random
import math

class MazeGenerator():

    def __init__(self):
        self.PRESET_LIBRARY = {
            "maze_0":
            [[
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ], [0,0], [15, 15]
            ],
            "maze_1.1.0": 
            [[
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,0,0,1,0,1,1,1,1,1,1],
            [1,0,0,0,0,1,0,0,0,0,0,1,1,1,0,1],
            [1,0,0,0,0,1,0,0,1,1,0,1,0,0,0,1],
            [1,0,1,1,1,1,0,0,1,1,0,1,0,1,0,1],
            [1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1],
            [1,1,1,1,0,1,0,0,1,0,0,1,0,1,0,1],
            [1,1,1,1,0,1,0,0,1,1,0,1,0,1,0,1],
            [1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
            [1,1,1,0,1,0,0,1,1,1,1,1,0,1,0,1],
            [1,0,1,0,1,0,1,1,0,0,0,1,0,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,1,0,1,1,1],
            [1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ], [2, 1], [9, 13]
            ],
            "maze_1.2.0": 
            [[
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ], [0,0], [15, 15]
            ],
            "maze_1.3.0": 
            [[
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ], [0,0], [15, 15]
            ],
            "maze_2.1.0": 
            [[
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0],
            [0,0,0,0,0,0,1,1,1,1,0,0,1,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ], [0,0], [15, 15]
            ],
            "LOST": 
            [[
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
            [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
            [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ], [0,0], [15, 15]
            ],
            "FINISH":
            [[
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0],
            [0,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0],
            [0,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ], [0,0], [15, 15]
            ],

        }

    def random_maze(self):
        maze = [[random.choice([0, 1]) for _ in range(16)] for _ in range(16)]
        return maze

    def get_preset(self, preset_id = "maze_0"):
        if preset_id in self.PRESET_LIBRARY:
            return self.PRESET_LIBRARY[preset_id]
        return self.PRESET_LIBRARY["maze_0"]
    """
    Rotates maze by 90° counter clockwise
    """
    def rotate_maze(self, maze):
        rotatedMaze = self.get_preset("maze_0")

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