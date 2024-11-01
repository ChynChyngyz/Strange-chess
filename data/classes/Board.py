from data.classes.Square import Square
from data.classes.pieces.Nuclear import Nuclear
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Duck import Duck
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Dragon import Dragon
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn


class Board:
    def __init__(self, width, height):
        self.game_result = None
        self.width = width
        self.height = height
        self.pieces = []
        self.square_width = width // 8
        self.square_height = height // 8
        self.selected_piece = None
        self.turn = 'white'

        self.config = [
            ['bR', 'bG', 'bB', 'bQ', 'bK', 'bD', 'bN', 'bR'],
            ['b ', 'b ', 'b ', 'b ', 'b ', 'b ', 'b ', 'bA'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['w ', 'w ', 'w ', 'w ', 'w ', 'w ', 'w ', 'wA'],
            ['wR', 'wG', 'wB', 'wQ', 'wK', 'wD', 'wN', 'wR'],
        ]

        self.squares = self.generate_squares()

        self.setup_board()

    def generate_squares(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(
                        x,
                        y,
                        self.square_width,
                        self.square_height
                    )
                )

        return output

    def setup_board(self):
        global piece_instance
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = self.get_square_from_pos((x, y))

                    if piece[1] == 'R':
                        piece_instance = Rook((x, y), 'white' if piece[0] == 'w' else 'black', self)

                    elif piece[1] == 'N':
                        piece_instance = Knight((x, y), 'white' if piece[0] == 'w' else 'black', self)

                    elif piece[1] == 'B':
                        piece_instance = Bishop((x, y), 'white' if piece[0] == 'w' else 'black', self)

                    elif piece[1] == 'A':
                        piece_instance = Nuclear((x, y), 'white' if piece[0] == 'w' else 'black', self)

                    elif piece[1] == 'G':
                        piece_instance = Duck((x, y), 'white' if piece[0] == 'w' else 'black', self)

                    elif piece[1] == 'D':
                        piece_instance = Dragon((x, y), 'white' if piece[0] == 'w' else 'black', self)

                    elif piece[1] == 'Q':
                        piece_instance = Queen((x, y), 'white' if piece[0] == 'w' else 'black', self)

                    elif piece[1] == 'K':
                        piece_instance = King((x, y), 'white' if piece[0] == 'w' else 'black', self)

                    elif piece[1] == ' ':
                        piece_instance = Pawn((x, y), 'white' if piece[0] == 'w' else 'black', self)

                    square.occupying_piece = piece_instance
                    self.pieces.append(piece_instance)

    def handle_click(self, mx, my):
        x = mx // self.square_width
        y = my // self.square_height
        clicked_square = self.get_square_from_pos((x, y))

        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece

        elif self.selected_piece.move(self, clicked_square):
            self.turn = 'white' if self.turn == 'black' else 'black'

        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece

    def is_in_check(self, color, board_change=None):  # board_change = [(x1, y1), (x2, y2)]
        output = False
        king_pos = None

        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None

        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece

        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]

        if changing_piece is not None:
            if changing_piece.notation == 'K':
                king_pos = new_square.pos
        if king_pos is None:
            for piece in pieces:
                if piece.notation == 'K':
                    if piece.color == color:
                        king_pos = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True

        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece

        return output

    def switch(self, square):
        attacked_piece = square.occupying_piece
        if isinstance(attacked_piece, Dragon):
            self.turn = 'black' if self.turn == 'white' else 'white'

    def is_in_checkmate(self, color):
        global king
        output = False

        for piece in [i.occupying_piece for i in self.squares]:
            if piece is not None:
                if piece.notation == 'K' and piece.color == color:
                    king = piece

        if not king.get_valid_moves(self):
            if self.is_in_check(color):
                output = True

        return output

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)
            for square in self.squares:
                if square.occupying_piece == piece:
                    square.occupying_piece = None
                    break
        else:
            print(f"Attempted to remove a piece that is not in the list: {piece}")

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece

    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True

        for square in self.squares:
            square.draw(display)
