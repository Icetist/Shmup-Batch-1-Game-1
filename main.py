# Shmup
import pygame as pg
import random
from os import path 

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 480 # Width of canvas
HEIGHT = 600 # Height of canvas
FPS = 60 # Frames per Second

# Define Colors (RGB)
# (red, green, blue)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set Up
pg.init() # Initialize Pygame
pg.mixer.init() # Initialzie Sound Effects mixer
screen = pg.display.set_mode((WIDTH, HEIGHT)) # Pygame screen
pg.display.set_caption("Shmup") # Title
clock = pg.time.Clock()

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (70, 58))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 30
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT] or keystate[pg.K_a]:
            self.speedx = -5
        if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(mob_imgs)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            # self.image = pg.transform.rotate(self.image, self.rot_speed) <- Wrong way, do not use
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy 
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(bullet_img, (15, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Kill if it moves off the screen 
        if self.rect.bottom < 0:
            self.kill()

# Load all game graphics
background = pg.image.load(path.join(img_dir, "bg.png")).convert()
background_rect = background.get_rect()
player_img = pg.image.load(path.join(img_dir, "player.png")).convert()
# mob_img = pg.image.load(path.join(img_dir, "mob_med1.png")).convert()
bullet_img = pg.image.load(path.join(img_dir, "bullet.png")).convert()
mob_imgs = []
meteor_list = ['mob_big1.png', 'mob_big2.png', 'mob_big3.png', 'mob_big4.png',
                'mob_med1.png', 'mob_med2.png',
                'mob_small1.png', 'mob_small2.png',
                'mob_tiny1.png', 'mob_tiny2.png']
for img in meteor_list:
    mob_imgs.append(pg.image.load(path.join(img_dir, img)).convert())

all_sprites = pg.sprite.Group() # All sprites group
mobs = pg.sprite.Group() # Mob group
bullets = pg.sprite.Group() # Bullets group
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game Loop
running = True
while running:
    clock.tick(FPS) # Keep game at right speed

    # Process input (events)
    for event in pg.event.get():
        # Check for closed window
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot() 

    # Update
    all_sprites.update()

    # Check to see if a bullet hit a mob
    hits = pg.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    # Check to see if a mob hit the player
    hits = pg.sprite.spritecollide(player, mobs, False, pg.sprite.collide_circle)
    if hits:
        running = False

    # Draw / Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)

    all_sprites.draw(screen)
    # After drawing everything, flip the display
    pg.display.flip()