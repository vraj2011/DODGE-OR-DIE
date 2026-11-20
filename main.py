import pygame
import random

pygame.init()
pygame.display.set_caption("DODGE OR DIE")
screen = pygame.display.set_mode((480, 640))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
ship = pygame.image.load("assets/ship.png").convert_alpha()
ship = pygame.transform.scale(ship, (50, 38))

rock = pygame.image.load("assets/rock.png").convert_alpha()
rock = pygame.transform.scale(rock, (40, 40))

player = pygame.Rect(215, 580, 50, 38)
blocks = []
score = 0

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
  player.x = max(0, min(430, player.x))

  if random.random() < 0.03:
    blocks.append(pygame.Rect(random.randint(0, 440), -40, 40, 40))

  for b in blocks:
    b.y += 5
    if b.colliderect(player):
      running = False

  blocks = [b for b in blocks if b.y < 640]
  score += 1

  screen.fill((20, 20, 30))
  screen.blit(ship, player)
  for b in blocks:
    screen.blit(rock, b)
  text = font.render(str(score // 60), True, (255, 255, 255))
  screen.blit(text, (10, 10))
  pygame.display.flip()

print("Score:", score // 60)

