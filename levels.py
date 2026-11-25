import pygame

levels = [
  {"name": "FIRST CONTACT", "time": 45, "rocks": 0.03, "speed": 4, "enemies": 0, "ecool": 100, "bg": 2, "goal": "meteor", "need": 10},
  {"name": "ROCK FIELD",    "time": 50, "rocks": 0.05, "speed": 5, "enemies": 0, "ecool": 100, "bg": 3, "goal": "meteor", "need": 20},
  {"name": "HOSTILES",      "time": 60, "rocks": 0.04, "speed": 5, "enemies": 1, "ecool": 100, "bg": 1, "goal": "ship",   "need": 3 },
  {"name": "CROSS FIRE",    "time": 70, "rocks": 0.05, "speed": 6, "enemies": 2, "ecool": 80,  "bg": 0, "goal": "ship",   "need": 5 },
  {"name": "LAST STAND",    "time": 80, "rocks": 0.06, "speed": 7, "enemies": 3, "ecool": 60,  "bg": 2, "goal": "ship",   "need": 6 }
]


star = ["   X   ", "  XXX  ", "XXXXXXX", " XXXXX ", "  XXX  ", " XX XX ", " X   X "]


def get_stars(lv, left, lost):
  n = 1
  if left >= lv["time"] // 2:
    n += 1
  if lost <= 2:
    n += 1
  return n


def draw_stars(screen, x, y, n, s):
  for i in range(3):
    col = (255, 230, 80) if i < n else (60, 55, 80)
    for r, row in enumerate(star):
      for c, ch in enumerate(row):
        if ch == "X":
          pygame.draw.rect(screen, col, (x + i * 8 * s + c * s, y + r * s, s, s))


def draw_select(screen, big, tiny, small, cur, unlocked, best, width):
  t1 = big.render("SELECT LEVEL", False, (220, 80, 80))
  screen.blit(t1, (width // 2 - t1.get_width() // 2, 100))

  for i in range(len(levels)):
    x = 35 + i * 180
    lv = levels[i]
    ok = i < unlocked
    col = (255, 255, 255) if ok else (90, 90, 110)
    edge = (255, 230, 80) if i == cur else col

    pygame.draw.rect(screen, (30, 25, 45), (x, 250, 170, 220))
    pygame.draw.rect(screen, edge, (x, 250, 170, 220), 4)

    num = big.render(str(i + 1), False, col)
    screen.blit(num, (x + 85 - num.get_width() // 2, 275))
    name = tiny.render(lv["name"], False, col)
    screen.blit(name, (x + 85 - name.get_width() // 2, 360))

    if ok:
      goal = tiny.render(str(lv["need"]) + (" METEORS" if lv["goal"] == "meteor" else " SHIPS"), False, (255, 230, 80))
      tm = tiny.render(str(lv["time"]) + " SEC", False, (160, 160, 180))
      screen.blit(goal, (x + 85 - goal.get_width() // 2, 400))
      screen.blit(tm, (x + 85 - tm.get_width() // 2, 425))
      draw_stars(screen, x + 85 - 34, 442, best[i], 3)
    else:
      lk = tiny.render("LOCKED", False, (90, 90, 110))
      screen.blit(lk, (x + 85 - lk.get_width() // 2, 410))

  hint = small.render("A D CHOOSE    SPACE PLAY    M MENU", False, (160, 160, 180))
  screen.blit(hint, (width // 2 - hint.get_width() // 2, 600))