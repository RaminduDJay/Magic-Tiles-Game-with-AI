import pygame
from config import TILE_WIDTH, TILE_HEIGHT, SCREEN_HEIGHT, COLOR_ACTIVE, COLOR_BORDER

class Tile:
    def __init__(self, column_index, key_name):
        self.column = column_index
        self.key = key_name
        self.x = self.column * TILE_WIDTH
        self.y = -TILE_HEIGHT
        self.active = True

    def update(self, speed):
        self.y += speed
        if self.y > SCREEN_HEIGHT:
            self.active = False  # Missed tile

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_ACTIVE, (self.x, self.y, TILE_WIDTH, TILE_HEIGHT))
        pygame.draw.rect(screen, COLOR_BORDER, (self.x, self.y, TILE_WIDTH, TILE_HEIGHT), 2)

    def is_hittable(self):
        return 500 < self.y < 560  # Hit zone
