import pygame
from constants import *
from models import Piece, Board


class Picasso:

    # Convert in game coordinates/(half)tiles to pixels that pygame understands
    @staticmethod
    def _coordsToPixel(coords: tuple, screen: pygame.Surface) -> tuple:
        x = TILE_SIZE * coords[0] / 2 + BORDER
        # by default y pos is down. The tile coordinates are up
        y = screen.get_height() - (TILE_SIZE * coords[1] / 2 + BORDER)
        return (x, y)

    # Draw the board and its contents in its current form
    @staticmethod
    def drawBoard(screen: pygame.Surface, board: Board):
        # Clear the screen with dark background
        screen.fill(BOARD_COL)

        # Add grid
        for i in range(board.dimensions[0]):
            pygame.draw.line(
                screen,
                BOARD_ACCENT,
                (BORDER + i * TILE_SIZE, BORDER),
                (BORDER + i * TILE_SIZE, screen.get_height() - BORDER),
                GRID_WIDTH,
            )

        for i in range(board.dimensions[1]):
            pygame.draw.line(
                screen,
                BOARD_ACCENT,
                (BORDER, BORDER + i * TILE_SIZE),
                (screen.get_width() - BORDER, i * TILE_SIZE + BORDER),
                GRID_WIDTH,
            )

        # Add required vertices (level requirements)
        for vortex in board.vertices:
            pygame.draw.circle(screen, PIECE_ACCENT,
                               Picasso._coordsToPixel(vortex, screen), VORTEX_SIZE)

        # Add already placed pieces
        for piece in board.placedPieces:
            Picasso.drawPiece(screen, piece)

    # Draw the piece on the screen
    @staticmethod
    def drawPiece(screen: pygame.Surface, piece: Piece):
        for tile in piece.size:
            # offset by one since rects are not drawn centered around coords but down and rigth
            coords = (tile[0] - 1, tile[1]+1)

            pixel = Picasso._coordsToPixel(coords, screen)

            pygame.draw.rect(
                screen, PIECE_BACKG, (pixel[0], pixel[1], TILE_SIZE, TILE_SIZE)
            )

            # draw an edge around the tile
            if (tile[0] + 2, tile[1]) not in piece.size:
                pygame.draw.line(
                    screen,
                    PIECE_BORDER,
                    Picasso._coordsToPixel((tile[0] + 1, tile[1] - 1), screen),
                    Picasso._coordsToPixel((tile[0] + 1, tile[1] + 1), screen),
                    TILE_BORDER_WIDTH,
                )
            if (tile[0], tile[1] + 2) not in piece.size:
                pygame.draw.line(
                    screen,
                    PIECE_BORDER,
                    Picasso._coordsToPixel((tile[0] - 1, tile[1] + 1), screen),
                    Picasso._coordsToPixel((tile[0] + 1, tile[1] + 1), screen),
                    TILE_BORDER_WIDTH,
                )
            if (tile[0] - 2, tile[1]) not in piece.size:
                pygame.draw.line(
                    screen,
                    PIECE_BORDER,
                    Picasso._coordsToPixel((tile[0] - 1, tile[1] - 1), screen),
                    Picasso._coordsToPixel((tile[0] - 1, tile[1] + 1), screen),
                    TILE_BORDER_WIDTH,
                )
            if (tile[0], tile[1] - 2) not in piece.size:
                pygame.draw.line(
                    screen,
                    PIECE_BORDER,
                    Picasso._coordsToPixel((tile[0] - 1, tile[1] - 1), screen),
                    Picasso._coordsToPixel((tile[0] + 1, tile[1] - 1), screen),
                    TILE_BORDER_WIDTH,
                )

        for vortex in piece.vertices:
            pygame.draw.circle(screen, PIECE_ACCENT,
                               Picasso._coordsToPixel(vortex, screen), VORTEX_SIZE)

        for io in piece.IO:
            pixel = [x - (IO_SIZE / 2)
                     for x in Picasso._coordsToPixel(io, screen)]
            pygame.draw.rect(screen, PIECE_ACCENT,
                             (pixel[0], pixel[1], IO_SIZE, IO_SIZE))

    # Draw the cursor on the screen
    @staticmethod
    def drawCursor(screen: pygame.Surface, piece: Piece):
        pygame.draw.circle(
            screen, CURSOR_COL, Picasso._coordsToPixel(
                (piece.x, piece.y), screen), CURSOR_SIZE
        )

    # Draw text on the screen
    def drawText(screen: pygame.Surface, str: str):

        font = pygame.font.SysFont(None, 48)
        text_surface = font.render(str, True, TEXT_COL)

        # Blit the text surface to the display surface
        screen.blit(
            text_surface,
            ((BORDER - FONT_SIZE)/2, (BORDER - FONT_SIZE)/2)
        )
