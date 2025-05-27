import pygame
import random
from game.tile import Tile
from config import TILE_SPEED, KEY_MAPPING, TILE_WIDTH, TILE_HEIGHT, SCREEN_WIDTH
import os

class GameManager:
    def __init__(self, max_health):
        self.tiles = []
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_delay = 40
        self.health = max_health
        self.max_health = max_health

    def spawn_tile(self):
        column = random.randint(0, 8)
        key = KEY_MAPPING[column]
        self.tiles.append(Tile(column, key))

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.restart()
            return

        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            for tile in self.tiles:
                if tile.key == key_name and tile.is_hittable():
                    tile.active = False
                    self.score += 1
                    break

    def update(self):
        if self.game_over:
            return

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_tile()
            self.spawn_timer = 0

        for tile in self.tiles:
            tile.update(TILE_SPEED)

        # Check for missed tiles
        for tile in self.tiles:
            if tile.y > 560:
                self.health -= 1
                tile.active = False
                if self.health <= 0:
                    self.end_game()

        self.tiles = [t for t in self.tiles if t.active]

    def draw(self, screen):
        font = pygame.font.SysFont(None, 40)
        if self.game_over:
            text = font.render("Game Over! Score: {} | Press R to Restart".format(self.score), True, (255, 0, 0))
            screen.blit(text, (50, 250))
        else:
            for tile in self.tiles:
                tile.draw(screen)

            score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

            # Draw health bar
            health_bar_x = 10
            health_bar_y = 50
            health_bar_width = 200
            health_bar_height = 20
            fill = (self.health / self.max_health) * health_bar_width

            pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, fill, health_bar_height))

            health_text = font.render(f"Health: {self.health}/{self.max_health}", True, (0, 0, 0))
            screen.blit(health_text, (health_bar_x + 210, health_bar_y - 5))

    def end_game(self):
        self.game_over = True
        self.save_score()

    def restart(self):
        self.tiles.clear()
        self.score = 0
        self.health = self.max_health
        self.game_over = False
        self.spawn_timer = 0

    def save_score(self):
        os.makedirs("data", exist_ok=True)
        with open("data/scores.txt", "a") as f:
            f.write(str(self.score) + "\n")
