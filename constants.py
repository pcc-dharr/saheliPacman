# Tile dimensions
TILEWIDTH = 16  # Width of each tile in pixels
TILEHEIGHT = 16  # Height of each tile in pixels

# Grid dimensions
NROWS = 36  # Number of rows in the grid
NCOLS = 28  # Number of columns in the grid

# Screen dimensions
SCREENWIDTH = NCOLS * TILEWIDTH  # Total screen width in pixels
SCREENHEIGHT = NROWS * TILEHEIGHT  # Total screen height in pixels
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)  # Screen size as a tuple (width, height)

# Color definitions (RGB values)
BLACK = (0, 0, 0)  # Black color
YELLOW = (255, 255, 0)  # Yellow color
WHITE = (255, 255, 255)  # White color
RED = (255, 0, 0)  # Red color
PINK = (255, 100, 150)  # Pink color
TEAL = (100, 255, 255)  # Teal color
ORANGE = (230, 190, 40)  # Orange color
GREEN = (0, 255, 0)  # Green color

# Movement directions
STOP = 0  # No movement
UP = 1  # Movement upwards
DOWN = -1  # Movement downwards
LEFT = 2  # Movement to the left
RIGHT = -2  # Movement to the right

# Entity types
PACMAN = 0  # Pacman entity
PORTAL = 3  # Portal entity
PELLET = 1  # Pellet entity
POWERPELLET = 2  # Power pellet entity
GHOST = 3  # Ghost entity

# Game modes
SCATTER = 0  # Scatter mode for ghosts
CHASE = 1  # Chase mode for ghosts
FREIGHT = 2  # Freight mode for ghosts
SPAWN = 3  # Spawn mode for ghosts

# Ghost identifiers
BLINKY = 4  # Blinky ghost
PINKY = 5  # Pinky ghost
INKY = 6  # Inky ghost
CLYDE = 7  # Clyde ghost

# Other game entities
FRUIT = 8  # Fruit entity

# Text types for UI
SCORETXT = 0  # Score text
LEVELTXT = 1  # Level text
READYTXT = 2  # Ready text
PAUSETXT = 3  # Pause text
GAMEOVERTXT = 4  # Game over text
