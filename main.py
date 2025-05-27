import pygame
import sys
import random
from game.game_manager import GameManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Magic Tile Brain Game")

clock = pygame.time.Clock()
game = GameManager()

# Main loop
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
