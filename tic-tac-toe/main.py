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
    def __init__(self, mark) -> None:
        self.mark = mark

    def move(self, valid_positions):
        return random.choices(valid_positions)[0]


class HumanPlayer(Player):
    def __init__(self, mark) -> None:
        super().__init__(mark)

    def move(self, valid_positions) -> Tuple[int, str]:
        index = None
        while index not in valid_positions:
            try:
                index = int(input(f'Your turn {valid_positions}:'))
                if index in valid_positions:
                    return index
                print(f'Invalid move {index}, try again.')
            except ValueError:
                print(f'Invalid move {index}, try again.')


class RandomPlayer(Player):
    def __init__(self, mark) -> None:
        super().__init__(mark)

    def move(self, valid_positions):
        return super().move(valid_positions)


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.player1 = HumanPlayer('X')
        self.player2 = RandomPlayer('O')

    def play(self):
        player = self.player1
        self.board.print()
        while self.board.position_avaliable():
            print(f'{player.mark} move:')
            index = player.move(self.board.position_avaliable())
            self.board.make_move(index, player.mark)
            self.board.print()
            if self.board.is_win(index):
                self.board.print()
                print(f'{player.mark} WIN!')
                break
            if player == self.player1:
                player = self.player2
            else:
                player = self.player1


if __name__ == '__main__':
    Game().play()
