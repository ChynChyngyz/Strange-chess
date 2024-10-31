import pygame
import random
from data.classes.Piece import Piece


class Duck(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        img_path = 'data/images/' + color[0] + '_duck.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.square_width - 20, board.square_height - 20))

        self.notation = 'G'
        self.jumped = False

    def get_possible_moves(self, board):
        output = []

        if self.color == 'white':
            moves = [
                (2, 0), (-2, 0),
                (0, -2), (-1, 1),
                (-1, -1), (1, -1),
            ]
        else:  # черный гусь
            moves = [
                (2, 0), (0, 2),
                (-2, 0), (-1, 1),
                (1, -1),  (1, 1),
            ]

        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if 0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8:
                square = board.get_square_from_pos(new_pos)
                output.append([square])

        return output

    def move(self, board, square, force=False):
        prev_square = board.get_square_from_pos(self.pos)

        if abs(self.x - square.x) == 2 or abs(self.y - square.y) == 2:
            middle_x = (self.x + square.x) // 2
            middle_y = (self.y + square.y) // 2
            middle_square = board.get_square_from_pos((middle_x, middle_y))

            if middle_square.is_occupied() and middle_square.get_piece().color == self.color:
                random_number = random.randint(1, 6)
                print(f"Random number: {random_number}")

                if random_number % 2 == 0:
                    piece_to_eat = middle_square.get_piece()
                    board.remove_piece(piece_to_eat)
                    print("Own piece eaten")

        for i in board.squares:
            i.highlight = False
        self.pos, self.x, self.y = square.pos, square.x, square.y
        prev_square.occupying_piece = None
        square.occupying_piece = self
        self.has_moved = True
        board.selected_piece = None
        return True
