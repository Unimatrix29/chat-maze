from enum import Enum

class Colors(Enum):
    WHITE = (255, 255, 255)        # Walls
    BLACK = (0, 0, 0)              # Canvas
    RED = (255, 0, 0)              # Finish
    LIMEGREEN = (150, 205, 50)     # System (active)
    GREY = (100 ,100, 100)         # System (inactive)  
    BLUE = (0, 0, 255)             # ChatGPT-Role colours
    CYAN = (0, 204, 153)           
    GREEN = (0, 255, 0)
    ORANGE = (204, 102, 0)
    PINK = (255, 0, 149)
    YELLOW = (255, 255, 0)