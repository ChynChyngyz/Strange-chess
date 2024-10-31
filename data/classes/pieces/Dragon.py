import pygame
from data.classes.Piece import Piece


class Dragon(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        img_path = 'data/images/' + color[0] + '_dragon.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.square_width - 5, board.square_height - 5))

        self.notation = 'D'

    def get_possible_moves(self, board):
        moves = [
            (0, -1), (0, -2), (1, -2),
            (1, -1), (2, -2), (-2, 1),
            (1, 0), (2, 0), (-1, -2),
            (1, 1), (2, 2), (2, 1),
            (0, 1), (0, 2), (1, 2),
            (-1, 1), (-2, 2), (-2, -1),
            (-1, 0), (-2, 0), (2, -1),
            (-1, -1), (-2, -2), (-1, 2),
        ]

        output = [
            [board.get_square_from_pos((self.x + dx, self.y + dy))]
            for dx, dy in moves
            if 0 <= self.x + dx < 8 and 0 <= self.y + dy < 8
        ]

        return output
