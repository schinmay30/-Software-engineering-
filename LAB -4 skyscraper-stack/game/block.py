import pygame


class Block:
    def __init__(self, x, y, width, height, color, speed=0):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.color = color
        self.speed = speed
        self.direction = 1

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            int(self.width),
            int(self.height)
        )

    def update(self, screen_width):
        if self.speed == 0:
            return

        self.x += self.speed * self.direction

        if self.x <= 20:
            self.x = 20
            self.direction = 1

        elif self.x + self.width >= screen_width - 20:
            self.x = screen_width - 20 - self.width
            self.direction = -1

    def render(self, surface):
        draw_rect = self.rect

        pygame.draw.rect(
            surface,
            self.color,
            draw_rect,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            (245, 245, 250),
            draw_rect,
            width=2,
            border_radius=4
        )


class Debris:
    def __init__(self, x, y, width, height, color, velocity_x):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.color = color

        self.velocity_x = float(velocity_x)
        self.velocity_y = -2.0

        self.gravity = 0.25
        self.rotation = 0
        self.rotation_speed = 6

    def update(self):
        self.velocity_y += self.gravity

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.rotation += self.rotation_speed

    def render(self, surface):
        debris_surface = pygame.Surface(
            (int(self.width), int(self.height)),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            debris_surface,
            self.color,
            (0, 0, int(self.width), int(self.height)),
            border_radius=4
        )

        pygame.draw.rect(
            debris_surface,
            (245, 245, 250),
            (0, 0, int(self.width), int(self.height)),
            width=2,
            border_radius=4
        )

        rotated_surface = pygame.transform.rotate(
            debris_surface,
            self.rotation
        )

        surface.blit(
            rotated_surface,
            (
                int(self.x - rotated_surface.get_width() / 2),
                int(self.y - rotated_surface.get_height() / 2)
            )
        )