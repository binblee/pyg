from typing import Tuple
import random


class Board:
    EMPTY = '.'

    def __init__(self) -> None:
        self.board = [self.EMPTY for _ in range(9)]

    def print(self) -> None:
        for row in [self.board[i*3:i*3+3] for i in range(3)]:
            print(' | ' + ' | '.join(row) + ' | ')
        print('')

    def position_avaliable(self) -> list:
        return [pos for pos, mark in enumerate(self.board)
                if mark == self.EMPTY]

    def is_valid_move(self, pos) -> bool:
        return pos in self.position_avaliable()

    def make_move(self, pos, mark) -> int:
        valid_move = self.is_valid_move(pos)
        if valid_move:
            self.board[pos] = mark
        return valid_move

    def is_win(self, pos) -> bool:
        mark = self.board[pos]
        # check row
        row = pos // 3
        if all([m == mark for m in self.board[row*3: row*3+3]]):
            return True
        # check col
        col = pos % 3
        if all([self.board[3*i+col] == mark for i in range(3)]):
            return True
        # check diagonal, pos in [0, 2, 4, 6, 8]
        if pos % 2 == 0:
            if all([self.board[i] == mark for i in (0, 4, 8)]):
                return True
            if all([self.board[i] == mark for i in (2, 4, 6)]):
                return True
        return False


class Player:
    def __init__(self, mark, board: Board) -> None:
        self.mark = mark
        self.board = board

    def move(self):
        return random.choices(self.board.position_avaliable())[0]


class HumanPlayer(Player):
    def __init__(self, mark, board: Board) -> None:
        super().__init__(mark, board)

    def move(self) -> Tuple[int, str]:
        index = None
        valid_positions = self.board.position_avaliable()
        while index not in valid_positions:
            try:
                index = int(input(f'Your turn {valid_positions}:'))
                if index not in valid_positions:
                    raise ValueError
            except ValueError:
                print(f'Invalid move {index}, try again.')
        return index


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.player1 = HumanPlayer('X', self.board)
        self.player2 = Player('O', self.board)

    def play(self):
        player = self.player1
        self.board.print()
        winner = None
        while self.board.position_avaliable() and not winner:
            print(f'{player.mark} move:')
            index = player.move()
            self.board.make_move(index, player.mark)
            self.board.print()
            if self.board.is_win(index):
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
