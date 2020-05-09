import time
from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

MAX, MIN = 1000, -1000

class StudentAI():
    
    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        bestVal = -999
        bestMove = None

        # if there is only one move to make, just make the move without evaluating
        possible_moves = self.board.get_all_possible_moves(self.color)
        if len(possible_moves) == 1 and len(possible_moves[0]) == 1:
            self.board.make_move(possible_moves[0][0], self.color)
            return possible_moves[0][0]

        for moves in possible_moves:
            for move in moves:
                self.board.make_move(move, self.color)
                val = self.search(1, StudentAI.switchColors(self.color), MIN, MAX)
                self.board.undo()

                if val > bestVal:
                    bestVal = val
                    bestMove = move

        self.board.make_move(bestMove, self.color)
        return bestMove

    def search(self, depth, currentColor, alpha, beta):
        if depth == 4 or self.board.is_win('B') or self.board.is_win('W'):
            return self.evaluate(currentColor)

        best = MIN if currentColor == self.color else MAX

        for moves in self.board.get_all_possible_moves(currentColor):
            for move in moves:
                self.board.make_move(move, currentColor)
                val = self.search(depth+1, StudentAI.switchColors(currentColor), alpha, beta)
                self.board.undo()
                
                if currentColor == self.color:
                    best = max(best, val)
                    alpha = max(alpha, best)

                elif currentColor != self.color:
                    best = min(best, val)
                    beta = min(beta, best)

                if beta <= alpha:
                    return best

        return best

    def piece_differential(self, currentColor):
        if currentColor == 'B':
            return self.board.black_count - self.board.white_count
        return self.board.white_count - self.board.black_count

    def evaluate(self, currentColor):
        currentColor = 'B' if currentColor == 1 else 'W'
        oppColor = 'W' if currentColor == 'B' else 'B'
        # if we win in this game state, prefer to choose this path
        # if the opponent wins in this game state, stay away from this path
        if self.board.is_win(currentColor):
            return 500
        elif self.board.is_win(oppColor):
            return -500

        piece_location, kings = 0, 0

        for i in range(self.board.row):
            for j in range(self.board.col):
                if (self.board.board[i][j].color == currentColor):
                    if self.board.board[i][j].is_king:
                        kings += 1
                        # we prefer the king to be in the middle of the board
                        if i <= self.row / 2:
                            piece_location += 7 + i
                        else:
                            piece_location += 7 + (self.board.row - i - 1)
                    else:
                        # we prefer the pawns to go to the opponent's side of the board
                        if self.board.board[i][j].color == 'B':
                            piece_location += 5 + i
                        else:
                            piece_location += 5 + (self.board.row - i - 1)
                elif (self.board.board[i][j].color == oppColor):
                    if self.board.board[i][j].is_king:
                        kings -= 1
                        # we prefer the opponent's king to not be in the middle of the board
                        if i <= self.row / 2:
                            piece_location -= 7 + i
                        else:
                            piece_location -= 7 + (self.board.row - i - 1)
                    else:
                        # we prefer the opponent's pawns to not be on our side of the board
                        if self.board.board[i][j].color == 'B':
                            piece_location -= 5 + i
                        else:
                            piece_location -= 5 + (self.board.row - i - 1)

        # if we have more kings, we prefer to play more aggressive
        if kings > 0:
            return piece_location + self.board.row * self.piece_differential(currentColor)
        else:
            return piece_location + self.piece_differential(currentColor)

    @staticmethod
    def switchColors(color):
        if color == 1:
            return 2
        return 1