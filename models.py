import math
from constants import SIDEABLE_IDS

# model of a physical piece to lay down on the board


class Piece:
    def __init__(self, pieceDict: dict):
        # pieceDict - a dictionary/json object holding all the information about the piece

        # placement on the board. The following locations are relative to this (the getter makes vertices and IO absolute/relatice to the global origin)
        self.x = 1
        self.y = 1
        # in degree from 0 to 270 in 90 steps
        self._rotation = 0
        self.side = 0  # 0 = front; 1 = back; 3 = side where possible

        # identifiers
        self.id = pieceDict.get("ID")
        self.name = pieceDict.get("name")  # mainly used for easy debug

        # shape
        self._size = [
            tuple(map(int, s.strip("()").split(","))) for s in pieceDict.get("size")
        ]

        self._vertices = [
            [
                tuple(map(int, s.strip("()").split(",")))
                for s in pieceDict.get("front").get("vertices")
            ],
            [
                tuple(map(int, s.strip("()").split(",")))
                for s in pieceDict.get("back").get("vertices")
            ]
        ]
        self._IO = [
            [
                tuple(map(int, s.strip("()").split(",")))
                for s in pieceDict.get("front").get("IO")
            ],
            [
                tuple(map(int, s.strip("()").split(",")))
                for s in pieceDict.get("back").get("IO")
            ]
        ]

    # turns the piece around
    def flip(self):
        self.side = (self.side + 1) % self.sides

    # calcualtes the absolute coordinates i.e. wrt. the board origin
    def _makeAbsolute(self, coords: tuple) -> tuple:
        # r' = Rr + b
        # rotate relative coordinates around (self.x,self.y)
        theta = (
            self._rotation * math.pi / 180
        )  # convert to radiants. _rotation is enough since sin, cos are 2Pi periodic
        x = math.cos(theta) * coords[0] - math.sin(theta) * coords[1]
        y = math.sin(theta) * coords[0] + math.cos(theta) * coords[1]
        x = round(x)
        y = round(y)  # account for inexact pi#

        # add the affine component
        x += self.x
        y += self.y

        return (x, y)

    # region get/set rotation
    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value % 360

    # endregion

    # region get/set vertices
    @property
    def vertices(self):
        if self.side == 0:
            return [self._makeAbsolute(vortex) for vortex in self._vertices[0]]
        elif self.side == 1:
            return [self._makeAbsolute(vortex) for vortex in self._vertices[1]]
        else:
            return []

    @vertices.setter
    def vertices(self, value):
        self._vertices = value  # front and back

    # endregion

    # region get/set IO
    @property
    def IO(self):
        if self.side == 0:
            return [self._makeAbsolute(io) for io in self._IO[0]]
        elif self.side == 1:
            return [self._makeAbsolute(io) for io in self._IO[1]]
        else:
            return []

    @IO.setter
    def IO(self, value):
        self._IO = value  # front and back

    # endregion

    # region get/set size
    @property
    def size(self):
        if self.side == 1:
            return [self._makeAbsolute((-tile[0], tile[1])) for tile in self._size]
        else:
            return [self._makeAbsolute(tile) for tile in self._size]

    @size.setter
    def size(self, value):
        self._size = value

    # endregion

    # region get/set sides
    @property
    def sides(self):
        if self.id in SIDEABLE_IDS:
            return 3
        else:
            return 2

    # endregion


# model of the playing field


class Board:
    def __init__(self, fieldDict, pieces):
        # fieldDict - a dictionary/json object holding all the information about the level setup

        # level setup
        self.dimensions = tuple(
            2 * x for x in map(int, fieldDict["layout"].strip("()").split(","))
        )  # by the level required layout
        self.vertices = [
            tuple(map(int, s.strip("()").split(","))) for s in fieldDict["vertices"]
        ]  # by the level required vetices

        # keep track of the game
        self.matchedIO = []    # io-ports that are connected to another io-port
        self.unmatchedIO = []  # io-ports that are available for connection
        self.placedTiles = []  # array of all tiles that are covered by a piece
        self.freeTiles = [     # array of alll the not yet covered tiles
            (x, y)
            for x in range(1, self.dimensions[0] + 1, 2)
            for y in range(1, self.dimensions[1] + 1, 2)
        ]
        self.placedPieces = []  # array of pieces that are already places
        self.leftPieces = pieces  # array of pieces that havent been placed yet

    # adds the piece to the board
    def placePiece(self, piece: Piece) -> bool:
        # returns True if succesfull, False if not

        if not self.verify(piece):
            return False

        self.placedPieces.append(piece)
        self.leftPieces.remove(piece)

        # place tiles
        for tile in piece.size:
            self.placedTiles.append(tile)
            self.freeTiles.remove(tile)

        # place io
        for io in piece.IO:
            if io in self.unmatchedIO:
                self.matchedIO.append(io)
                self.unmatchedIO.remove(io)
            else:
                self.unmatchedIO.append(io)

        return True

    # removes the chronologically last placed piece from the board
    def removeLastPiece(self):

        if len(self.placedPieces) == 0:
            # theres no piece to remove
            return

        piece = self.placedPieces.pop()
        self.leftPieces.append(piece)

        # remove tiles
        for tile in piece.size:
            self.placedTiles.remove(tile)
            self.freeTiles.append(tile)

        # remove io
        for io in piece.IO:
            if io in self.matchedIO:
                self.matchedIO.remove(io)
                self.unmatchedIO.append(io)
            else:
                self.unmatchedIO.remove(io)

        return

    # a function used to verify, if a placed piece is gonna be legal
    def verify(self, piece: Piece) -> bool:

        if any(tile in self.placedTiles for tile in piece.size):
            # print("not a valid move. There are overlappinmg piecs")
            return False
        if any(tile[0] >= self.dimensions[0] or tile[1] >= self.dimensions[1] or tile[0] <= 0 or tile[1] <= 0 for tile in piece.size):
            # print("not a valid move. Youre venturing outside the board")
            return False
        if any(vortex not in self.vertices for vortex in piece.vertices):
            # print("not a valid move. Theres a vortex where it shouldnt")
            return False
        if any(vortex in piece.size and vortex not in piece.vertices for vortex in self.vertices):
            # print("not a valid move. There should be a vortex")
            return False
        for io in piece.IO:
            if (io[0] >= self.dimensions[0] or io[1] >= self.dimensions[1] or io[0] <= 0 or io[1] <= 0):
                # print("not a valid move. Your traces lead off the board")
                return False
            if (any(x in self.placedTiles for x in [(io[0] + 1, io[1]), (io[0] - 1, io[1]), (io[0], io[1] + 1), (io[0], io[1] - 1)]) and io not in self.unmatchedIO):
                # print("not a valid move. Your new placed trace cant connect here")
                return False
        for tile in piece.size:
            if any(x in self.unmatchedIO and x not in piece.IO for x in [(tile[0] + 1, tile[1]), (tile[0] - 1, tile[1]), (tile[0], tile[1] + 1), (tile[0], tile[1] - 1)]):
                # print("not a valid move. An existing trace cant connect to your piece")
                return False
        # checks that assume tile has been placed
        # the tiles that would be free if it is placed
        newFreeTiles = [x for x in self.freeTiles if x not in piece.size]
        newIO = self.unmatchedIO + piece.IO  # may contain duplicates
        if any(all(neighbour not in newFreeTiles for neighbour in [(tile[0] + 2, tile[1]), (tile[0] - 2, tile[1]), (tile[0], tile[1] + 2), (tile[0], tile[1] - 2)]) for tile in newFreeTiles):
            # print("not a valid move. Single isolated tile detected")
            return False

        while len(newFreeTiles) != 0:
            pocket, count = self.getPocket(
                newFreeTiles[0], newFreeTiles, newIO)
            if count["io"] % 2 != count["vertices"] % 2:
                # print("not a valid move. Impossible to fill isolated pocket detected")
                return False
            for tile in pocket:
                newFreeTiles.remove(tile)

        return True

    # Depth-First-Search
    # detects confined spaces of free tiles and counts the amount of io-ports into it and the amount of vertices inside
    def getPocket(self, start_tile, freeTiles, io):
        pocket = []
        count = {"io": 0, "vertices": 0}
        visited = set()

        def dfs(tile):
            if tile in visited or tile not in freeTiles:
                return

            # Mark tile as visited and add to pocket
            visited.add(tile)
            pocket.append(tile)

            # Check if current tile contains a vortex
            if tile in self.vertices:
                count["vertices"] += 1

            # Check surrounding tiles for markers (I/O ports)
            adjacent_tiles = [
                (tile[0] + 2, tile[1]),  # Right
                (tile[0] - 2, tile[1]),  # Left
                (tile[0], tile[1] + 2),  # Down
                (tile[0], tile[1] - 2),  # Up
            ]
            io_offsets = [
                (tile[0] + 1, tile[1]),  # Marker to the right
                (tile[0] - 1, tile[1]),  # Marker to the left
                (tile[0], tile[1] + 1),  # Marker down
                (tile[0], tile[1] - 1),  # Marker up
            ]

            # Explore adjacent free tiles
            for i, adj_tile in enumerate(adjacent_tiles):
                # Check for I/O ports (markers on adjacent tiles)
                if io_offsets[i] in io:
                    count["io"] += 1

                # Recursive DFS for free tiles
                if adj_tile in freeTiles and adj_tile[0] > 0 and adj_tile[1] > 0 and adj_tile[0] < self.dimensions[0] and adj_tile[1] < self.dimensions[0]:
                    dfs(adj_tile)

        # Start DFS from the start tile
        dfs(start_tile)

        return pocket, count
