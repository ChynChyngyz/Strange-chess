import pygame, os
from data.classes.Board import Board

pygame.init()

WINDOW_SIZE = (750, 750)
screen = pygame.display.set_mode(WINDOW_SIZE)
board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])


def draw(display):
    display.fill('white')
    board.draw(display)
    pygame.display.update()


running = True
while running:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.handle_click(mx, my)

    if board.is_in_checkmate('black'):
        print('White wins!')
        running = False
    elif board.is_in_checkmate('white'):
        print('Black wins!')
        running = False
    if board.game_result == "draw":
        print("The game ends in a draw!")
        os.startfile("C:\\Users\\Victus\\Desktop\\Царь Бомба _ Tsar Bomba (HD) ( звук).mp4")
        running = False

    draw(screen)
