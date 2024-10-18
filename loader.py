from models import Board, Piece
import json


class Loader:
    @staticmethod
    def loadJSON(lvl: str):
        # load pieces
        # Load JSON from a file
        with open('pieces.json', 'r') as file:
            piecesJSON = json.load(file)

        # convert JSON to python data types
        pieces = []
        for pieceJSON in piecesJSON.get("pieces"):
            piece = Piece(pieceJSON)
            pieces.append(piece)

        # load level
        # Load JSON from a file
        with open('level.json', 'r') as file:
            level = json.load(file)

        # convert JSON to python data type
        board = Board(level[lvl], pieces)

        return board
