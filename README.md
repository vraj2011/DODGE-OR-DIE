# Dodge or Die

- A fast arcade space shooter for one or two players, built in Python with pygame.
- Dodge the meteors, shoot down enemy ships, and survive five levels, each with its own goal and deadline.

- This is my first game, made for Hack Club.

# Screenshots
<img width="1917" height="1198" alt="Screenshot 2026-11-25 211346" src="https://github.com/user-attachments/assets/fed9b561-261e-4862-a74e-88dc06848229" />
<img width="1917" height="1198" alt="Screenshot 2026-11-25 211354" src="https://github.com/user-attachments/assets/919beb18-95b8-4255-bcc3-2c59fef67b97" />
<img width="1917" height="1198" alt="Screenshot 2026-11-25 211444" src="https://github.com/user-attachments/assets/851dfd97-ac21-48d7-ab3f-a1b456f803d0" />
<img width="1917" height="1198" alt="Screenshot 2026-11-25 211426" src="https://github.com/user-attachments/assets/2e0d43ed-8244-4add-9023-0a595dd92500" />


# Features
-Single player and local two-player on one keyboard
- 5 levels, each with a goal (destroy a number of meteors or enemy ships) and a time limit
- 3 ships with different stats: Scout (fast, fires quickly, 3 hearts), Fighter (balanced, 4 hearts) and Tank (slow, 5 hearts)
- Enemy ships that shoot back, and bullets you can shoot out of the air
- Explosions, sound effects and a scrolling space background
- Level select screen that unlocks levels as you beat them

# Download and play (Windows)
- Go to the Releases page and download the latest .exe
- Run the game. Windows may show a SmartScreen warning because the file is not signed: click More info, then Run anyway.
- Pick single player or two-player, choose your ship, choose a level, and play.
- Run from source

- NOTE: You need Python 3 and pygame-ce.

git clone https://github.com/vraj2011/DODGE-OR-DIE/
cd DODGE-OR-DIE
pip install pygame-ce
python main.py

- On Windows you can also use py main.py.

# Controls
- Action	Single player	Player 1 (two-player)	Player 2 (two-player)
- Move	WASD or arrow keys	WASD	Arrow keys
-  Shoot	Space or Shift	Space	Right Shift

# Menus:

- Menu: 1 single player, 2 two-player
- Ship select and level select: A / D to choose, Space to confirm, M to go back to the menu (level select)
- Game over: R retry the level, L level select, M menu

# How to play

- Each level has a goal shown at the top of the screen, such as METEORS 4/10, and a countdown.
-  Reach the goal before time runs out to win the level.
-   A meteor hit costs 1 heart and an enemy bullet costs 2.
-    In two-player, both ships share the same goal, and if you lose all your hearts the other player keeps going.

# Built with
Python and pygame-ce
Compiled to an .exe 
# Credits
Art and sound effects: Space Shooter Redux by Kenney, released under CC0
Other sounds: from kenney.nl
