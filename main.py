import curses
from random import randint
from time import sleep
from typing import List

from blessed import Terminal

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

        self.shape_matrix = possible_shapes[randint(0, len(possible_shapes) - 1)]
        self.position = (0, 10)
        self.height = len(self.shape_matrix)
        self.width = len(self.shape_matrix[0])

    def fall(self):
        if self.position[0] <= WINDOW_HEIGHT - self.height:
            self.position = (self.position[0] + 1, self.position[1])

    def move(self, d: int):
        self.position = (self.position[0], self.position[1] + d)

    def can_fall(self, grid: List[List]):
        for col, block in enumerate(self.shape_matrix[-1]):
            if block:
                if grid[self.position[0] + self.height][col + self.position[1]]:
                    return False
        return True

    def is_blocked(self, grid: List[List], direction: int) -> bool:
        """
        checks if shape can move along the x-axis along the given direction
        """
        for row_num, shape_row in enumerate(self.shape_matrix):
            collision_index = 0 if direction < 0 else -1
            # skip checking row if this row of shape matrix has no tile on collision index
            if not shape_row[collision_index]:
                continue
            neighbor_y = self.position[0] + row_num
            # since position is top left point of shape matrix,
            # width needs to be added to check right neighbor
            neighbor_x = self.position[1] + (direction if direction < 0 else self.width)
            return grid[neighbor_y][neighbor_x]

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
        self.width = len(self.shape_matrix[0])


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
                if tgram.can_fall(game_grid):
                    tgram.fall()
                else:
                    place_tgram(game_grid, tgram)
                    tgram = Tgram()
                    steps += 1
                    continue

            # change tgram pos based on user input
            val = term.inkey(timeout=0.05)
            if val.code == curses.KEY_LEFT:
                if tgram.position[1] > 0:
                    direction = -1
                    if not tgram.is_blocked(game_grid, direction):
                        tgram.move(direction)
            elif val.code == curses.KEY_RIGHT:
                if tgram.position[1] + len(tgram.shape_matrix[0]) < WINDOW_WIDTH:
                    direction = 1
                    if not tgram.is_blocked(game_grid, direction):
                        tgram.move(direction)
            elif val == ' ':
                tgram.rotate_right()
            elif val.lower() == 'q':
                break

            place_tgram(game_grid, tgram)
            print(term.clear)
            print_grid(game_grid)
            with term.location(30, 0):
                print("score: ", steps)

            sleep(0.1)

            if steps % 2 == 0:
                sleep(0.1)

            steps += 1
