import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, NUM_TILES, TILE_WIDTH, TILE_HEIGHT, COLOR_GRAD_TOP, COLOR_GRAD_BOTTOM, KEY_MAPPING

def draw_gradient_background(screen):
    for y in range(SCREEN_HEIGHT):
        blend = y / SCREEN_HEIGHT
        r = int(COLOR_GRAD_TOP[0] * (1 - blend) + COLOR_GRAD_BOTTOM[0] * blend)
        g = int(COLOR_GRAD_TOP[1] * (1 - blend) + COLOR_GRAD_BOTTOM[1] * blend)
        b = int(COLOR_GRAD_TOP[2] * (1 - blend) + COLOR_GRAD_BOTTOM[2] * blend)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

def draw_key_guides(screen):
    font = pygame.font.SysFont("Arial", 28, bold=True)
    for i, key in enumerate(KEY_MAPPING):
        x = i * TILE_WIDTH + TILE_WIDTH // 2
        y = SCREEN_HEIGHT - 40
        label = font.render(key.upper(), True, (50, 50, 50))
        label_rect = label.get_rect(center=(x, y))
        screen.blit(label, label_rect)
