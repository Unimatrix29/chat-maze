import pygame
import random

# Farben definieren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bildschirmgröße und Gittergröße
SCREEN_SIZE = (510, 510)
GRID_SIZE = 16
CELL_SIZE = 30

# generate random maze
def generate_maze():
    maze = [[random.choice([0, 1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return maze

# Pygame init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Chat_Leap")

# Labyrinth generieren
maze = generate_maze()

screen_running = True
while screen_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen_running = False

    # Hintergrund zeichnen
    screen.fill(WHITE)

    # Labyrinth zeichnen
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    pygame.display.flip()

# Pygame beenden
pygame.quit()
