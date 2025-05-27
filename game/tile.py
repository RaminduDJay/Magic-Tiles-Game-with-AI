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
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_ACTIVE, (self.x, self.y, TILE_WIDTH, TILE_HEIGHT), border_radius=8)
        pygame.draw.rect(screen, COLOR_BORDER, (self.x, self.y, TILE_WIDTH, TILE_HEIGHT), 2, border_radius=8)

        font = pygame.font.SysFont("Arial", 24, bold=True)
        text = font.render(self.key.upper(), True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x + TILE_WIDTH // 2, self.y + TILE_HEIGHT // 2))
        screen.blit(text, text_rect)

    def is_hittable(self):
        return 500 < self.y < 560  # Hit zone
