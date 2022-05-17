

class Pieces:
    def __init__(self):
        self.pieces_dictionary = {
            "k": self.King,
            "q": self.Queen,
            "r": self.Rook,
            "b": self.Bishop,
            "n": self.Knight,
            "p": self.Pawn
        }

    # Returns appropriate piece class
    def get_appropriate_piece(self, string, position):
        if string.isupper(): color = "white"
        else: color = "black"

        return self.pieces_dictionary[string.lower()](color, position)

    class King:
        def __init__(self, color, position):
            self.color = color
            self.position = position
            self.value = float("inf")

            # Castling info
            self.has_moved = False
            self.can_kingside_castle = True
            self.can_queenside_castle = True

    class Queen:
        def __init__(self, color, position):
            self.color = color
            self.position = position
            self.value = 9.5

    class Rook:
        def __init__(self, color, position):
            self.color = color
            self.position = position
            self.value = 5.63

            # Castling info
            self.has_moved = False

    class Bishop:
        def __init__(self, color, position):
            self.color = color
            self.position = position
            self.value = 3.33

    class Knight:
        def __init__(self, color, position):
            self.color = color
            self.position = position
            self.value = 3.05
        
        def moves(self):
            Rank, File = self.position
            return [
                [Rank+2, File-1],
                [Rank+2, File+1],
                [Rank+1, File+2],
                [Rank-1, File+2],
                [Rank-2, File+1],
                [Rank-2, File-1],
                [Rank-1, File-2],
                [Rank+1, File-2]
            ]

        def legal_moves(self, board):
            moves = self.moves()
            semi_legal_moves = [move for move in moves if move[0] in range(0, 8) and move[1] in range(0, 8)]

            return semi_legal_moves

    class Pawn:
        def __init__(self, color, position):
            self.color = color
            self.position = position
            self.value = 1

            # Double pawn move info
            self.has_moved = False