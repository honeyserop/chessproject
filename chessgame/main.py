import random
import pygame as p
import chessengine
import socket
class chess_game():
    def __init__(self,set):
        self.width = self.height = 512
        self.dimension = 8
        self.square_size = self.height // self.dimension
        self.MAX_FPS = 15
        self.images = {}
        self.set = set
        #self.set = set
        self.playerwhite = True
        self.otherplayer = False

    def send_color(self,sock):
        n = random.randint(0,1)
        if n == 0:
            sock.send(str(1).encode())
        if n == 0:
            sock.send(str(0).encode())

    def recv_color(self,sock):
        data = sock.recv(1024).decode()
        if data == "1":
            return 1
        if data == '0':
            return 0

    def send_move(self,sock,move):
        sock.send(move.chessnotation.encode())

    def recv_move(self,sock):
        data = sock.recv(1024).decode()
        return data
    def load_images(self):
        pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
        #setpicked = self.set
        for piece in pieces:
            try:
                self.images[piece] = p.transform.scale(p.image.load("images/" + self.set + piece + ".png"), (self.square_size, self.square_size))
            except:
                self.images[piece] = p.transform.scale(p.image.load("images/" + self.set + piece + ".png"),
                                                       (self.square_size, self.square_size))
    def main(self):
        p.init()
        screen = p.display.set_mode((self.width, self.height))
        clock = p.time.Clock()
        screen.fill(p.Color("blue"))
        state = chessengine.game_state(self.playerwhite)
        self.load_images()
        running = True
        valid_moves = state.get_checks()
        move_made = False
        animate = False
        sqr_selected = ()
        player_clicks = []
        game_over = False
        while running:
            for x in p.event.get():
                if x.type == p.QUIT:
                    running = False
                    p.display.quit()
                    p.quit()
                    break
                if x.type == p.MOUSEBUTTONDOWN:
                    if not game_over:

                        location = p.mouse.get_pos()
                        column = location[0] // self.square_size
                        row = location[1] // self.square_size
                        if sqr_selected == (row, column):
                            sqr_selected = ()
                            player_clicks = []
                        else:
                            sqr_selected = (row, column)
                            player_clicks.append(sqr_selected)
                            if len(player_clicks) == 2:
                                if self.playerwhite:
                                    move = chessengine.Movement(self.playerwhite, player_clicks[0], player_clicks[1], state.board)
                                else:
                                    move = chessengine.Movement(self.playerwhite, player_clicks[0], player_clicks[1], state.blackboard)
                                for i in range(len(valid_moves)):
                                    if move == valid_moves[i]:
                                        state.makemove(valid_moves[i])
                                        move_made = True
                                        animate = True
                                        print(move.chessnotation())
                                        print(move.blacktowhitemoveid())
                                        print(move.moveid)
                                        print(str(state.white_to_move))
                                        sqr_selected = ()
                                        player_clicks = []
                                if not move_made:
                                    player_clicks = [sqr_selected]

                elif x.type == p.KEYDOWN:
                    if x.key == p.K_z:
                        state.undo_move()
                        move_made = True
                        animate = False
                    if x.key == p.K_r:
                        state = chessengine.game_state(self.playerwhite,)
                        valid_moves = state.get_checks()
                        sqr_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
            if move_made:
                if animate:
                    self.animate_pieces(state.movelog[-1], screen, state, clock)
                valid_moves = state.get_checks()
                move_made = False
                animate = False
                if state.checkmate:
                    if state.white_to_move:
                        self.draw_text(screen, "Black wins by checkmate")
                        running = False
                    else:
                        self.draw_text(screen, "White wins by checkmate")
                        running = False
                if state.stalemate:
                    self.draw_text(screen, "Stalemate")
            p.display.flip()
            clock.tick(self.MAX_FPS)
            self.draw_board(state, screen, valid_moves, sqr_selected)
        p.display.quit()
        p.quit()

    def mainclient(self):
        p.init()
        screen = p.display.set_mode((self.width, self.height))
        clock = p.time.Clock()
        screen.fill(p.Color("blue"))
        state = chessengine.game_state(self.playerwhite)
        self.load_images()
        running = True
        valid_moves = state.get_checks()
        move_made = False
        animate = False
        sqr_selected = ()
        player_clicks = []
        game_over = False
        while running:
            for x in p.event.get():
                if x.type == p.QUIT:
                    running = False
                    p.display.quit()
                    p.quit()
                    break
                if x.type == p.MOUSEBUTTONDOWN:
                    if not game_over:
                        if state.white_to_move != self.otherplayer:
                            location = p.mouse.get_pos()
                            column = location[0] // self.square_size
                            row = location[1] // self.square_size
                            if sqr_selected == (row, column):
                                sqr_selected = ()
                                player_clicks = []
                            else:
                                sqr_selected = (row, column)
                                player_clicks.append(sqr_selected)
                                if len(player_clicks) == 2:
                                    if self.playerwhite:
                                        move = chessengine.Movement(self.playerwhite, player_clicks[0], player_clicks[1], state.board)
                                    else:
                                        move = chessengine.Movement(self.playerwhite, player_clicks[0], player_clicks[1], state.blackboard)
                                    for i in range(len(valid_moves)):
                                        if move == valid_moves[i]:
                                            state.makemove(valid_moves[i])
                                            move_made = True
                                            animate = True
                                            print(move.chessnotation())
                                            print(move.blacktowhitemoveid())
                                            print(move.moveid)
                                            print(str(state.white_to_move))
                                            sqr_selected = ()
                                            player_clicks = []
                                    if not move_made:
                                        player_clicks = [sqr_selected]
                        elif state.white_to_move == self.otherplayer:
                            state.white_to_move = not state.white_to_move
                            print(state.white_to_move)
                            break
                elif x.type == p.KEYDOWN:
                    if x.key == p.K_z:
                        state.undo_move()
                        move_made = True
                        animate = False
                    if x.key == p.K_r:
                        state = chessengine.game_state(self.playerwhite,)
                        valid_moves = state.get_checks()
                        sqr_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
            if move_made:
                if animate:
                    self.animate_pieces(state.movelog[-1], screen, state, clock)
                valid_moves = state.get_checks()
                move_made = False
                animate = False
                if state.checkmate:
                    if state.white_to_move:
                        self.draw_text(screen, "Black wins by checkmate")
                        running = False
                    else:
                        self.draw_text(screen, "White wins by checkmate")
                        running = False
                if state.stalemate:
                    self.draw_text(screen, "Stalemate")
            p.display.flip()
            clock.tick(self.MAX_FPS)
            self.draw_board(state, screen, valid_moves, sqr_selected)
        p.display.quit()
        p.quit()
    def mainserver(self):
        p.init()
        screen = p.display.set_mode((self.width, self.height))
        clock = p.time.Clock()
        screen.fill(p.Color("blue"))
        state = chessengine.game_state(self.playerwhite)
        self.load_images()
        running = True
        valid_moves = state.get_checks()
        move_made = False
        animate = False
        sqr_selected = ()
        player_clicks = []
        game_over = False
        server_socket = socket.socket()
        while running:
            for x in p.event.get():
                if x.type == p.QUIT:
                    running = False
                    p.display.quit()
                    p.quit()
                    break
                if x.type == p.MOUSEBUTTONDOWN:
                    if not game_over:
                        if state.white_to_move != self.otherplayer:
                            location = p.mouse.get_pos()
                            column = location[0] // self.square_size
                            row = location[1] // self.square_size
                            if sqr_selected == (row, column):
                                sqr_selected = ()
                                player_clicks = []
                            else:
                                sqr_selected = (row, column)
                                player_clicks.append(sqr_selected)
                                if len(player_clicks) == 2:
                                    if self.playerwhite:
                                        move = chessengine.Movement(self.playerwhite, player_clicks[0], player_clicks[1], state.board)
                                    else:
                                        move = chessengine.Movement(self.playerwhite, player_clicks[0], player_clicks[1], state.blackboard)
                                    for i in range(len(valid_moves)):
                                        if move == valid_moves[i]:
                                            state.makemove(valid_moves[i])
                                            move_made = True
                                            animate = True
                                            print(move.chessnotation())
                                            print(move.blacktowhitemoveid())
                                            print(move.moveid)
                                            print(str(state.white_to_move))
                                            sqr_selected = ()
                                            player_clicks = []
                                    if not move_made:
                                        player_clicks = [sqr_selected]
                        elif state.white_to_move == self.otherplayer:
                            state.white_to_move = not state.white_to_move
                            print(state.white_to_move)
                            break
                elif x.type == p.KEYDOWN:
                    if x.key == p.K_z:
                        state.undo_move()
                        move_made = True
                        animate = False
                    if x.key == p.K_r:
                        state = chessengine.game_state(self.playerwhite,)
                        valid_moves = state.get_checks()
                        sqr_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
            if move_made:
                if animate:
                    self.animate_pieces(state.movelog[-1], screen, state, clock)
                valid_moves = state.get_checks()
                move_made = False
                animate = False
                if state.checkmate:
                    if state.white_to_move:
                        self.draw_text(screen, "Black wins by checkmate")
                        running = False
                    else:
                        self.draw_text(screen, "White wins by checkmate")
                        running = False
                if state.stalemate:
                    self.draw_text(screen, "Stalemate")
            p.display.flip()
            clock.tick(self.MAX_FPS)
            self.draw_board(state, screen, valid_moves, sqr_selected)
        p.display.quit()
        p.quit()
    def draw_board(self, state, screen, valid_moves, sqr_selected):
        self.draw_screen(screen)
        self.highlight_squares(screen, state, valid_moves, sqr_selected)
        self.draw_pieces(screen, state)

    def draw_screen(self, screen):
        global colors
        if self.playerwhite:
            colors = (p.Color('white'), p.Color('grey'))
        else:
            colors = (p.Color('grey'), p.Color('white'))
        p.display.set_mode((self.width, self.height))
        for r in range(self.dimension):
            for c in range(self.dimension):
                color = colors[((r + c) % 2)]
                p.draw.rect(screen, color, p.Rect(c*self.square_size, r*self.square_size, self.square_size, self.square_size))

    def draw_pieces(self,screen, state):
        if self.playerwhite:
            lst = state.board
        else:
            lst = state.blackboard
        for r in range(self.dimension):
            for c in range(self.dimension):
                pieces = lst[r][c]
                if pieces != '--':
                    screen.blit(self.images[pieces], p.Rect(c*self.square_size, r*self.square_size, self.square_size, self.square_size))

    def highlight_squares(self, screen, state, valid_moves, sqr_selected):
        if sqr_selected != ():
            r, c = sqr_selected
            if self.playerwhite:
                if state.screen[r][c][0] == ('w' if state.white_to_move else 'b'):
                    highlight = p.Surface((self.square_size, self.square_size))
                    highlight.set_alpha(100)
                    highlight.fill(p.Color('yellow'))
                    screen.blit(highlight, (c*self.square_size, r*self.square_size))
                    highlight.fill(p.Color('red'))
                    for move in valid_moves:
                        if move.startrow == r and move.startcolumn == c:
                            screen.blit(highlight, (move.endcolumn * self.square_size, move.endrow * self.square_size))
            else:
                if state.screen[r][c][0] == ('w' if state.white_to_move else 'b'):
                    highlight = p.Surface((self.square_size, self.square_size))
                    highlight.set_alpha(100)
                    highlight.fill(p.Color('yellow'))
                    screen.blit(highlight, (c*self.square_size, r*self.square_size))
                    highlight.fill(p.Color('red'))
                    for move in valid_moves:
                        if move.startrow == r and move.startcolumn == c:
                            screen.blit(highlight, (move.endcolumn * self.square_size, move.endrow * self.square_size))

    def animate_pieces(self, move, screen, state, clock):
        global colors
        h_distance = move.endcolumn - move.startcolumn
        v_distance = move.endrow - move.startrow
        framepersquare = 10
        framecount = (abs(h_distance) + abs(v_distance)) * framepersquare
        for frame in range(framecount + 1):
            r, c = (move.startrow + v_distance * frame/framecount, move.startcolumn + h_distance * frame/framecount)
            self.draw_screen(screen)
            self.draw_pieces(screen, state)
            color = colors[(move.endrow + move.endcolumn) % 2]
            end_square = p.Rect(move.endcolumn * self.square_size, move.endrow * self.square_size, self.square_size, self.square_size)
            p.draw.rect(screen, color, end_square)
            if move.piececaptured != "--":
                screen.blit(self.images[move.piececaptured], end_square)
            screen.blit(self.images[move.piecemoved], p.Rect(c * self.square_size, r * self.square_size, self.square_size, self.square_size))
            p.display.flip()
            clock.tick(60)

    def draw_text(self, screen, text):
        font = p.font.SysFont("helvetica", 32, True, False)
        text_object = font.render(text, 0, p.Color("black"))
        text_location = p.Rect(0, 0, self.width, self.height).move(self.width/2 - text_object.get_width()/2, self.height/2 - text_object.get_height()/2)
        screen.blit(text_object, text_location)
        text_object = font.render(text, 0, p.Color("gray"))
        screen.blit(text_object, text_location.move(2, 2))


def main():
    game = chess_game()
    game.main()


if __name__ == '__main__':
    main()
