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
        random_number = None

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
                (1, -1), (1, 1),
            ]

        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if 0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8:
                square = board.get_square_from_pos(new_pos)
                if square.is_occupied() and square.get_piece().color != self.color:
                    output.append([
                        board.get_square_from_pos(new_pos)
                    ])
                if square.is_occupied() and square.get_piece().color == self.color:
                    jump_pos = (self.x + move[0] // 2, self.y + move[1] // 2)
                    jump_square = board.get_square_from_pos(jump_pos)
                    if jump_square.is_empty() and not self.jumped:
                        output.append([square])
                        random_number = random.randint(1, 6)
                        self.jumped = True

                        if random_number % 2 == 0:
                            piece_to_eat = square.get_piece()
                            board.remove_piece(piece_to_eat)
                            print("Piece eaten")

                elif square.is_empty():
                    output.append([square])

        if self.jumped and random_number is not None:
            print(f"Jumped over a piece! Random number: {random_number}")

        return output
