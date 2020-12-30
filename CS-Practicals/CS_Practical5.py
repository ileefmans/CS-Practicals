import random
import string
import string
import re
import numpy as np
import time

words = string.ascii_lowercase


class board:
    def __init__(self, n_grid=None):
        if n_grid == None:
            n_grid = 9
        self.n_grid = n_grid
        self.cur = [[" " for _ in range(self.n_grid)] for _ in range(self.n_grid)]

    def __repr__(self):
        # structured print for the board
        res = ""
        for i in range(2 * (self.n_grid + 1)):
            if i == 0:
                res += " " * 6
                res += "   ".join(words[: self.n_grid])
                res += " " * 2
                res += "\n"
                continue
            if i % 2 == 1:
                res += " " * 4 + "-" * (4 * self.n_grid + 1) + "\n"
                continue
            res += (
                str(i // 2)
                + " " * (4 - len(str(i // 2)))
                + "| "
                + " | ".join(self.cur[(i - 1) // 2])
                + " |\n"
            )
        return res


class game(board):
    def __init__(self, n_mines=None, n_grid=None):
        if n_mines is None:
            n_mines = 10
        if n_grid is None:
            n_grid = 9
        self.mine_map = board(n_grid)  # mine board
        self.dis_map = board(n_grid)  # display board
        self.n_mines = n_mines
        self.n_grid = n_grid
        # randomly initialize the mine positions
        self.pos_mines = list(
            map(
                lambda x: divmod(x, self.n_grid),
                np.random.choice(self.n_grid ** 2, self.n_mines, replace=False),
            )
        )

        for i in self.pos_mines:
            self.mine_map.cur[i[0]][i[1]] = "X"

        self.conversion = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7,
            "i": 8,
            "j": 9,
            "k": 10,
            "l": 11,
        }

    def play(self):
        """
        Play the game
        """
        print("=" * 70)
        print(
            "Starting Minesweeper (with {} mines on {}x{} grid.)".format(
                self.n_mines, self.n_grid, self.n_grid
            )
            + "\n"
        )
        print(self.dis_map)
        print("=" * 70)

        result = False
        base = [0, 0]
        while not result:
            result = self.check1(base)
            if base[0] < self.n_grid:
                base[0] = base[0] + 1
            else:
                base[1] = base[1] + 1

        print(self.mine_map)

        done = False
        while not done:

            index0 = (
                int(
                    input("PLEASE ENTER ROW, A NUMBER FROM 1 to {}".format(self.n_grid))
                )
                - 1
            )
            index1 = self.conversion[input("PLEASE ENTER COLUMN, A LETTER FROM a to i")]
            index = (index0, index1)

            out = self.check(index)
            print(out)
            if out == "BOMB":
                print("BOMB!!! YOU LOSE!!!")
                return
            else:
                print(self.dis_map)

            count = 0
            print(self.dis_map.cur)
            for i in self.dis_map.cur:
                for j in i:
                    if j == " ":
                        count += 1
            if count == 0:
                done = True
        print("YOU WIN!!!")

    def check(self, idx):
        """
        check to see what to reveal to player
        """

        already_visited = [idx]

        # list of directions to move to find neighbors
        directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]

        # Take car of scenarios where bomb spot or already chosen spot are picked
        if self.mine_map.cur[idx[0]][idx[1]] == "X":
            return "BOMB"
        elif self.mine_map.cur[idx[0]][idx[1]] in ["1", "2", "3", "4", "5", "6"]:
            self.dis_map.cur[idx[0]][idx[1]] = self.mine_map.cur[idx[0]][idx[1]]
            return self.mine_map.cur[idx[0]][idx[1]]
        else:

            def search1(index):
                if (
                    self.mine_map.cur[index[0]][index[1]] == "X"
                    or index[0] < 0
                    or (self.n_grid) < index[0]
                    or index[1] < 0
                    or (self.n_grid) < index[1]
                ):

                    return

                elif self.mine_map.cur[index[0]][index[1]] in [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                ]:

                    self.dis_map.cur[index[0]][index[1]] = self.mine_map.cur[index[0]][
                        index[1]
                    ]
                    return

                else:
                    self.dis_map.cur[index[0]][index[1]] = self.mine_map.cur[index[0]][
                        index[1]
                    ]

                    for direction in directions:
                        new_direction = (
                            index[0] + direction[0],
                            index[1] + direction[1],
                        )

                        # make sure we do not go out of range of the board
                        if 0 <= new_direction[0] <= (
                            self.n_grid - 1
                        ) and 0 <= new_direction[1] <= (self.n_grid - 1):
                            if new_direction not in already_visited:
                                if (
                                    self.mine_map.cur[new_direction[0]][
                                        new_direction[1]
                                    ]
                                    != "X"
                                ):
                                    already_visited.append(new_direction)
                                    # recursive call
                                    search1(new_direction)

            search1(idx)

            return "DONE"

    def check1(self, idx):

        """
        Sweeps entire board to find all numbers
        """
        already_visited = [idx]

        # list of directions to move to find neighbors
        directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]

        # Take car of scenarios where bomb spot or already chosen spot are picked
        if self.mine_map.cur[idx[0]][idx[1]] == "X":
            return False
        elif self.mine_map.cur[idx[0]][idx[1]] in ["0", "1", "2", "3", "4", "5", "6"]:
            return False
        else:

            # function to recursively check to see how many mines are around spot chosen
            def search(index):

                # if you come accross a spot that is a mine terminate search in that direction
                if (
                    self.mine_map.cur[index[0]][index[1]] == "X"
                    or index[0] < 0
                    or (self.n_grid) < index[0]
                    or index[1] < 0
                    or (self.n_grid) < index[1]
                ):
                    # print("ENDING SINGLE SEARCH")
                    return

                # elif self.mine_map.cur[index[0]][index[1]] =="":
                else:
                    # print("IN ELSE")

                    # check the number of neighboring spots that have mines
                    num_neighbors = 0

                    for direction in directions:
                        new_direction = (
                            index[0] + direction[0],
                            index[1] + direction[1],
                        )
                        # make sure we do not go out of range of the board
                        if 0 <= new_direction[0] <= (
                            self.n_grid - 1
                        ) and 0 <= new_direction[1] <= (self.n_grid - 1):
                            # if the neighbor is a mine
                            if (
                                self.mine_map.cur[new_direction[0]][new_direction[1]]
                                == "X"
                            ):
                                num_neighbors += 1

                    # update mine map with number of neighboring mines at that spot
                    self.mine_map.cur[index[0]][index[1]] = str(num_neighbors)

                    # update display map with number of neighboring mines at that spot
                    # self.dis_map.cur[index[0]][index[1]] = str(num_neighbors)

                    # for each direction make a recursive call
                    for direction in directions:
                        new_direction = (
                            index[0] + direction[0],
                            index[1] + direction[1],
                        )

                        # make sure we do not go out of range of the board
                        if 0 <= new_direction[0] <= (
                            self.n_grid - 1
                        ) and 0 <= new_direction[1] <= (self.n_grid - 1):
                            if new_direction not in already_visited:
                                if (
                                    self.mine_map.cur[new_direction[0]][
                                        new_direction[1]
                                    ]
                                    != "X"
                                ):
                                    already_visited.append(new_direction)
                                    # recursive call
                                    search(new_direction)

            search(idx)

            return True


if __name__ == "__main__":
    g = game(10, 9)  # n_mines=15, n_grid=12
    g.play()
