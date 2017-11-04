# Zombie Shooter
import pygame

import random
from os import path

img_dir = path. join(path.dirname(__file__), 'img')
snd_dir = path. join(path.dirname(__file__), 'snd')

WIDTH = 800
HEIGHT = 457
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255,0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")
clock = pygame.time.Clock()
 
font_name =  pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

def newmob():
	m = Mob()
	all_sprites.add(m)
	mobs.add(m) 

def draw_shield_bar(surf, x, y, pct):
	if pct < 0:
		pct = 0
	BAR_LENGTH = 200
	BAR_HEIGHT = 20
	fill = (pct / 100 * BAR_LENGTH)
	outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surf, GREEN, fill_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2) 

# Creating a Zombie
class Zombie(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(zombie_img, (50, 60))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect() 
		self.radius = 20
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.speedy = 0
		self.shield = 100
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()

 

	def update(self):
		# RIGHT LEFT control
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -10
		if keystate[pygame.K_RIGHT]:
			self.speedx = 10
		if keystate[pygame.K_SPACE]:
			self.shoot()
		self.rect.x += self.speedx
		# UP DOWN control
		self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_UP]:
			self.speedy = -10
		if keystate[pygame.K_DOWN]:
			self.speedy = 10
		self.rect.y += self.speedy
		# Walls
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
		if self.rect.top < 0:
			self.rect.top = 0

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			bullets.add(bullet)

# Creating the Enemy
class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(enemy_images)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width * .85 / 2)
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -10)
		self.speedy = random.randrange(2, 20)
		self.speedx = random.randrange(-3, 3)
		self.rot = 0
		self.rot_speed = random.randrange(-30, 30)
		self.last_update = pygame.time.get_ticks()

	
	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rot = (self.rot + self.rot_speed) % 360
			new_image = pygame.transform.rotate(self.image_orig, self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 5)

# Creating bullets
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = bonebullet_img 
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 7
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.bottom = y
		self.rect.centerx = x 
		self.speedy = -5
  

	def update(self):
		self.rect.y += self.speedy
		# kill if it moves off the top of the screen
		if self.rect.bottom < 0:
			self.kill()

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "BG.png")).convert()
background_rect = background.get_rect()
zombie_img = pygame.image.load(path.join(img_dir, "Attack (8).png")).convert()
tombstone_img = pygame.image.load(path.join(img_dir, "TombStone (2).png")).convert()
bonebullet_img = pygame.image.load(path.join(img_dir, "Bone (2).png")).convert()
enemy_images = []
enemy_list = ['TombStone (1).png', 'TombStone (2).png', 'TombStone (3).png', 
			  'TombStone (4).png', 'Crate.png', 'Tree.png']
for img in enemy_list:
	enemy_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'hit2.wav'))
hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'hit1.wav'))
#pygame.mixer.music.load(path.join(snd_dir, 'gamesnd.mp3'))
pygame.mixer.music.set_volume(1.9)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Zombie()
all_sprites.add(player)
for i in range(20):
	newmob()
score = 0

#pygame.mixer.music.play(loops=-1)
# Game loop
running = True
while running:
	# keep loop running at the right speed
	clock.tick(FPS)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False

	# Update
	all_sprites.update()
	# Check to see if a bullet hit a mob
	hits = pygame.sprite.groupcollide(bullets, mobs, False, True, pygame.sprite.collide_circle) 
	for hit in hits:
		score += 50 - hit.radius
		shoot_sound.play()
		newmob()

 	# Check to see if a mob hit the player
	hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) 
	for hit in hits: 
		hit_sound.play()
		player.shield -= hit.radius * 1.2
		newmob()
		if player.shield <= 0:
			running = False


	# Draw / render
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 26, WIDTH / 2, 10)
	draw_shield_bar(screen, 5, 5, player.shield)
	# *after* drawing everything, flip the display
	pygame.display.flip()

pygame.quit()