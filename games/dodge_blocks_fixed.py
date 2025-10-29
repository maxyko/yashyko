"""
Tiny graphical game: Dodge the Blocks (fully fixed)
Requirements: Python 3.8+ and pygame
Install pygame: pip install pygame

Controls:
- Left / Right arrows (or A / D) to move the player
- Press R to restart after game over
- Press Esc or close window to quit
"""

import random
import sys
import pygame

# ---- Config ----
WIDTH, HEIGHT = 480, 640
FPS = 60
PLAYER_SIZE = 50
BLOCK_MIN_SIZE = 20
BLOCK_MAX_SIZE = 80
BLOCK_SPAWN_TIME = 700  # milliseconds
SPEED_INCREASE_EVERY = 5000  # ms
INITIAL_BLOCK_SPEED = 3
BACKGROUND_COLOR = (20, 24, 30)
PLAYER_COLOR = (50, 200, 150)
BLOCK_COLOR = (200, 80, 80)
TEXT_COLOR = (240, 240, 240)


# ---- Game code ----
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.image, PLAYER_COLOR, (0, 0, PLAYER_SIZE, PLAYER_SIZE), border_radius=8)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.speed = 6

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        # keep inside screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Block(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        size = random.randint(BLOCK_MIN_SIZE, BLOCK_MAX_SIZE)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLOCK_COLOR, (0, 0, size, size), border_radius=6)
        self.rect = self.image.get_rect(midtop=(random.randint(0, WIDTH - size), -size))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


def draw_text(surface, text, size, pos, center=True):
    font = pygame.font.SysFont(None, size)
    surf = font.render(text, True, TEXT_COLOR)
    rect = surf.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(surf, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodge the Blocks")
    clock = pygame.time.Clock()

    player = Player()

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    all_sprites.add(player)

    score = 0
    running = True
    game_over = False

    block_event = pygame.USEREVENT + 1
    pygame.time.set_timer(block_event, BLOCK_SPAWN_TIME)

    speed_increase_event = pygame.USEREVENT + 2
    pygame.time.set_timer(speed_increase_event, SPEED_INCREASE_EVERY)

    block_speed = INITIAL_BLOCK_SPEED
    last_time = pygame.time.get_ticks()

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == block_event and not game_over:
                block = Block(block_speed)
                blocks.add(block)
                all_sprites.add(block)
            if event.type == speed_increase_event and not game_over:
                block_speed += 0.5
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    # restart
                    for s in all_sprites:
                        s.kill()
                    player = Player()
                    all_sprites.add(player)
                    blocks.empty()
                    score = 0
                    block_speed = INITIAL_BLOCK_SPEED
                    game_over = False

        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys)
            blocks.update()

            # collision
            if pygame.sprite.spritecollideany(player, blocks):
                game_over = True

            # update score by time survived
            now = pygame.time.get_ticks()
            if now - last_time >= 100:
                score += 1
                last_time = now

        # draw
        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)

        # HUD
        draw_text(screen, f"Score: {score}", 28, (10, 10), center=False)

        if game_over:
            draw_text(screen, "GAME OVER", 64, (WIDTH // 2, HEIGHT // 2 - 30))
            draw_text(screen, f"Final score: {score}", 36, (WIDTH // 2, HEIGHT // 2 + 20))
            draw_text(screen, "Press R to restart or Esc to quit", 24, (WIDTH // 2, HEIGHT // 2 + 70))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
