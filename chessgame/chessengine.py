class game_state:
    def __init__(self,playerwhite):# the first letter indicates the colour of the piece#
        self.playerwhite = playerwhite
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.blackboard = [
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]]
        if playerwhite:
            self.screen = self.board
        else:
            self.screen = self.blackboard
        self.white_to_move = True
        self.movelog = []
        self.whitekinglocation = (7, 4)
        self.blackkinglocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassant_possible = ()  # coordinates for the square where en-passant capture is possible
        self.enpassant_possible_log = [self.enpassant_possible]
        self.currentpossiblecastling = castle_types(True, True, True, True)
        self.castlelog = [self.currentpossiblecastling]
        self.copycastlelog = [castle_types(self.currentpossiblecastling.whitequeenside, self.currentpossiblecastling.whitekingside,
                                           self.currentpossiblecastling.blackqueenside, self.currentpossiblecastling.blackkingside)]

    def get_board(self, playerwhite):
        if playerwhite:
            return self.board
        return self.blackboard

    def makemove(self, Movement):
        self.screen[Movement.startrow][Movement.startcolumn] = "--"
        self.screen[Movement.endrow][Movement.endcolumn] = Movement.piecemoved
        self.movelog.append(Movement)
        self.white_to_move = not self.white_to_move
        if Movement.piecemoved == 'wK':
            self.whitekinglocation = (Movement.endrow, Movement.endcolumn)
        if Movement.piecemoved == 'bK':
            self.blackkinglocation = (Movement.endrow, Movement.endcolumn)
        if Movement.pawnpromotion:
            self.screen[Movement.endrow][Movement.endcolumn] = Movement.piecemoved[0] + "Q"
        if Movement.is_enpassant_move:
            self.screen[Movement.startrow][Movement.endcolumn] = "--"
        if Movement.piecemoved[1] == "p" and abs(Movement.startrow - Movement.endrow) == 2:  # only on 2 square pawn advance
            self.enpassant_possible = ((Movement.startrow + Movement.endrow) // 2, Movement.startcolumn)
        else:
            self.enpassant_possible = ()
        self.enpassant_possible_log.append(self.enpassant_possible)
        if Movement.castle:
            if Movement.endcolumn - Movement.startcolumn == 2:
                self.screen[Movement.endrow][Movement.endcolumn - 1] = self.screen[Movement.endrow][Movement.endcolumn+1]
                self.screen[Movement.endrow][Movement.endcolumn + 1] = "--"
            else:
                self.screen[Movement.endrow][Movement.endcolumn + 1] = self.screen[Movement.endrow][
                    Movement.endcolumn - 2]
                self.screen[Movement.endrow][Movement.endcolumn - 2] = "--"

        self.updatecastlemoves(Movement)
        self.castlelog.append(castle_types(self.currentpossiblecastling.whitequeenside, self.currentpossiblecastling.whitekingside,
                                           self.currentpossiblecastling.blackqueenside, self.currentpossiblecastling.blackkingside))
        #self.castlelog.append(self.copycastlelog)
    
    def undo_move(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.screen[move.startrow][move.startcolumn] = move.piecemoved
            self.screen[move.endrow][move.endcolumn] = move.piececaptured
            self.white_to_move = not self.white_to_move
            if move.piecemoved == 'wK':
                self.whitekinglocation = (move.startrow, move.startcolumn)
            elif move.piecemoved == 'bK':
                self.blackkinglocation = (move.startrow, move.startcolumn)

            if move.is_enpassant_move:
                self.screen[move.endrow][move.endcolumn] = "--"  # leave landing square blank
                self.screen[move.startrow][move.endcolumn] = move.piececaptured

            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]

            self.castlelog.pop()
            self.currentpossiblecastling.whitequeenside, self.currentpossiblecastling.whitekingside, self.currentpossiblecastling.blackqueenside\
                , self.currentpossiblecastling.blackkingside =self.castlelog[-1].whitequeenside, self.castlelog[-1].whitekingside\
                , self.castlelog[-1].blackqueenside, self.castlelog[-1].blackkingside,
            if move.castle:
                if move.endcolumn - move.startcolumn == 2:
                    self.screen[move.endrow][move.endcolumn + 1] = self.screen[move.endrow][
                        move.endcolumn - 1]
                    self.screen[move.endrow][move.endcolumn - 1] = "--"
                else:
                    self.screen[move.endrow][move.endcolumn - 2] = self.screen[move.endrow][
                        move.endcolumn + 1]
                    self.screen[move.endrow][move.endcolumn + 1] = "--"

    def updatecastlemoves(self, move):
        if move.piecemoved == 'wK':
            self.currentpossiblecastling.whitekingside = False
            self.currentpossiblecastling.whitequeenside = False
        elif move.piecemoved == 'bK':
            self.currentpossiblecastling.blackkingside = False
            self.currentpossiblecastling.blackqueenside = False
        elif move.piecemoved == 'wR' and move.startrow == 7:
            if move.startcolumn == 0:
                self.currentpossiblecastling.whitequeenside = False
            elif move.startcolumn == 7:
                self.currentpossiblecastling.whitekingside = False
        elif move.piecemoved == 'bR' and move.startrow == 0:
            if move.startcolumn == 0:
                self.currentpossiblecastling.blackqueenside = False
            elif move.startcolumn == 7:
                self.currentpossiblecastling.blackkingside = False

    def get_checks(self):  # checks using get_possible_moves a valid to do with king in #
        store_white_to_move = self.white_to_move
        tempcastlerights = castle_types(self.currentpossiblecastling.whitequeenside, self.currentpossiblecastling.whitekingside
                                        , self.currentpossiblecastling.blackqueenside, self.currentpossiblecastling.blackkingside)
        moves = self.get_possible_moves()
        if self.white_to_move:
            self.get_castlemoves(self.whitekinglocation[0], self.whitekinglocation[1], moves)
        else:
            self.get_castlemoves(self.blackkinglocation[0], self.blackkinglocation[1], moves)
        for i in range(len(moves) - 1, -1, -1):
            self.makemove(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.currentpossiblecastling = tempcastlerights
        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_attacked(self.whitekinglocation[0], self.whitekinglocation[1])
        if not self.white_to_move:
            return self.square_attacked(self.blackkinglocation[0], self.blackkinglocation[1])

    def square_attacked(self, r, c):
        self.white_to_move = not self.white_to_move
        oppmoves = self.get_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in oppmoves:
            if move.endrow == r and move.endcolumn == c:
                return True
        return False

    def get_possible_moves(self):  # checks for all possible player moves #
        allmoves = []
        while True:
            for r in range(len(self.screen)):
                for c in range(len(self.screen[r])):
                    turn = self.screen[r][c][0]
                    if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                        piece = self.screen[r][c][1]
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
                    endpiece = self.screen[endrow][endcol]
                    if endpiece == "--":
                        allmoves.append(Movement(self.playerwhite,(r, c), (endrow, endcol), self.screen))
                    elif endpiece[0] == enemycolor:
                        allmoves.append(Movement(self.playerwhite,(r, c), (endrow, endcol), self.screen))
                        break
                    else:
                        break
                else:
                    break

    def getpawnmoves(self, r, c, allmoves):
        if self.playerwhite:
            if self.white_to_move:

                if self.screen[r - 1][c] == "--":
                    allmoves.append(Movement(self.playerwhite, (r, c), (r - 1, c), self.screen))
                    if r == 6 and self.screen[r - 2][c] == "--":
                        allmoves.append(Movement(self.playerwhite, (r, c), (r - 2, c), self.screen))
                if c - 1 >= 0:
                    if self.screen[r - 1][c - 1][0] == 'b':
                        allmoves.append(Movement(self.playerwhite, (r, c), (r - 1, c - 1), self.screen))
                    elif (r - 1, c - 1) == self.enpassant_possible:
                        allmoves.append(
                            Movement(self.playerwhite, (r, c), (r - 1, c - 1), self.screen, is_enpassant_move=True))
                if c + 1 <= 7:
                    if self.screen[r - 1][c + 1][0] == 'b':
                        allmoves.append(Movement(self.playerwhite, (r, c), (r - 1, c + 1), self.screen))
                    elif (r - 1, c + 1) == self.enpassant_possible:
                        allmoves.append(
                            Movement(self.playerwhite, (r, c), (r - 1, c + 1), self.screen, is_enpassant_move=True))
            if not self.white_to_move:
                if self.screen[r + 1][c] == "--":
                    allmoves.append(Movement(self.playerwhite, (r, c), (r + 1, c), self.screen))
                    if r == 1 and self.screen[r + 2][c] == "--":
                        allmoves.append(Movement(self.playerwhite, (r, c), (r + 2, c), self.screen))
                if c - 1 >= 0:
                    if self.screen[r + 1][c - 1][0] == 'w':
                        allmoves.append(Movement(self.playerwhite, (r, c), (r + 1, c - 1), self.screen))
                    elif (r + 1, c - 1) == self.enpassant_possible:
                        allmoves.append(
                            Movement(self.playerwhite, (r, c), (r + 1, c - 1), self.screen, is_enpassant_move=True))
                if c + 1 <= 7:
                    if self.screen[r + 1][c + 1][0] == 'w':
                        allmoves.append(Movement(self.playerwhite, (r, c), (r + 1, c + 1), self.screen))
                    elif (r + 1, c + 1) == self.enpassant_possible:
                        allmoves.append(
                            Movement(self.playerwhite, (r, c), (r + 1, c + 1), self.screen, is_enpassant_move=True))
        else:
            if not self.white_to_move:

                if self.screen[r - 1][c] == "--":
                    allmoves.append(Movement(self.playerwhite, (r, c), (r - 1, c), self.screen))
                    if r == 6 and self.screen[r - 2][c] == "--":
                        allmoves.append(Movement(self.playerwhite, (r, c), (r - 2, c), self.screen))
                if c - 1 >= 0:
                    if self.screen[r - 1][c - 1][0] == 'w':
                        allmoves.append(Movement(self.playerwhite, (r, c), (r - 1, c - 1), self.screen))
                    elif (r - 1, c - 1) == self.enpassant_possible:
                        allmoves.append(
                            Movement(self.playerwhite, (r, c), (r - 1, c - 1), self.screen, is_enpassant_move=True))
                if c + 1 <= 7:
                    if self.screen[r - 1][c + 1][0] == 'w':
                        allmoves.append(Movement(self.playerwhite, (r, c), (r - 1, c + 1), self.screen))
                    elif (r - 1, c + 1) == self.enpassant_possible:
                        allmoves.append(
                            Movement(self.playerwhite, (r, c), (r - 1, c + 1), self.screen, is_enpassant_move=True))
            if self.white_to_move:
                if self.screen[r + 1][c] == "--":
                    allmoves.append(Movement(self.playerwhite, (r, c), (r + 1, c), self.screen))
                    if r == 1 and self.screen[r + 2][c] == "--":
                        allmoves.append(Movement(self.playerwhite, (r, c), (r + 2, c), self.screen))
                if c - 1 >= 0:
                    if self.screen[r + 1][c - 1][0] == 'b':
                        allmoves.append(Movement(self.playerwhite, (r, c), (r + 1, c - 1), self.screen))
                    elif (r + 1, c - 1) == self.enpassant_possible:
                        allmoves.append(
                            Movement(self.playerwhite, (r, c), (r + 1, c - 1), self.screen, is_enpassant_move=True))
                if c + 1 <= 7:
                    if self.screen[r + 1][c + 1][0] == 'b':
                        allmoves.append(Movement(self.playerwhite, (r, c), (r + 1, c + 1), self.screen))
                    elif (r + 1, c + 1) == self.enpassant_possible:
                        allmoves.append(
                            Movement(self.playerwhite, (r, c), (r + 1, c + 1), self.screen, is_enpassant_move=True))

    def getkingmoves(self, r, c, allmoves):
        if self.playerwhite:
            pass
        if r + 1 <= 7:
            if self.screen[r + 1][c] == '--' or self.screen[r + 1][c][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r,c), (r + 1,c), self.screen))
        if r - 1 >= 0:
            if self.screen[r - 1][c] == '--' or self.screen[r - 1][c][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r,c), (r - 1,c), self.screen))
        if c + 1 <= 7:
            if self.screen[r][c + 1] == '--' or self.screen[r][c + 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r,c), (r,c + 1), self.screen))
        if c - 1 >= 0:
            if self.screen[r][c - 1] == '--' or self.screen[r][c - 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r,c), (r,c - 1), self.screen))
        if r + 1 <= 7 and c + 1 <= 7:
            if self.screen[r + 1][c + 1] == '--' or self.screen[r + 1][c + 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r,c), (r + 1,c + 1), self.screen))
        if r + 1 <= 7 and c - 1 >= 0:
            if self.screen[r + 1][c - 1] == '--' or self.screen[r + 1][c - 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r,c), (r + 1,c - 1), self.screen))
        if r - 1 >= 0 and c + 1 <= 7:
            if self.screen[r - 1][c + 1] == '--' or self.screen[r - 1][c + 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r,c), (r - 1,c + 1), self.screen))
        if r - 1 >= 0 and c - 1 >= 0:
            if self.screen[r - 1][c - 1] == '--' or self.screen[r - 1][c - 1][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r, c), (r - 1, c - 1), self.screen))

    def get_castlemoves(self, r, c, allmoves):
        if self.square_attacked(r, c):
            return
        if (self.white_to_move and self.currentpossiblecastling.whitekingside) or (
                not self.white_to_move and self.currentpossiblecastling.blackkingside):
            self.get_kingsidecastles(r, c, allmoves)
        if (self.white_to_move and self.currentpossiblecastling.whitequeenside) or (
                not self.white_to_move and self.currentpossiblecastling.blackqueenside):
            self.get_queensidecastles(r, c, allmoves)

    def get_queensidecastles(self, r, c, allmoves):
        if self.screen[r][c - 1] == '--' and self.screen[r][c - 2] == '--' and self.screen[r][c - 3] == '--':
            if not self.square_attacked(r, c - 1) and not self.square_attacked(r, c - 2):
                allmoves.append(Movement(self.playerwhite,(r, c), (r, c - 2), self.screen, castle=True))

    def get_kingsidecastles(self, r, c, allmoves):
        if self.screen[r][c + 1] == "--" and self.screen[r][c + 2] == "--":
            if not self.square_attacked(r, c + 1) and not self.square_attacked(r, c + 2):
                allmoves.append(Movement(self.playerwhite,(r, c), (r, c + 2), self.screen, castle=True))

    def getknightmoves(self, r, c, allmoves):
        l = 1
        o = 2
        if r + o <= 7 and c + l <= 7:
            if self.screen[r + o][c + l] == '--' or self.screen[r + o][c + l][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r, c), (r + o, c + l), self.screen))
        if r + o <= 7 and c - l >= 0:
            if self.screen[r + o][c - l] == '--' or self.screen[r + o][c - l][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r, c), (r + o, c - l), self.screen))
        if r - o >= 0 and c + l <= 7:
            if self.screen[r - o][c + l] == '--' or self.screen[r - o][c + l][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r, c), (r - o, c + l), self.screen))
        if r - o >= 0 and c - l >= 0:
            if self.screen[r - o][c - l] == '--' or self.screen[r - o][c - l][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r, c), (r - o, c - l), self.screen))
        if r + l <= 7 and c + o <= 7:
            if self.screen[r + l][c + o] == '--' or self.screen[r + l][c + o][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r, c), (r + l, c + o), self.screen))
        if r + l <= 7 and c - o >= 0:
            if self.screen[r + l][c - o] == '--' or self.screen[r + l][c - o][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r, c), (r + l, c - o), self.screen))
        if r - l >= 0 and c + o <= 7:
            if self.screen[r - l][c + o] == '--' or self.screen[r - l][c + o][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r, c), (r - l, c + o), self.screen))
        if r - l >= 0 and c - o >= 0:
            if self.screen[r - l][c - o] == '--' or self.screen[r - l][c - o][0] == ('b' if self.white_to_move else 'w'):
                allmoves.append(Movement(self.playerwhite,(r, c), (r - l, c - o), self.screen))

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
                    endpiece = self.screen[endrow][endcol]
                    if endpiece == "--":
                        allmoves.append(Movement(self.playerwhite,(r, c), (endrow, endcol), self.screen))
                    elif endpiece[0] == enemycolor:
                        allmoves.append(Movement(self.playerwhite,(r, c), (endrow, endcol), self.screen))
                        break
                    else:
                        break
                else:
                    break


class castle_types():
    def __init__(self,whitequeenside, whitekingside, blackqueenside, blackkingside):
        self.whitequeenside = whitequeenside
        self.whitekingside = whitekingside
        self.blackqueenside = blackqueenside
        self.blackkingside = blackkingside


class Movement:
    def __init__(self,playerwhite,  start, end, screen, is_enpassant_move=False, castle=False):
        self.startrow = start[0]
        self.startcolumn = start[1]
        self.endrow = end[0]
        self.endcolumn = end[1]
        self.piecemoved = screen[self.startrow][self.startcolumn]
        self.piececaptured = screen[self.endrow][self.endcolumn]
        self.pawnpromotion = False
        if playerwhite:
            if self.piecemoved == 'bp' and self.endrow == 7:
                self.pawnpromotion = True
            elif self.piecemoved == 'wp' and self.endrow == 0:
                self.pawnpromotion = True
        else:
            if self.piecemoved == 'bp' and self.endrow == 0:
                self.pawnpromotion = True
            elif self.piecemoved == 'wp' and self.endrow == 7:
                self.pawnpromotion = True
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piececaptured = "wp" if self.piecemoved == "bp" else "bp"
        self.castle = castle
        self.moveid = self.startrow * 1000 + self.startcolumn * 100 + self.endrow * 10 + self.endcolumn

    ranktorows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    ranks_translator = {7:"1", 6: "2", 5:"3", 4:"4",
                        3:"5", 2:"6", 1:"7", 0:"8"}
    ranks_trans = {v: k for k, v in ranks_translator.items()}
    rowstoranks = {v: k for k, v in ranktorows.items()}
    filestocols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    files_translator = {0:"a", 1:"b", 2:"c", 3:"d"
                        , 4:"e", 5:"f", 6:"g", 7:"h"}
    files_trans = {v: k for k, v in files_translator.items()}

    colstofiles = {v: k for k, v in filestocols.items()}
    blacktowhite = {0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 0 }
    whitetoblack = {v: k for k, v in blacktowhite.items()}

    def chessnotation(self):
        return self.rankfile(self.startrow, self.startcolumn) + self.rankfile(self.endrow, self.endcolumn)

    def rankfile(self, c, r):
        return self.rowstoranks[r] + self.colstofiles[c]

    def blacktowhitemaker(self, r):
        return self.whitetoblack[r]
    def files_trans_maker(self,r):
        return self.files_trans[r]

    def ranks_trans_maker(self, r):
        return  self.ranks_trans[r]

    def blacktowhitemoveid(self):
        return self.blacktowhitemaker(self.startrow) * 1000 + self.blacktowhitemaker(self.startcolumn) * 100 + self.blacktowhitemaker(self.endrow) * 10 + self.blacktowhitemaker(self.endcolumn)

    def to_moveid(self,star):
        return self.ranks_trans_maker(star[0]) * 1000 + self.files_trans_maker(star[1]) * 100 + self.ranks_trans_maker(star[2]) * 10 + self.files_trans_maker(star[3])

    def __eq__(self, other):
        if isinstance(other, Movement):
            return self.moveid == other.moveid
        return False
