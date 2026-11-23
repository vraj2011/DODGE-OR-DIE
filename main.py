import pygame
import random
from levels import levels, draw_select

pygame.init()
pygame.display.set_caption("DODGE OR DIE")
WIDTH = 960
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font("assets/font.ttf", 24)
big = pygame.font.Font("assets/font.ttf", 56)
small = pygame.font.Font("assets/font.ttf", 14)
tiny = pygame.font.Font("assets/font.ttf", 12)

def load(f):
  img = pygame.image.load(f).convert_alpha()
  return pygame.transform.scale(img, (50, 38))

reds = [load("assets/red1.png"), load("assets/red2.png"), load("assets/red3.png")]
blues = [load("assets/blue1.png"), load("assets/blue2.png"), load("assets/blue3.png")]
bgs = [pygame.image.load("assets/bg_" + n + ".png").convert() for n in ["black", "blue", "darkPurple", "purple"]]
bg_i = 2
scroll = 0


def draw_bg():
  for x in range(0, WIDTH, 256):
    for y in range(-256, HEIGHT, 256):
      screen.blit(bgs[bg_i], (x, y + scroll))

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
pop = pygame.mixer.Sound("assets/boom_small.ogg")
pop.set_volume(0.3)
boom = pygame.mixer.Sound("assets/boom_big.ogg")

COL_S = [(255, 230, 80), (255, 255, 255)]
COL_B = [(255, 230, 80), (255, 150, 40), (230, 60, 40), (255, 255, 255)]
sparks = []


def blast(x, y, n, size, colors):
  for i in range(n):
    sparks.append({"x": x, "y": y, "vx": random.uniform(-4, 4), "vy": random.uniform(-4, 4), "life": random.randint(15, 35), "c": random.choice(colors), "s": size})


heart = pygame.Surface((28, 24), pygame.SRCALPHA)
shape = [" XX XX ", "XXXXXXX", "XXXXXXX", " XXXXX ", "  XXX  ", "   X   "]
for y, row in enumerate(shape):
  for x, ch in enumerate(row):
    if ch == "X":
      pygame.draw.rect(heart, (230, 50, 70), (x * 4, y * 4, 4, 4))


stats = [
  {"name": "SCOUT", "speed": 8, "hearts": 3, "cool": 10},
  {"name": "FIGHTER", "speed": 6, "hearts": 4, "cool": 15},
  {"name": "TANK", "speed": 4, "hearts": 5, "cool": 20}
]


def make(x, imgs, lz, left, right, up, down, fire, pick):
  s = stats[pick]
  return {
    "rect": pygame.Rect(x, HEIGHT - 80, 50, 38),
    "img": imgs[pick],
    "laser": lz,
    "left": left,
    "right": right,
    "up": up,
    "down": down,
    "fire": fire,
    "speed": s["speed"],
    "maxcool": s["cool"],
    "hearts": s["hearts"],
    "hurt": 0,
    "cool": 0,
    "alive": True,
    "bullets": []
  }


def new_players(mode):
  if mode == 1:
    return [make(WIDTH // 2 - 25, reds, laser,
      [pygame.K_a, pygame.K_LEFT], [pygame.K_d, pygame.K_RIGHT],
      [pygame.K_w, pygame.K_UP], [pygame.K_s, pygame.K_DOWN],
      [pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_RSHIFT], picks[0])]

  return [
    make(WIDTH // 3 - 25, reds, laser,
      [pygame.K_a], [pygame.K_d], [pygame.K_w], [pygame.K_s],
      [pygame.K_SPACE], picks[0]),
    make(WIDTH * 2 // 3 - 25, blues, laser2,
      [pygame.K_LEFT], [pygame.K_RIGHT], [pygame.K_UP], [pygame.K_DOWN],
      [pygame.K_RSHIFT], picks[1])
  ]


blocks = []
enemies = []
ebullets = []
score = 0
dead = False
menu = True
mode = 1
select = False
turn = 0
picks = [1, 1]
players = new_players(mode)
over = 0
level = 0
ltimer = 0
lvl_done = False
win = False
got = 0
msg = "GAME OVER"
lsel = False
cur = 0
unlocked = 1

running = True
while running:
  clock.tick(60)
  scroll = (scroll + 1) % 256

  tapped = []
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      tapped.append(event.key)

  keys = pygame.key.get_pressed()

  if menu:
    draw_bg()
    t1 = big.render("DODGE OR DIE", False, (220, 80, 80))
    t2 = font.render("1  SINGLE PLAYER", False, (255, 255, 255))
    t3 = font.render("2  TWO PLAYER", False, (255, 255, 255))

    draw_bg()
    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 200))
    screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 340))
    screen.blit(t3, (WIDTH // 2 - t3.get_width() // 2, 400))

    pygame.display.flip()

    if keys[pygame.K_1]:
      mode = 1
      menu = False
      select = True
    if keys[pygame.K_2]:
      mode = 2
      menu = False
      select = True
    continue

  if select:
    for k in tapped:
      if k in (pygame.K_a, pygame.K_LEFT):
        picks[turn] = (picks[turn] - 1) % 3
      if k in (pygame.K_d, pygame.K_RIGHT):
        picks[turn] = (picks[turn] + 1) % 3
      if k in (pygame.K_SPACE, pygame.K_RETURN):
        turn += 1
        if turn >= mode:
          turn = 0
          select = False
          lsel = True

    draw_bg()
    t1 = big.render("PLAYER " + str(turn + 1), False, (220, 80, 80))
    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 100))

    imgs = reds if turn == 0 else blues
    for i in range(3):
      x = 170 + i * 260
      s = stats[i]
      screen.blit(pygame.transform.scale(imgs[i], (100, 76)), (x, 270))
      name = font.render(s["name"], False, (255, 255, 255))
      screen.blit(name, (x + 50 - name.get_width() // 2, 370))
      lines = ["SPEED " + str(s["speed"]), "HEARTS " + str(s["hearts"]), "FIRE " + str(60 // s["cool"])]
      for j, line in enumerate(lines):
        t = small.render(line, False, (160, 160, 180))
        screen.blit(t, (x + 50 - t.get_width() // 2, 420 + j * 26))
      if i == picks[turn]:
        pygame.draw.rect(screen, (255, 230, 80), (x - 30, 240, 160, 280), 3)

    hint = small.render("A D  CHOOSE     SPACE  CONFIRM", False, (160, 160, 180))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 600))
    pygame.display.flip()
    continue

  if lsel:
    for k in tapped:
      if k in (pygame.K_a, pygame.K_LEFT):
        cur = (cur - 1) % len(levels)
      if k in (pygame.K_d, pygame.K_RIGHT):
        cur = (cur + 1) % len(levels)
      if k == pygame.K_m:
        lsel = False
        menu = True
      if k in (pygame.K_SPACE, pygame.K_RETURN) and cur < unlocked:
        level = cur
        bg_i = levels[level]["bg"]
        players = new_players(mode)
        blocks = []
        enemies = []
        ebullets = []
        sparks = []
        over = 0
        ltimer = 0
        got = 0
        score = 0
        win = False
        msg = "GAME OVER"
        dead = False
        lsel = False

    draw_bg()
    draw_select(screen, big, tiny, small, cur, unlocked, WIDTH)
    pygame.display.flip()
    continue

  if lvl_done:
    ltimer += 1
    draw_bg()
    t1 = big.render("LEVEL " + str(level + 1) + " DONE", False, (255, 230, 80))
    t2 = font.render("Score: " + str(score // 60) + "   SPACE  next level", False, (255, 255, 255))
    t3 = small.render("NEXT  " + levels[level + 1]["name"], False, (160, 160, 180))

    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 230))
    screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 330))
    screen.blit(t3, (WIDTH // 2 - t3.get_width() // 2, 400))
    pygame.display.flip()

    if ltimer > 60 and pygame.K_SPACE in tapped:
      level += 1
      ltimer = 0
      got = 0
      bg_i = levels[level]["bg"]
      blocks = []
      enemies = []
      ebullets = []
      sparks = []
      for p in players:
        p["bullets"] = []
        if not p["alive"]:
          p["alive"] = True
          p["hearts"] = 2
      lvl_done = False
    continue
    
  if dead:
    draw_bg()
    t1 = big.render(msg, False, (255, 230, 80) if win else (220, 80, 80))
    t2 = font.render("Score: " + str(score // 60), False, (255, 255, 255))
    t3 = small.render("R RETRY    L LEVELS    M MENU", False, (160, 160, 180))

    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 250))
    screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 340))
    screen.blit(t3, (WIDTH // 2 - t3.get_width() // 2, 410))
    pygame.display.flip()

    if keys[pygame.K_r] or keys[pygame.K_m] or keys[pygame.K_l]:
      blocks = []
      enemies = []
      ebullets = []
      sparks = []
      over = 0
      ltimer = 0
      win = False
      got = 0
      msg = "GAME OVER"
      score = 0
      players = new_players(mode)
      dead = False
      if keys[pygame.K_m]:
        menu = True
      if keys[pygame.K_l]:
        lsel = True
    continue

  for p in players:
    if not p["alive"]:
      continue

    r = p["rect"]
    if any(keys[k] for k in p["left"]):
      r.x -= p["speed"]
    if any(keys[k] for k in p["right"]):
      r.x += p["speed"]
    if any(keys[k] for k in p["up"]):
      r.y -= p["speed"]
    if any(keys[k] for k in p["down"]):
      r.y += p["speed"]
    r.x = max(0, min(WIDTH - 50, r.x))
    r.y = max(HEIGHT // 2, min(HEIGHT - 38, r.y))

    p["cool"] -= 1
    if any(keys[k] for k in p["fire"]) and p["cool"] <= 0:
      p["bullets"].append(pygame.Rect(r.centerx - 5, r.y, 10, 30))
      shoot.play()
      p["cool"] = p["maxcool"]

  L = levels[level]
  if random.random() < L["rocks"]:
    blocks.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 40))

  if random.random() < 0.004 and len(enemies) < L["enemies"]:
    enemies.append({"rect": pygame.Rect(random.randint(0, WIDTH - 60), -50, 60, 50), "hp": 2, "cool": 60, "dx": 3})

  for b in blocks:
    b.y += L["speed"]

  for p in players:
    for bl in p["bullets"]:
      bl.y -= 10
      for b in blocks:
        if bl.colliderect(b):
          blast(b.centerx, b.centery, 8, 4, COL_S)
          blocks.remove(b)
          bl.y = -100
          score += 120
          if L["goal"] == "meteor":
            got += 1
          break

      for e in enemies:
        if bl.colliderect(e["rect"]):
          e["hp"] -= 1
          bl.y = -100
          if e["hp"] <= 0:
            blast(e["rect"].centerx, e["rect"].centery, 30, 7, COL_B)
            boom.play()
            enemies.remove(e)
            score += 300
            if L["goal"] == "ship":
              got += 1
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
      e["cool"] = L["ecool"]

  for eb in ebullets:
    eb.y += 7

  for p in players:
    for bl in p["bullets"]:
      for eb in ebullets:
        if bl.colliderect(eb):
          blast(bl.centerx, bl.centery, 8, 4, COL_S)
          pop.play()
          bl.y = -100
          eb.y = HEIGHT + 100
          break

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
      blast(p["rect"].centerx, p["rect"].centery, 30, 7, COL_B)
      lose.play()

  if not any(p["alive"] for p in players):
    over += 1
    if over > 70:
      dead = True

  for sp in sparks:
    sp["x"] += sp["vx"]
    sp["y"] += sp["vy"]
    sp["life"] -= 1
  sparks = [sp for sp in sparks if sp["life"] > 0]

  blocks = [b for b in blocks if b.y < HEIGHT]
  ebullets = [eb for eb in ebullets if eb.y < HEIGHT]
  score += 1
  
  ltimer += 1
  if got >= L["need"] and any(p["alive"] for p in players):
    unlocked = max(unlocked, min(level + 2, len(levels)))
    ltimer = 0
    if level == len(levels) - 1:
      win = True
      msg = "YOU WIN"
      dead = True
    else:
      lvl_done = True
  elif ltimer >= L["time"] * 60:
    msg = "TIME UP"
    dead = True

  draw_bg()
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

  for sp in sparks:
    s = max(2, sp["s"] * sp["life"] // 35)
    pygame.draw.rect(screen, sp["c"], (sp["x"], sp["y"], s, s))

  for n, p in enumerate(players):
    for i in range(p["hearts"]):
      if n == 0:

        screen.blit(heart, (10 + i * 36, 50))
      else:
        screen.blit(heart, (WIDTH - 40 - i * 36, 10))

  lt = font.render("LEVEL " + str(level + 1) + "   " + str(L["time"] - ltimer // 60), False, (255, 255, 255))
  screen.blit(lt, (WIDTH // 2 - lt.get_width() // 2, 10))
  gt = small.render(("METEORS " if L["goal"] == "meteor" else "SHIPS ") + str(min(got, L["need"])) + "/" + str(L["need"]), False, (255, 230, 80))
  screen.blit(gt, (WIDTH // 2 - gt.get_width() // 2, 44))

  text = font.render(str(score // 60), False, (255, 255, 255))
  screen.blit(text, (10, 10))
  pygame.display.flip()

print("Score:", score // 60)