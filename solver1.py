import pygame
from models import Piece, Board
from loader import Loader
from painter import Picasso
from constants import *
import time

# load the game confiuration from pieces.json and level.json
board = Loader.loadJSON("level1")


def solveStep(board: Board, piecesDown: list) -> bool:

    if len(board.freeTiles) == 0:
        return True

    for piece in board.leftPieces[:]:
        for side in range(piece.sides):
            piece.side = side
            for rotation in [0, 90, 180, 270]:
                if side == 2 and (rotation == 180 or rotation == 270):
                    # the third/empty side is symmetric
                    continue

                piece.rotation = rotation
                for tile in board.freeTiles[:]:
                    piece.x = tile[0]
                    piece.y = tile[1]

                    piecesDown.append((piece.id, side, rotation, tile))
                    if board.placePiece(piece):
                        # coment in for visuals and progress
                        # print(piecesDown)
                        # Picasso.drawBoard(screen, board)
                        # Update the display
                        # pygame.display.flip()

                        if solveStep(board, piecesDown):
                            return True  # succesfully solved
                        else:
                            board.removeLastPiece()  # backtrack

                    piecesDown.remove((piece.id, side, rotation, tile))
    return False


# Initialize Pygame
pygame.init()

# Set up the window (width, height)
screenDim = tuple(x * TILE_SIZE / 2 + 2 * BORDER for x in board.dimensions)
screen = pygame.display.set_mode(screenDim)
pygame.display.set_caption("IQ Circuit Solver")

# happy solving
if solveStep(board, []):
    while True:
        Picasso.drawBoard(screen, board)
        pygame.display.flip()
        print("congratulations!!!! Theres a solutions")
else:
    print("no solution exists. I've tried'em all...")
