"""
Space Blaster 2.1 — arcade shooter with explosions, stars & (optional) sound

Controls:
  ← / →      Move ship
  SPACE      Fire
  ESC        Quit
"""

import pygame, random, sys, os
pygame.init()

# --- Settings ---
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Blaster 2.1")
clock = pygame.time.Clock()

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 60, 60)
GREEN = (0, 255, 0)
BLUE  = (60, 180, 255)
YELLOW= (255, 255, 100)

# --- Initialize sound mixer ---
pygame.mixer.init()

def load_sound(path):
    """Safe sound loader (returns None if missing)."""
    if os.path.exists(path):
        try:
            return pygame.mixer.Sound(path)
        except Exception as e:
            print(f"Warning: couldn't load sound {path}: {e}")
    return None

# Optional sound files (put small .wav files in same folder)
shoot_sound = load_sound("laser.wav")
explosion_sound = load_sound("explosion.wav")

# --- Sprite classes ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 60))
        self.speed = 7

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH-20),
                                                random.randint(-100, -40)))
        self.speedy = random.randint(3, 6)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(20, WIDTH-20)
            self.speedy = random.randint(3, 6)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.frames = []
        for size in range(10, 60, 10):
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, YELLOW, (size//2, size//2), size//2)
            self.frames.append(surf)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=center)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # ms

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.frames[self.index]
                self.rect = self.image.get_rect(center=center)

# --- Stars background ---
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(80)]
def draw_stars():
    for s in stars:
        pygame.draw.circle(screen, WHITE, s, 1)
        s[1] += 2
        if s[1] > HEIGHT:
            s[0], s[1] = random.randint(0, WIDTH), 0

# --- Sprite groups ---
player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

for _ in range(8):
    e = Enemy()
    enemies.add(e)
    all_sprites.add(e)

score = 0
font = pygame.font.SysFont("arial", 28)

# --- Game loop ---
running = True
while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(bullet)
            all_sprites.add(bullet)
            if shoot_sound:
                shoot_sound.play()

    # Update
    player.update(keys)
    enemies.update()
    bullets.update()
    explosions.update()

    # Collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        if explosion_sound:
            explosion_sound.play()
        exp = Explosion(hit.rect.center)
        explosions.add(exp)
        all_sprites.add(exp)
        e = Enemy()
        enemies.add(e)
        all_sprites.add(e)

    if pygame.sprite.spritecollideany(player, enemies):
        if explosion_sound:
            explosion_sound.play()
        exp = Explosion(player.rect.center)
        explosions.add(exp)
        all_sprites.add(exp)
        running = False

    # --- Draw ---
    screen.fill(BLACK)
    draw_stars()
    all_sprites.draw(screen)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

# --- Game Over ---
screen.fill(BLACK)
game_over = font.render("GAME OVER", True, RED)
score_txt = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over, (WIDTH//2 - 80, HEIGHT//2 - 40))
screen.blit(score_txt, (WIDTH//2 - 100, HEIGHT//2 + 10))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()

