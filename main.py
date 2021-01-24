import pygame as p
from chessgame import chessengine

width = height = 512
dimension = 8
square_size = height // dimension
images = {}


def load_images():

    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'BQ', 'bK']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (square_size, square_size))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    screen.fill(p.Color("white"))
    state = chessengine.gamestate()
    load_images()
    print(state.board)


if __name__ == '__main__':
    main()