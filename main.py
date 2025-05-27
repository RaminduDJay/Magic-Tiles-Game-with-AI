import pygame
import sys
from game.game_manager import GameManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Ask player for allowed fails
allowed_fails = 0
try:
    allowed_fails = int(input("Enter the number of allowed misses (e.g., 3): "))
except:
    allowed_fails = 3  # default

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Magic Tile Brain Game")

clock = pygame.time.Clock()
game = GameManager(allowed_fails)

while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        game.handle_event(event)

    game.update()
    game.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
