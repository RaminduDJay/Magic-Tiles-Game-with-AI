import pygame
import random
from game.tile import Tile
from config import TILE_SPEED, KEY_MAPPING, TILE_WIDTH, TILE_HEIGHT, SCREEN_WIDTH
import os
import csv
import time
from utils.ui_utils import draw_gradient_background, draw_key_guides

class GameManager:
    def __init__(self, max_health):
        self.tiles = []
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_delay = 40
        self.health = max_health
        self.max_health = max_health
        self.click_logs = []
        self.start_time = time.time()
        os.makedirs("data", exist_ok=True)

        self.interaction_file = "data/interactions.csv"
        with open(self.interaction_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Tile Speed", "Expected Key", "Pressed Key", "Correct", "Reaction Time (ms)"])

    def spawn_tile(self):
        column = random.randint(0, 8)
        key = KEY_MAPPING[column]
        tile = Tile(column, key)
        tile.spawn_time = time.time()
        self.tiles.append(tile)

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.restart()
            return

        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            event_time = time.time()
            matched = False
            for tile in self.tiles:
                if tile.key == key_name and tile.is_hittable():
                    reaction_time = round((event_time - tile.spawn_time) * 1000, 2)
                    self.score += 1
                    matched = True
                    self.log_interaction(TILE_SPEED, tile.key, key_name, True, reaction_time)
                    tile.active = False
                    break

            if not matched:
                self.log_interaction(TILE_SPEED, "None", key_name, False, 0)

    def update(self):
        if self.game_over:
            return

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_tile()
            self.spawn_timer = 0

        for tile in self.tiles:
            tile.update(TILE_SPEED)

        for tile in self.tiles:
            if tile.y > 560:
                self.health -= 1
                if hasattr(tile, 'spawn_time'):
                    reaction_time = round((time.time() - tile.spawn_time) * 1000, 2)
                else:
                    reaction_time = 0
                self.log_interaction(TILE_SPEED, tile.key, "Missed", False, reaction_time)
                tile.active = False
                if self.health <= 0:
                    self.end_game()

        self.tiles = [t for t in self.tiles if t.active]

    def draw(self, screen):
        draw_gradient_background(screen)

        font = pygame.font.SysFont("Arial", 30)
        if self.game_over:
            game_over_text = font.render(f"Game Over! Score: {self.score} | Press R to Restart", True, (200, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 300, 250))
        else:
            for tile in self.tiles:
                tile.draw(screen)

            score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

            # Health Bar
            health_bar_x = 10
            health_bar_y = 50
            health_bar_width = 200
            health_bar_height = 20
            fill = (self.health / self.max_health) * health_bar_width
            pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, fill, health_bar_height))

            health_text = font.render(f"Health: {self.health}/{self.max_health}", True, (0, 0, 0))
            screen.blit(health_text, (health_bar_x + 210, health_bar_y - 5))

            # Show key guides
            draw_key_guides(screen)

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
        with open("data/scores.txt", "a") as f:
            f.write(str(self.score) + "\n")

    def log_interaction(self, tile_speed, expected_key, pressed_key, correct, reaction_time):
        with open(self.interaction_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            timestamp = round(time.time() - self.start_time, 2)
            writer.writerow([timestamp, tile_speed, expected_key, pressed_key, correct, reaction_time])
