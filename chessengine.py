class game_state:
    def __init__(self):  # the first letter indicates the colour of the piece#
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "wB", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.white_to_move = True
        self.movelog = []
        self.whitekinglocation = (7, 4)
        self.blackkinglocation = (0, 4)


    def get_board(self):
        return self.board

    def makemove(self, movement):
        self.board[movement.startrow][movement.startcolumn] = "--"
        self.board[movement.endrow][movement.endcolumn] = movement.piecemoved
        self.movelog.append(movement)
        self.white_to_move = not self.white_to_move
        if movement.piecemoved == 'wK':
            self.whitekinglocation = (movement.endrow, movement.endcolumn)
        if movement.piecemoved == 'bK':
            self.blackkinglocation = (movement.endrow, movement.endcolumn)

    def undo_move(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startrow][move.startcolumn] = move.piecemoved
            self.board[move.endrow][move.endcolumn] = move.piececaptured
            self.white_to_move = not self.white_to_move
            if Movement.piecemoved == 'wK':
                self.whitekinglocation =(Movement.startrow, Movement.startcolumn)
            if Movement.piecemoved == 'bK':
                self.blackkinglocation = (Movement.endrow, Movement.endcolumn)

    def get_checks(self):  # checks using get_possible_moves a valid to do with king in #
        moves = self.get_possible_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.makemove(moves(i))
        return moves
    def in_check(self):
        if self.white_to_move:
            return self.square_attacked(self.whitekinglocation[0], self.whitekinglocation[1])
        if not self.white_to_move:
            return self.square_attacked(self.blackkinglocation[0], self.blackkinglocation[1])

    def square_attacked(self, r, c):
        self.white_to_move = not self.white_to_move
        oppmoves = self.get_possible_moves()
        for move in oppmoves:
            if move.endrow == r and move.endcolumn == c:
                pass

    def get_possible_moves(self):  # checks for all possible player moves #
        allmoves = []
        while True:
            for r in range(len(self.board)):
                for c in range(len(self.board[r])):
                    turn = self.board[r][c][0]
                    if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                        piece = self.board[r][c][1]
                        if piece == 'p':
                            self.getpawnmoves(r, c, allmoves)
                        if piece == 'R':
                            self.getrookmoves(r, c, allmoves)
                        if piece == 'B':
                            self.getbishopmoves(r, c, allmoves)
                        if piece == 'N':
                            self.getknightmoves(r, c, allmoves)
                        if piece == 'Q':
                            self.getqueenmoves(r, c, allmoves)
                        if piece == 'K':
                            self.getkingmoves(r, c, allmoves)
            return allmoves

    def getrookmoves(self, r, c, allmoves):
        directions = ((-1, 0), (1, 0), (0, 1), (0, -1))
        enemycolor = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endpiece = self.board[endrow][endcol]
                    if endpiece == "--":
                        allmoves.append(Movement((r, c), (endrow, endcol), self.board))
                    elif endpiece[0] == enemycolor:
                        allmoves.append(Movement((r, c), (endrow, endcol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getpawnmoves(self, r, c, allmoves):
        if self.white_to_move:
            if self.board[r - 1][c] == "--":
                allmoves.append(Movement((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    allmoves.append(Movement((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    allmoves.append(Movement((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    allmoves.append(Movement((r, c), (r - 1, c + 1), self.board))
        if not self.white_to_move:
            if self.board[r + 1][c] == "--":
                allmoves.append(Movement((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    allmoves.append(Movement((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    allmoves.append(Movement((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    allmoves.append(Movement((r, c), (r + 1, c + 1), self.board))

    def getkingmoves(self, r, c, allmoves):
        if r + 1 <= 7:
            if self.board[r + 1][c] == '--' or self.board[r + 1][c][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r,c), (r + 1,c), self.board))
        if r - 1 >= 0:
            if self.board[r - 1][c] == '--' or self.board[r - 1][c][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r,c), (r - 1,c), self.board))
        if c + 1 <= 7:
            if self.board[r][c + 1] == '--' or self.board[r][c + 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r,c), (r,c + 1), self.board))
        if c - 1 >= 0:
            if self.board[r][c - 1] == '--' or self.board[r][c - 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r,c), (r,c - 1), self.board))
        if r + 1 <= 7 and c + 1 <= 7:
            if self.board[r + 1][c + 1] == '--' or self.board[r + 1][c + 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r,c), (r + 1,c + 1), self.board))
        if r + 1 <= 7 and c - 1 >= 0:
            if self.board[r + 1][c - 1] == '--' or self.board[r + 1][c - 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r,c), (r + 1,c - 1), self.board))
        if r - 1 >= 0 and c + 1 <= 7:
            if self.board[r - 1][c + 1] == '--' or self.board[r - 1][c + 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r,c), (r - 1,c + 1), self.board))
        if r - 1 >= 0 and c - 1 >= 0:
            if self.board[r - 1][c - 1] == '--' or self.board[r - 1][c - 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r, c), (r - 1, c - 1), self.board))

    def getknightmoves(self, r, c, allmoves):
        l = 1
        o = 2
        if r + o <= 7 and c + l <= 7:
            if self.board[r + o][c + l] == '--' or self.board[r + o][c + l][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r, c), (r + o, c + l), self.board))
        if r + o <= 7 and c - l >= 0:
            if self.board[r + o][c - l] == '--' or self.board[r + o][c - l][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r, c), (r + o, c - l), self.board))
        if r - o >= 0 and c + l <= 7:
            if self.board[r - o][c + l] == '--' or self.board[r - o][c + l][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r, c), (r - o, c + l), self.board))
        if r - o >= 0 and c - l >= 0:
            if self.board[r - o][c - l] == '--' or self.board[r - o][c - l][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r, c), (r - o, c - l), self.board))
        if r + l <= 7 and c + o <= 7:
            if self.board[r + l][c + o] == '--' or self.board[r + l][c + o][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r, c), (r + l, c + o), self.board))
        if r + l <= 7 and c - o >= 0:
            if self.board[r + l][c - o] == '--' or self.board[r + l][c - o][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r, c), (r + l, c - o), self.board))
        if r - l >= 0 and c + o <= 7:
            if self.board[r - l][c + o] == '--' or self.board[r - l][c + o][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r, c), (r - l, c + o), self.board))
        if r - l >= 0 and c - o >= 0:
            if self.board[r - l][c - o] == '--' or self.board[r - l][c - o][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement((r, c), (r - l, c - o), self.board))

    def getqueenmoves(self, r, c, allmoves):
        self.getrookmoves(r, c, allmoves)
        self.getbishopmoves(r, c, allmoves)

    def getbishopmoves(self, r, c, allmoves):
        directions = ((-1, -1), (1, 1), (-1, 1), (1, -1))
        enemycolor = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endpiece = self.board[endrow][endcol]
                    if endpiece == "--":
                        allmoves.append(Movement((r, c), (endrow, endcol), self.board))
                    elif endpiece[0] == enemycolor:
                        allmoves.append(Movement((r, c), (endrow, endcol), self.board))
                        break
                    else:
                        break
                else:
                    break


class Movement:
    def __init__(self, start, end, board):
        self.startrow = start[0]
        self.startcolumn = start[1]
        self.endrow = end[0]
        self.endcolumn = end[1]
        self.piecemoved = board[self.startrow][self.startcolumn]
        self.piececaptured = board[self.endrow][self.endcolumn]
        self.moveid = self.startrow * 1000 + self.startcolumn * 100 + self.endrow * 10 + self.endcolumn

    ranktorows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rowstoranks = {v: k for k, v in ranktorows.items()}
    filestocols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colstofiles = {v: k for k, v in filestocols.items()}

    def chessnotation(self):
        return self.rankfile(self.startrow, self.startcolumn) + self.rankfile(self.endrow, self.endcolumn)

    def rankfile(self, c, r):
        return self.colstofiles[c] + self.rowstoranks[r]

    def __eq__(self, other):
        if isinstance(other, Movement):
            return self.moveid == other.moveid
        return False
