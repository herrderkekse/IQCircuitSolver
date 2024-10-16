# sizes and constraints
TILE_SIZE: int = 200  # size of one game tile in pixel
BORDER: int = TILE_SIZE / 2

IO_SIZE: int = TILE_SIZE / 10
VORTEX_SIZE: int = TILE_SIZE / 3
CURSOR_SIZE: int = TILE_SIZE / 10
GRID_WIDTH: int = int(TILE_SIZE / 20)
TILE_BORDER_WIDTH: int = int(TILE_SIZE / 30)

# colors (RGB format)
BOARD_COL = (0, 0, 0)
BOARD_ACCENT = (50, 50, 50)

PIECE_BACKG = (150, 150, 150)
PIECE_ACCENT = (200, 200, 0)
PIECE_BORDER = (200, 200, 200)

CURSOR_COL = (255, 0, 0)

# Text stuff
FONT_SIZE = 48
DISPLAY_DURATION = 1000  # millis
TEXT_COL = (255, 0, 0)
