from enum import Enum

class Color(Enum):
    BACKGROUND = (0, 0, 0)          # Black
    
    MAZE_BORDER = (255, 0, 0)       # Red
    MAZE_CELL = (255, 255, 0)       # Yellow
    
    CHAT_BORDER = (0,191,255)       # deepskyblue
    TEXT = (0, 255, 0)              # limegreen