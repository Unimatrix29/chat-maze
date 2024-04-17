import pygame
import random

# Farben definieren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Bildschirmgröße und Gittergröße
SCREEN_SIZE = (480, 480)
GRID_SIZE =16
CELL_SIZE = 30
PIXEL_SIZE = 24

# generate random maze
def random_maze():
    maze = [[random.choice([0, 1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return maze

# Pygame init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Chat_Leap")

# Labyrinth generieren
maze = random_maze()

player_pos = [0,0]

screen_running = True
while screen_running:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if player_pos[1] > 0 and maze[player_pos[1] - 1][player_pos[0]] == 0:
                    player_pos[1] -= 1
            elif event.key == pygame.K_DOWN:
                if player_pos[1] < GRID_SIZE - 1 and maze[player_pos[1] + 1][player_pos[0]] == 0:
                    player_pos[1] += 1
            elif event.key == pygame.K_LEFT:
                if player_pos[0] > 0 and maze[player_pos[1]][player_pos[0] - 1] == 0:
                    player_pos[0] -= 1
            elif event.key == pygame.K_RIGHT:
                if player_pos[0] < GRID_SIZE - 1 and maze[player_pos[1]][player_pos[0] + 1] == 0:
                    player_pos[0] += 1
            print(player_pos)

    # Hintergrund zeichnen
    screen.fill(BLACK)

    # Labyrinth zeichnen
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    pygame.display.flip()

# Pygame beenden
pygame.quit()
