import random
import os
import pygame
from game.block import Block, Debris


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_height = 28
        self.base_width = 180

        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 28)
        self.font_big = pygame.font.SysFont(None, 46)
        self.font_perfect = pygame.font.SysFont(None, 42)

        self.high_score_file = "highscore.txt"
        self.high_score = self.load_high_score()

        self.reset()

    def load_high_score(self):
        if not os.path.exists(self.high_score_file):
            return 0

        try:
            with open(self.high_score_file, "r") as file:
                return int(file.read().strip())
        except (ValueError, OSError):
            return 0

    def save_high_score(self):
        try:
            with open(self.high_score_file, "w") as file:
                file.write(str(self.high_score))
        except OSError:
            pass

    def get_color(self, index):
        palette = [
            (230, 75, 75),
            (240, 140, 45),
            (245, 210, 50),
            (60, 195, 110),
            (50, 150, 240),
            (165, 80, 225),
        ]

        return palette[index % len(palette)]

    def reset(self):
        self.score = 0
        self.blocks_placed = 0
        self.game_over = False

        self.perfect_streak = 0
        self.perfect_message_timer = 0

        self.debris = []

        base_x = (self.width - self.base_width) // 2
        base_y = self.height - 60

        base_block = Block(
            base_x,
            base_y,
            self.base_width,
            self.block_height,
            self.get_color(0),
            speed=0
        )

        self.stack = [base_block]

        self.spawn_active_block()

    def spawn_active_block(self):
        top_block = self.stack[-1]

        next_y = top_block.y - self.block_height - 4

        speed = min(
            10.0,
            4.5 + (len(self.stack) * 0.35)
        )

        color = self.get_color(len(self.stack))

        start_x = (
            25
            if random.choice([True, False])
            else self.width - 25 - top_block.width
        )

        self.active_block = Block(
            start_x,
            next_y,
            top_block.width,
            self.block_height,
            color,
            speed=speed
        )

    def add_debris(self, act, top_block):
        if act.x < top_block.x:
            width = top_block.x - act.x

            if width > 1:
                self.debris.append(
                    Debris(
                        act.x + width / 2,
                        act.y + self.block_height / 2,
                        width,
                        self.block_height,
                        act.color,
                        -2.5
                    )
                )

        if act.x + act.width > top_block.x + top_block.width:
            width = (
                act.x
                + act.width
                - top_block.x
                - top_block.width
            )

            if width > 1:
                self.debris.append(
                    Debris(
                        top_block.x
                        + top_block.width
                        + width / 2,
                        act.y + self.block_height / 2,
                        width,
                        self.block_height,
                        act.color,
                        2.5
                    )
                )

    def drop_block(self):
        if self.game_over:
            return

        top_block = self.stack[-1]
        act = self.active_block

        left = max(act.x, top_block.x)

        right = min(
            act.x + act.width,
            top_block.x + top_block.width
        )

        overlap = right - left

        is_successful_drop = overlap > 0

        if not is_successful_drop:
            self.perfect_streak = 0
            self.game_over = True

            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

            return

        # A block was successfully placed.
        self.blocks_placed += 1

        is_perfect = abs(act.x - top_block.x) <= 3

        if is_perfect:
            self.perfect_streak += 1
            self.perfect_message_timer = 45

            new_x = top_block.x
            new_width = top_block.width

            self.score += 2

        else:
            self.perfect_streak = 0

            self.add_debris(act, top_block)

            new_x = left
            new_width = max(10.0, overlap)

            self.score += 1

        if self.perfect_streak >= 3:
            new_x = top_block.x
            new_width = top_block.width
            self.perfect_streak = 0

        new_block = Block(
            new_x,
            act.y,
            new_width,
            self.block_height,
            act.color,
            speed=0
        )

        self.stack.append(new_block)

        if new_block.y < 180:
            shift_amount = self.block_height + 4

            for b in self.stack:
                b.y += shift_amount

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        self.spawn_active_block()

    def handle_event(self, event):
        if self.game_over:
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ) or (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                self.reset()

            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.drop_block()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.drop_block()

    def update(self):
        if not self.game_over:
            self.active_block.update(self.width)

        if self.perfect_message_timer > 0:
            self.perfect_message_timer -= 1

        for debris in self.debris:
            debris.update()

        self.debris = [
            debris
            for debris in self.debris
            if debris.y < self.height + 100
        ]

    def render(self, screen):
        screen.fill((24, 27, 36))

        title_surf = self.font_title.render(
            "Skyscraper Stack",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                16
            )
        )

        score_surf = self.font_hud.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (
                20,
                20
            )
        )

        blocks_surf = self.font_hud.render(
            f"Blocks: {self.blocks_placed}",
            True,
            (100, 220, 255)
        )

        screen.blit(
            blocks_surf,
            (
                20,
                52
            )
        )

        best_surf = self.font_hud.render(
            f"Best: {self.high_score}",
            True,
            (120, 255, 150)
        )

        screen.blit(
            best_surf,
            (
                self.width - best_surf.get_width() - 20,
                20
            )
        )

        for b in self.stack:
            b.render(screen)

        for debris in self.debris:
            debris.render(screen)

        if not self.game_over:
            self.active_block.render(screen)

        if self.perfect_message_timer > 0:
            perfect_surf = self.font_perfect.render(
                "PERFECT!",
                True,
                (255, 220, 80)
            )

            screen.blit(
                perfect_surf,
                (
                    self.width // 2 - perfect_surf.get_width() // 2,
                    100
                )
            )

        if self.game_over:
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 195))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render(
                "TOWER COLLAPSED!",
                True,
                (240, 75, 75)
            )

            screen.blit(
                over_surf,
                (
                    self.width // 2 - over_surf.get_width() // 2,
                    self.height // 2 - 70
                )
            )

            final_surf = self.font_hud.render(
                f"Final Score: {self.score}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                final_surf,
                (
                    self.width // 2 - final_surf.get_width() // 2,
                    self.height // 2 - 25
                )
            )

            blocks_final_surf = self.font_hud.render(
                f"Blocks Placed: {self.blocks_placed}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                blocks_final_surf,
                (
                    self.width // 2
                    - blocks_final_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )

            best_final_surf = self.font_hud.render(
                f"Best Score: {self.high_score}",
                True,
                (120, 255, 150)
            )

            screen.blit(
                best_final_surf,
                (
                    self.width // 2
                    - best_final_surf.get_width() // 2,
                    self.height // 2 + 45
                )
            )

            restart_surf = self.font_hud.render(
                "Press [Space] or [R] to Play Again",
                True,
                (200, 200, 200)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    self.height // 2 + 85
                )
            )