import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magic Tiles 9-Key Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
GRAY = (211, 211, 211)

# Tile settings
TILE_WIDTH = WIDTH // 9
TILE_HEIGHT = HEIGHT

# Keys mapping (left to right)
key_mapping = [
    pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
    pygame.K_SPACE,
    pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON
]

# Initial tile states
tile_pressed = [False] * 9

clock = pygame.time.Clock()

# Main loop
while True:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Key Down
        if event.type == pygame.KEYDOWN:
            for i, key in enumerate(key_mapping):
                if event.key == key:
                    tile_pressed[i] = True

        # Key Up
        if event.type == pygame.KEYUP:
            for i, key in enumerate(key_mapping):
                if event.key == key:
                    tile_pressed[i] = False

    # Draw tiles
    for i in range(9):
        x = i * TILE_WIDTH
        color = BLUE if tile_pressed[i] else GRAY
        pygame.draw.rect(screen, color, (x, 0, TILE_WIDTH, TILE_HEIGHT))
        pygame.draw.rect(screen, BLACK, (x, 0, TILE_WIDTH, TILE_HEIGHT), 2)

    pygame.display.flip()
    clock.tick(60)
