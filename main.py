import pygame as p
from chessgame import chessengine

width = height = 512
dimension = 8
square_size = height // dimension
MAX_FPS = 15
images = {}


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (square_size, square_size))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    screen.fill(p.Color("blue"))
    state = chessengine.game_state()
    load_images()
    running = True
    valid_moves = state.get_checks()
    move_made = False
    sqr_selected = ()
    player_clicks = []
    while running:
        for x in p.event.get():
            if x.type == p.quit:
                running = False
            elif x.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                column = location[0]//square_size
                row = location[1] // square_size
                if sqr_selected == (row, column):
                    sqr_selected = ()
                    player_clicks = []
                else:
                    sqr_selected = (row, column)
                    player_clicks.append(sqr_selected)
                    if len(player_clicks) == 2:
                        move = chessengine.Movement(player_clicks[0], player_clicks[1], state.board)
                        if move in valid_moves:
                            state.makemove(move)
                            move_made = True
                            print(move.chessnotation())
                            sqr_selected = ()
                            player_clicks = []
                        else:
                            player_clicks = [sqr_selected]
            elif x.type == p.KEYDOWN:
                if x.key == p.K_z:
                    state.undo_move()
                    move_made = True

        if move_made:
            valid_moves = state.get_checks()
            move_made = False
        p.display.flip()
        draw_board(state, screen)


def draw_board(state, screen):
    draw_screen(screen)
    draw_pieces(screen, state)


def draw_screen(screen):
    colors = (p.Color('white'), p.Color('grey'))
    p.display.set_mode((width, height))
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*square_size, r*square_size, square_size, square_size))


def draw_pieces(screen, state):
    for r in range(dimension):
        for c in range(dimension):
            lst = state.board
            line = lst[r]
            pieces = line[c]
            if pieces != '--':
                screen.blit(images[pieces], p.Rect(c*square_size, r*square_size, square_size, square_size))


if __name__ == '__main__':
    main()
