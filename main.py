import pygame
import random

pygame.init()
pygame.display.set_caption("DODGE OR DIE")
WIDTH = 960
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH , HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font("assets/font.ttf", 24)
big = pygame.font.Font("assets/font.ttf", 56)
ship = pygame.image.load("assets/ship.png").convert_alpha()
ship = pygame.transform.scale(ship, (50, 38))

rock = pygame.image.load("assets/rock.png").convert_alpha()
rock = pygame.transform.scale(rock, (40, 40))
shoot = pygame.mixer.Sound("assets/shoot.ogg")
lose = pygame.mixer.Sound("assets/lose.ogg")
laser = pygame.image.load("assets/laser.png").convert_alpha()
laser = pygame.transform.scale(laser, (10, 30))
enemy = pygame.image.load("assets/enemy.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (60, 50))
elaser = pygame.image.load("assets/elaser.png").convert_alpha()
elaser = pygame.transform.scale(elaser, (10, 30))
eshoot = pygame.mixer.Sound("assets/eshoot.ogg")
eshoot.set_volume(0.4)
hit = pygame.mixer.Sound("assets/hit.ogg")

heart = pygame.Surface((28, 24), pygame.SRCALPHA)
shape = [" XX XX ", "XXXXXXX", "XXXXXXX", " XXXXX ", "  XXX  ", "   X   "]
for y, row in enumerate(shape):
  for x, ch in enumerate(row):
    if ch == "X":
      pygame.draw.rect(heart, (230, 50, 70), (x * 4, y * 4, 4, 4))


player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 38)
blocks = []
score = 0
bullets = []
cooldown = 0
dead = False
enemies = []
ebullets = []
hearts = 4
hurt = 0

running = True
while running:
  clock.tick(60)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  if dead:
    screen.fill((20, 20, 30))
    t1 = big.render("GAME OVER", False, (220, 80, 80))
    t2 = font.render("Score: " + str(score // 60) + "   Press R to restart", False, (255, 255, 255))
    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 250))
    screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 340))
    pygame.display.flip()
    if pygame.key.get_pressed()[pygame.K_r]:
      blocks = []
      bullets = []
      enemies = []
      ebullets = []
      hearts = 4
      hurt = 0
      score = 0
      player.x = WIDTH // 2 - 25
      dead = False
    continue

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

  if random.random() < 0.004 and len(enemies) < 2:
    enemies.append({"rect": pygame.Rect(random.randint(0, WIDTH - 60), -50, 60, 50), "hp": 2                                                                                          , "cool": 60, "dx": 3})

  damage = 0
  for b in blocks:
    b.y += 5
    if b.colliderect(player):
      damage += 1
      b.y = HEIGHT + 100

  for bl in bullets:
    bl.y -= 10
    for b in blocks:
      if bl.colliderect(b):      
        blocks.remove(b)
        bl.y = -100
        score += 120
        break

    for e in enemies:
      if bl.colliderect(e["rect"]):
        e["hp"] -= 1
        bl.y = -100
        if e["hp"] <= 0:
          enemies.remove(e)
          score += 300
        break

  for e in enemies:
    r = e["rect"]
    if r.y < 80:
      r.y += 2
    else:
      r.x += e["dx"]
      if r.x < 0 or r.x > WIDTH - 60:
        e["dx"] = -e["dx"]
    e["cool"] -= 1
    if e["cool"] <= 0:
      ebullets.append(pygame.Rect(r.centerx - 5, r.bottom, 10, 30))
      eshoot.play()
      e["cool"] = 90

  for eb in ebullets:
    eb.y += 7
    if eb.colliderect(player):
      damage += 2
      eb.y = HEIGHT + 100

  if damage > 0 and hurt <= 0:
    hearts -= damage
    hurt = 90
    hit.play()
  hurt -= 1
  if hearts <= 0:
    dead = True
    lose.play()

  blocks = [b for b in blocks if b.y < HEIGHT]
  bullets = [bl for bl in bullets if bl.y > -20]
  ebullets = [eb for eb in ebullets if eb.y < HEIGHT]
  score += 1

  screen.fill((20, 20, 30))
  if hurt <= 0 or hurt // 6 % 2 == 0:
    screen.blit(ship, player)
  for b in blocks:
    screen.blit(rock, b)
  for bl in bullets:
    screen.blit(laser, bl)
  text = font.render(str(score // 60), False, (255, 255, 255))
  for e in enemies:
    screen.blit(enemy, e["rect"])
  for eb in ebullets:
    screen.blit(elaser, eb)
  for i in range(hearts):
    screen.blit(heart, (WIDTH - 40 - i * 36, 10))

  screen.blit(text, (10, 10))
  pygame.display.flip()

print("Score:", score // 60)
 
