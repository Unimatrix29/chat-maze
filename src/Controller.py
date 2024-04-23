#Note: !This is a test implementation!
import pygame

class Controller:
    
    def __init__(self):
        pass
    
    """
    Returns a movement vector of a player
    determined by the pressed key.
    """
    def get_movement(key):
        if key == pygame.K_a:
            return [-1, 0]
        elif key == pygame.K_d:
            return [1, 0]
        elif key == pygame.K_w:
            return [0, -1]
        elif key == pygame.K_s:
            return [0, 1]
        
        return [0, 0]
