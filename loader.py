from models import Board, Piece
import json


class Loader:
    @staticmethod
    def loadJSON():
        # load pieces
        # Load JSON from a file
        with open('pieces.json', 'r') as file:
            piecesJSON = json.load(file)

        # convert JSON to python data types
        pieces = [None] * 10
        for pieceJSON in piecesJSON.get("pieces"):
            piece = Piece(pieceJSON)
            pieces[piece.id] = piece

        # load level
        # Load JSON from a file
        with open('level.json', 'r') as file:
            level = json.load(file)

        # convert JSON to python data type
        board = Board(level["level1"], pieces)

        return board
