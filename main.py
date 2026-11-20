import pygame
import random

pygame.init()
pygame.display.set_caption("DODGE OR DIE")
WIDTH = 960
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH , HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
ship = pygame.image.load("assets/ship.png").convert_alpha()
ship = pygame.transform.scale(ship, (50, 38))

rock = pygame.image.load("assets/rock.png").convert_alpha()
rock = pygame.transform.scale(rock, (40, 40))
shoot = pygame.mixer.Sound("assets/shoot.ogg")
laser = pygame.image.load("assets/laser.png").convert_alpha()
laser = pygame.transform.scale(laser, (10, 30))

player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 38)
blocks = []
score = 0
bullets = []
cooldown = 0

running = True
while running:
  clock.tick(60)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    player.x -= 6
  if keys[pygame.K_RIGHT]:
    player.x += 6
  player.x = max(0, min(WIDTH - 50, player.x))
  
  cooldown -= 1
  if keys[pygame.K_SPACE] and cooldown <= 0:
    bullets.append(pygame.Rect(player.centerx - 5, player.y, 10, 30))
    shoot.play()
    cooldown = 15
  
  if random.random() < 0.05:
    blocks.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 40))
  for b in blocks:
    b.y += 5
    if b.colliderect(player):
      running = False

  for bl in bullets:
    bl.y -= 10
    for b in blocks:
      if bl.colliderect(b):
        blocks.remove(b)
        bl.y = -100
        score += 120
        break

  blocks = [b for b in blocks if b.y < HEIGHT]
  bullets = [bl for bl in bullets if bl.y > -20]
  score += 1

  screen.fill((20, 20, 30))
  screen.blit(ship, player)
  for b in blocks:
    screen.blit(rock, b)
  for bl in bullets:
    screen.blit(laser, bl)
  text = font.render(str(score // 60), True, (255, 255, 255))
  screen.blit(text, (10, 10))
  pygame.display.flip()

print("Score:", score // 60)

