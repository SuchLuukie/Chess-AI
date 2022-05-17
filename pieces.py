

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
            semi_legal_moves = [move for move in moves if move[0] in range(0, 7) and move[1] in range(0, 7)]
            semi_semi_legal_moves = [move for move in semi_legal_moves if board[move[0]][move[1]] != self.color]

            return semi_semi_legal_moves

    class Pawn:
        def __init__(self, color, position):
            self.color = color
            self.position = position
            self.value = 1
            self.en_passantable = False

            if self.color == "white": self.direction = 1
            else: self.direction = -1


            # Double pawn move info
            self.has_moved = False

        def check_for_en_passant(self, board):
            Rank, File = self.position
            en_passantable_cells = [[Rank, File-1], [Rank, File+1]]

            # Remove outside table
            en_passantable_cells = [move for move in en_passantable_cells if move[0] in range(0, 7) and move[1] in range(0, 7)]

            legal_en_passant = []
            for move in en_passantable_cells:
                Rank, File = move
                cell = board[Rank][File]
                if cell == "":
                    continue

                elif cell.color != self.color:
                    if cell.en_passantable:
                        legal_en_passant.append([move[0]+1*self.direction, move[1]])
            
            return legal_en_passant

        def check_for_captures(self, board):
            Rank, File = self.position
            captures = [
                [Rank+1*self.direction, File-1],
                [Rank+1*self.direction, File+1]
            ]
            captures = [move for move in captures if move[0] in range(0, 7) and move[1] in range(0, 7)]
            legal_captures = []

            for move in captures:
                Rank, File = move
                cell = board[Rank][File]
                
                if cell == "":
                    continue

                elif cell.color != self.color:
                    legal_captures.append(move)

            return legal_captures

        def legal_moves(self, board):
            Rank, File = self.position
            moves = [
                [Rank+1*self.direction, File]
            ]

            if not self.has_moved:
                moves.append([Rank+2*self.direction, File])

            moves = [move for move in moves if move[0] in range(0, 7) and move[1] in range(0, 7)]
            [moves.append(move) for move in self.check_for_en_passant(board)]
            [moves.append(move) for move in self.check_for_captures(board)]

            return moves