# Import libraries/files
from pieces import Pieces
from PIL import Image, ImageDraw

class Board:
    def __init__(self):
        self.pieces = Pieces()
        # Default FEN
        self.import_from_fen("rnbqkbnr/pppppppp/8/8/8/N7/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.board = self.board[::-1]

        number_dictionary = [700, 600, 500, 400, 300, 200, 100, 0]


        print(self.board[2][0].color)
        moves = self.board[2][0].legal_moves(self.board)
        moves.append([2, 0])
        print(moves)
        rects = []
        for pos in moves:
            y, x = pos
            pos = [x * 100, number_dictionary[y]]
            rects.append((pos[0], pos[1], pos[0] + 100, pos[1] + 100))

        image = Image.open("resources/empty_board.png").convert('RGBA')
        draw = ImageDraw.Draw(image)
        for rect in rects:
            draw.rectangle(rect, fill=(255, 0 ,0))
        image.save("visual.png")


    # Import a game from a FEN
    def import_from_fen(self, fen):
        fields = fen.split(" ")

        self.set_board_from_fen(fields[0])
        self.turn = fields[1]
        
        self.set_castling_rights(fields[2])
        self.set_en_passant_right(fields[3])

        # Half moves, number since last capture or pawn advance
        # Increment after black's move
        self.half_moves = fields[4]

        # Total moves
        # Increment after black's move
        self.full_moves = fields[5]

    # To set up the board from the FEN field
    def set_board_from_fen(self, position):
        ranks = position.split("/")
        board = [["" for _ in range(8)] for _ in range(8)]
        
        for rank_index, Rank in enumerate(ranks):
            offset = 0
            for cell_index, cell in enumerate(Rank):
                if cell.isnumeric():
                    offset += int(cell) - 1
                
                else:
                    position = [rank_index, cell_index]
                    board[rank_index][cell_index + offset] = self.pieces.get_appropriate_piece(cell, position)

        self.board = board

    # To set the castling rights from the FEN field
    def set_castling_rights(self, string):
        for rank in self.board:
            for cell in rank:
                try:
                    if type(cell) is Pieces.King:
                        if cell.color == "white":
                            if "K" in string or string == "-":
                                cell.can_kingside_castle = False

                            if "Q" in string or string == "-":
                                cell.can_queenside_castle = False

                        if cell.color == "black":
                            if "k" in string or string == "-":
                                cell.can_kingside_castle = False

                            if "q" in string or string == "-":
                                cell.can_queenside_castle = False

                except AttributeError:
                    continue

    # To set En passant pawn from FEN field
    def set_en_passant_right(self, string):
        if string == "-":
            self.en_passant = False

        else:
            self.en_passant = string