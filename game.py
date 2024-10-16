import pygame
import sys
from models import Piece, Board
from loader import Loader
from painter import Picasso
from constants import *


# load the game confiuration from pieces.json and level.json
board = Loader.loadJSON()

# Initialize Pygame
pygame.init()

# Set up the window (width, height)
screenDim = tuple(x * TILE_SIZE / 2 + 2 * BORDER for x in board.dimensions)
screen = pygame.display.set_mode(screenDim)
pygame.display.set_caption("IQ Circuit Emulator")

# Set up game clock for managing frame rate
clock = pygame.time.Clock()

# initialize the currently selected piece
current_piece: Piece = board.leftPieces[0]


# Main game loop
running = True
last_time = pygame.time.get_ticks()  # Start time
text_start = None  # will be set to the time the text starts to display
while running:

    # region handle input
    # Handle events (e.g., user input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keypress handling (arrow keys to move the square)
        if event.type == pygame.KEYDOWN:
            # cursor movement
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                current_piece.x -= 2
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                current_piece.x += 2
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                current_piece.y -= 2
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                current_piece.y += 2
            # piece placement
            if event.key == pygame.K_RETURN:
                if not board.placePiece(current_piece):
                    text_start = pygame.time.get_ticks()
                else:
                    current_piece = (
                        board.leftPieces[0]
                        if len(board.leftPieces) != 0
                        else Piece(dict({"ID": 11, "name": "you won", "size": [], "front": {"vertices": [], "IO": []}, "back": {"vertices": [], "IO": []}, }))
                    )
            if event.key == pygame.K_BACKSPACE:
                board.removeLastPiece()
            # piece rotation
            if event.key == pygame.K_p or event.key == pygame.K_e:
                current_piece.rotation += 90
            if event.key == pygame.K_o or event.key == pygame.K_q:
                current_piece.rotation -= 90
            # flip piece
            if event.key == pygame.K_r:
                current_piece.flip()
            # piece selection
            if event.key == pygame.K_c:
                current_piece = board.leftPieces[(board.leftPieces.index(
                    current_piece) + 1) % len(board.leftPieces)]
            if event.key == pygame.K_y:
                current_piece = board.leftPieces[(board.leftPieces.index(
                    current_piece) - 1) % len(board.leftPieces)]

    # endregion

    # Prevent square from moving off the board
    current_piece.x = max(1, min(board.dimensions[0] - 1, current_piece.x))
    current_piece.y = max(1, min(board.dimensions[1] - 1, current_piece.y))

    # Draw the background and objects
    Picasso.drawBoard(screen, board)
    Picasso.drawPiece(screen, current_piece)
    Picasso.drawCursor(screen, current_piece)

    # draw Text
    # Check if the time elapsed is less than the display duration
    if text_start != None and pygame.time.get_ticks() - text_start < DISPLAY_DURATION:
        Picasso.drawText(screen, "Not a valid move")

    # Update the display
    pygame.display.flip()

    # Control the frame rate (60 FPS)
    clock.tick(60)

# Exiting the game safely
pygame.quit()
