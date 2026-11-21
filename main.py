import pygame
import random

pygame.init()
pygame.display.set_caption("DODGE OR DIE")
WIDTH = 960
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font("assets/font.ttf", 24)
big = pygame.font.Font("assets/font.ttf", 56)

ship = pygame.image.load("assets/ship.png").convert_alpha()
ship = pygame.transform.scale(ship, (50, 38))
ship2 = pygame.image.load("assets/ship2.png").convert_alpha()
ship2 = pygame.transform.scale(ship2, (50, 38))
rock = pygame.image.load("assets/rock.png").convert_alpha()
rock = pygame.transform.scale(rock, (40, 40))
laser = pygame.image.load("assets/laser.png").convert_alpha()
laser = pygame.transform.scale(laser, (10, 30))
laser2 = pygame.image.load("assets/laser2.png").convert_alpha()
laser2 = pygame.transform.scale(laser2, (10, 30))
enemy = pygame.image.load("assets/enemy.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (60, 50))
elaser = pygame.image.load("assets/elaser.png").convert_alpha()
elaser = pygame.transform.scale(elaser, (10, 30))

shoot = pygame.mixer.Sound("assets/shoot.ogg")
lose = pygame.mixer.Sound("assets/lose.ogg")
eshoot = pygame.mixer.Sound("assets/eshoot.ogg")
eshoot.set_volume(0.4)
hit = pygame.mixer.Sound("assets/hit.ogg")

heart = pygame.Surface((28, 24), pygame.SRCALPHA)
shape = [" XX XX ", "XXXXXXX", "XXXXXXX", " XXXXX ", "  XXX  ", "   X   "]
for y, row in enumerate(shape):
  for x, ch in enumerate(row):
    if ch == "X":
      pygame.draw.rect(heart, (230, 50, 70), (x * 4, y * 4, 4, 4))


def make(x, img, lz, left, right, up, down, fire):
  return {
    "rect": pygame.Rect(x, HEIGHT - 80, 50, 38),
    "img": img,
    "laser": lz,
    "left": left,
    "right": right,
    "up": up,
    "down": down,
    "fire": fire,
    "hearts": 4,
    "hurt": 0,
    "cool": 0,
    "alive": True,
    "bullets": []
  }


def new_players(mode):
  if mode == 1:
    return [make(WIDTH // 2 - 25, ship, laser,
      [pygame.K_a, pygame.K_LEFT], [pygame.K_d, pygame.K_RIGHT],
      [pygame.K_w, pygame.K_UP], [pygame.K_s, pygame.K_DOWN],
      [pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_RSHIFT])]

  return [
    make(WIDTH // 3 - 25, ship, laser,
      [pygame.K_a], [pygame.K_d], [pygame.K_w], [pygame.K_s],
      [pygame.K_SPACE]),
    make(WIDTH * 2 // 3 - 25, ship2, laser2,
      [pygame.K_LEFT], [pygame.K_RIGHT], [pygame.K_UP], [pygame.K_DOWN],
      [pygame.K_RSHIFT])
  ]


blocks = []
enemies = []
ebullets = []
score = 0
dead = False
menu = True
mode = 1
players = new_players(mode)

running = True
while running:
  clock.tick(60)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  keys = pygame.key.get_pressed()

  if menu:
    screen.fill((20, 20, 30))
    t1 = big.render("DODGE OR DIE", False, (220, 80, 80))
    t2 = font.render("1  SINGLE PLAYER", False, (255, 255, 255))
    t3 = font.render("2  TWO PLAYER", False, (255, 255, 255))

    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 200))
    screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 340))
    screen.blit(t3, (WIDTH // 2 - t3.get_width() // 2, 400))
    pygame.display.flip()

    if keys[pygame.K_1]:
      mode = 1
      players = new_players(mode)
      menu = False
    if keys[pygame.K_2]:
      mode = 2
      players = new_players(mode)
      menu = False
    continue

  if dead:
    screen.fill((20, 20, 30))
    t1 = big.render("GAME OVER", False, (220, 80, 80))
    t2 = font.render("Score: " + str(score // 60) + "  R restart   M menu", False, (255, 255, 255))

    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 250))
    screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 340))
    pygame.display.flip()

    if keys[pygame.K_r] or keys[pygame.K_m]:
      blocks = []
      enemies = []
      ebullets = []
      score = 0
      players = new_players(mode)
      dead = False
      if keys[pygame.K_m]:
        menu = True
    continue

  for p in players:
    if not p["alive"]:
      continue

    r = p["rect"]
    if any(keys[k] for k in p["left"]):
      r.x -= 6
    if any(keys[k] for k in p["right"]):
      r.x += 6
    if any(keys[k] for k in p["up"]):
      r.y -= 5
    if any(keys[k] for k in p["down"]):
      r.y += 5
    r.x = max(0, min(WIDTH - 50, r.x))
    r.y = max(HEIGHT // 2, min(HEIGHT - 38, r.y))

    p["cool"] -= 1
    if any(keys[k] for k in p["fire"]) and p["cool"] <= 0:
      p["bullets"].append(pygame.Rect(r.centerx - 5, r.y, 10, 30))
      shoot.play()
      p["cool"] = 15

  if random.random() < 0.05:
    blocks.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 40))

  if random.random() < 0.004 and len(enemies) < 2:
    enemies.append({"rect": pygame.Rect(random.randint(0, WIDTH - 60), -50, 60, 50), "hp": 2, "cool": 60, "dx": 3})

  for b in blocks:
    b.y += 5

  for p in players:
    for bl in p["bullets"]:
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

    p["bullets"] = [bl for bl in p["bullets"] if bl.y > -20]

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

  for p in players:
    if not p["alive"]:
      continue

    damage = 0
    for b in blocks:
      if b.colliderect(p["rect"]):
        damage += 1
        b.y = HEIGHT + 100
    for eb in ebullets:
      if eb.colliderect(p["rect"]):
        damage += 2
        eb.y = HEIGHT + 100

    if damage > 0 and p["hurt"] <= 0:
      p["hearts"] -= damage
      p["hurt"] = 90
      hit.play()
    p["hurt"] -= 1

    if p["hearts"] <= 0:
      p["alive"] = False
      lose.play()

  if not any(p["alive"] for p in players):
    dead = True

  blocks = [b for b in blocks if b.y < HEIGHT]
  ebullets = [eb for eb in ebullets if eb.y < HEIGHT]
  score += 1

  screen.fill((20, 20, 30))
  for p in players:
    if p["alive"] and (p["hurt"] <= 0 or p["hurt"] // 6 % 2 == 0):
      screen.blit(p["img"], p["rect"])
    for bl in p["bullets"]:
      screen.blit(p["laser"], bl)
  for b in blocks:
    screen.blit(rock, b)
  for e in enemies:
    screen.blit(enemy, e["rect"])
  for eb in ebullets:
    screen.blit(elaser, eb)

  for n, p in enumerate(players):
    for i in range(p["hearts"]):
      if n == 0:
        screen.blit(heart, (10 + i * 36, 50))
      else:
        screen.blit(heart, (WIDTH - 40 - i * 36, 10))

  text = font.render(str(score // 60), False, (255, 255, 255))
  screen.blit(text, (10, 10))
  pygame.display.flip()

print("Score:", score // 60)