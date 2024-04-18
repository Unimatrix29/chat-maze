import pygame
import random
import MazeGenerator

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_SIZE = (16, 16)
GRID_SIZE = 16
CELL_SIZE = 30
PIXEL_SIZE = 24



# Pygame init
pygame.init()
screen = pygame.display.set_mode([480, 480])
pygame.display.set_caption("Chat_Leap")

# Labyrinth generieren
maze = MazeGenerator.get_preset("maze_1")

screen_running = True
while screen_running:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen_running = False

    screen.fill(BLACK)

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    pygame.display.flip()

# Pygame beenden
pygame.quit()
