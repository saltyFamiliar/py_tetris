import random
import time
from typing import List, Tuple
from time import sleep

from blessed import Terminal
import curses

WINDOW_WIDTH = 20
WINDOW_HEIGHT = 15


class Tgram:
    def __init__(self):
        possible_shapes = [
            [
                [0, 1, 0],
                [1, 1, 1],
            ],
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1, 1, 1]
            ],
            [
                [1, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 1, 1],
                [1, 1, 0]
            ],
            [
                [1, 0],
                [1, 0],
                [1, 1]
            ],
            [
               [0, 1],
               [0, 1],
               [1, 1]
            ]
        ]

        self.shape_matrix = possible_shapes[random.randint(0, len(possible_shapes) - 1)]
        self.position = (0, 10)
        self.height = len(self.shape_matrix)

    def fall(self):
        if self.position[0] <= WINDOW_HEIGHT - self.height:
            self.position = (self.position[0] + 1, self.position[1])

    def move(self, d: int):
        self.position = (self.position[0], self.position[1] + d)

    def is_blocked(self, grid: List[List]):
        for col, block in enumerate(self.shape_matrix[-1]):
            if block:
                if grid[self.position[0] + self.height][col + self.position[1]]:
                    return True
        return False

    def rotate_right(self):
        new_shape_matrix: List[List[int]] = []
        col = 0
        while col < len(self.shape_matrix[0]):
            new_row = []
            row = self.height - 1
            while row >= 0:
                new_row.append(self.shape_matrix[row][col])
                row -= 1
            new_shape_matrix.append(new_row)
            col += 1
        self.shape_matrix = new_shape_matrix
        self.height = len(self.shape_matrix)


def print_grid(grid: List[List[int]]) -> None:
    out_str = ""
    for row in grid:
        for col in row:
            if col == 1:
                out_str += "█"
            elif col == 2:
                out_str += "═"
            else:
                out_str += "."
        out_str += "\n"

    print(out_str)


def place_tgram(grid: List[List[int]], tgram_: Tgram):
    for y, row in enumerate(tgram.shape_matrix):
        for x, col in enumerate(row):
            if col:
                grid[tgram_.position[0] + y][tgram_.position[1] + x] = col


def clear_tgram(grid: List[List[int]], tgram_: Tgram):
    for y, row in enumerate(tgram_.shape_matrix):
        for x, col in enumerate(row):
            if col:
                grid[tgram_.position[0] + y][tgram_.position[1] + x] = 0


term = Terminal()
game_grid: List[List[int]] = [[0 for _ in range(WINDOW_WIDTH)] for _ in range(WINDOW_HEIGHT - 1)]
game_grid.append([2 for _ in range(WINDOW_WIDTH)])

tgram = Tgram()
steps = 0
print(term.clear)
with term.cbreak():
    with term.hidden_cursor():
        while True:
            # clear last tgram position
            clear_tgram(game_grid, tgram)

            if steps % 3 == 0:
                if not tgram.is_blocked(game_grid):
                    tgram.fall()
                else:
                    place_tgram(game_grid, tgram)
                    tgram = Tgram()
                    steps += 1
                    continue

            # change tgram pos based on user input
            val = term.inkey(timeout=0.05)
            if val.code == curses.KEY_LEFT:
                tgram.move(-1)
            elif val.code == curses.KEY_RIGHT:
                tgram.move(1)
            elif val == ' ':
                tgram.rotate_right()
            elif val.lower() == 'q':
                break

            place_tgram(game_grid, tgram)
            print(term.clear)
            print_grid(game_grid)
            with term.location(30, 0):
                print("score: ", steps)

            time.sleep(0.1)

            if steps % 2 == 0:
                time.sleep(0.1)

            steps += 1
