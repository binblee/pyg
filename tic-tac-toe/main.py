import random
import math


class Board:
    EMPTY = '.'

    def __init__(self):
        self.board = [self.EMPTY for _ in range(9)]

    def print(self):
        for row in [self.board[i*3:i*3+3] for i in range(3)]:
            print(' | ' + ' | '.join(row) + ' | ')
        print('')

    def available_moves(self) -> list:
        return [square for square, mark in enumerate(self.board)
                if mark == self.EMPTY]

    def is_valid_move(self, square) -> bool:
        return square in self.available_moves()

    def make_move(self, square, mark) -> bool:
        valid_move = self.is_valid_move(square)
        if valid_move:
            self.board[square] = mark
        return valid_move

    def undo_move(self, square):
        self.board[square] = self.EMPTY

    def is_win(self, square) -> bool:
        mark = self.board[square]
        # check row
        row = square // 3
        if all([m == mark for m in self.board[row*3: row*3+3]]):
            return True
        # check col
        col = square % 3
        if all([self.board[3*i+col] == mark for i in range(3)]):
            return True
        # check diagonal, square in [0, 2, 4, 6, 8]
        if square % 2 == 0:
            if all([self.board[i] == mark for i in (0, 4, 8)]):
                return True
            if all([self.board[i] == mark for i in (2, 4, 6)]):
                return True
        return False


class Player:
    def __init__(self, mark, board: Board):
        self.mark = mark
        self.board = board

    def move(self):
        return random.choices(self.board.available_moves())[0]


class HumanPlayer(Player):
    def __init__(self, mark, board: Board):
        super().__init__(mark, board)

    def move(self):
        square = None
        available_moves = self.board.available_moves()
        while square not in available_moves:
            try:
                square = int(input(f'Your turn {available_moves}:'))
                if square not in available_moves:
                    raise ValueError
            except ValueError:
                print(f'Invalid move {square}, try again.')
        return square


class MinimaxPlayer(Player):
    def __init__(self, mark, board: Board):
        super().__init__(mark, board)

    def move(self):
        best_move = self.__minimax(self.mark)
        return best_move['square']

    def is_original(self, mark):
        return self.mark == mark

    def __minimax(self, player_mark):
        best = {'square': None, 'score': None}
        if self.is_original(player_mark):
            best['score'] = -math.inf
        else:
            best['score'] = math.inf
        available_moves = self.board.available_moves()
        if len(available_moves) == 9:
            best['square'] = random.choices(available_moves)[0]
            return best
        for move in available_moves:
            ok = self.board.make_move(move, player_mark)
            assert(ok)
            score = self.__evaluate(move, player_mark)
            if score is None:
                opponent = self.__switch_player(player_mark)
                square_score = self.__minimax(opponent)
                score = square_score['score']
            self.board.undo_move(move)
            if self.is_original(player_mark):
                if score > best['score']:
                    best = {'square': move, 'score': score}
            else:
                if score < best['score']:
                    best = {'square': move, 'score': score}
        return best

    def __switch_player(self, player_mark):
        if player_mark == 'X':
            return 'O'
        else:
            return 'X'

    def __evaluate(self, move, mark):
        num_available_move = len(self.board.available_moves())
        score = None
        if self.board.is_win(move):
            if self.mark == mark:
                score = 1 * (num_available_move + 1)
            else:
                score = - 1 * (num_available_move + 1)
        elif num_available_move == 0:
            score = 0
        return score


class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = HumanPlayer('X', self.board)
        self.player2 = MinimaxPlayer('O', self.board)

    def play(self):
        player = self.player1
        self.board.print()
        winner = None
        while self.board.available_moves() and not winner:
            print(f'{player.mark} move:')
            move = player.move()
            ok = self.board.make_move(move, player.mark)
            assert(ok)
            self.board.print()
            if self.board.is_win(move):
                winner = player
                break
            if player == self.player1:
                player = self.player2
            else:
                player = self.player1
        if winner:
            print(f'{winner.mark} WIN!')
        else:
            print("It's a tie.")


if __name__ == '__main__':
    Game().play()
