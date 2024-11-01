import pygame

from data.classes.Piece import Piece


class Nuclear(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.lives = 1

        img_path = 'data/images/' + color[0] + '_nuclear.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.square_width - 20, board.square_height - 20))

        self.notation = 'A'

    def eat_nuclear(self):
        self.lives -= 1
        print(f'Lives {self.lives}')
        if self.lives <= 0:
            return True
        return False

    def get_possible_moves(self, board):
        output = []
        moves = [
            (0, -1), (1, -1),
            (1, 0), (1, 1),
            (0, 1), (-1, 1),
            (-1, 0), (-1, -1),
        ]

        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if (
                    (new_pos[0] < 8) and (new_pos[0] >= 0) and (new_pos[1] < 8) and (new_pos[1] >= 0)
            ):
                output.append([
                    board.get_square_from_pos(new_pos)
                ])

        return output
