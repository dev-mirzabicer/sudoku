import time
import pygame
from from_aima_book.csp import CSP
import re
import copy
from Cube import Cube


class Sudoku(CSP):
    def __init__(self, grid, show=True):
        self.show = show
        BLOCK_SIZE = 3
        BLOCKS_IN_ROW = 3
        ROW_SIZE = 9
        COL_SIZE = 9

        # Variables -
        # Variables definition. The varibles are an array with a sequence of indexes, from 0 to 80.

        self.variables = [x for x in range(ROW_SIZE * COL_SIZE)]
        # Domains -
        # Domains defintion. In this case of Sudoku CSP, the domains are '123456789' for empty cells and
        # the value of cell for cells with the default value.
        original_grid = list(iter(re.findall(r"\d|\.", grid)))
        domains = {}
        counter = 0
        for item in original_grid:
            if item == ".":
                domains[int(counter)] = "123456789"
            else:
                value = int(item)
                restricted_domain = [str(value)]
                domains[int(counter)] = restricted_domain
            counter += 1

        # Neighbors
        # Neighbors of binary-constraint definition. This dictionary contains the relations among a cell with its row,
        # column and block.
        neighbors = {}

        # rows
        # ∀ a
        # ∀ i ≠ j: xai ≠ xaj
        for a in range(ROW_SIZE):
            row_start = a * BLOCKS_IN_ROW * BLOCK_SIZE
            row_stop = a * BLOCKS_IN_ROW * BLOCK_SIZE + BLOCKS_IN_ROW * BLOCK_SIZE
            row_indexes = list(range(row_start, row_stop))
            for item in row_indexes:
                neighbors[int(item)] = list()
                item_neighbors = list(copy.copy(row_indexes))
                item_neighbors = [x for x in item_neighbors if x != item]
                neighbors[int(item)] += item_neighbors

        # columns
        # ∀ b
        # ∀ h ≠ k : xbh ≠ xbk
        for b in range(COL_SIZE):
            col_indexes = [ROW_SIZE * a + b for a in range(COL_SIZE)]
            for item in col_indexes:
                item_neighbors = list(copy.copy(col_indexes))
                item_neighbors = [x for x in item_neighbors if x != item]
                neighbors[int(item)] += item_neighbors

        # blocks
        # A block is a submatrix of sudoku grid:
        # a = {1, 4, 7}:  i, j = [a, a + 2]
        # b = {1, 4, 7}:  k, h = [b, b + 2]
        # {xpq} p = a...a + 2, q = b...b + 2 ∈ A ∈ N^(3x3)
        # where
        # ∀a:  i, j = [a, a + 2]
        # ∀b:  k, h = [b, b + 2]
        # ∀ h ≠ k or i ≠ j: xik ≠ xj, h
        a = b = [0, 3, 6]
        for b_row in a:
            for b_col in b:
                # block
                block_items = []
                for r in range(3):
                    for c in range(3):
                        block_items.append((b_row + r) * ROW_SIZE + b_col + c)

                for item in block_items:
                    item_neighbors = list(copy.copy(block_items))
                    item_neighbors = [x for x in item_neighbors if x != item]
                    neighbors[int(item)] += item_neighbors

        # remove duplicates
        for item in neighbors:
            neighbors[int(item)] = set(neighbors[int(item)])

        CSP.__init__(self, None, domains, neighbors, self.different_values_constraint)
        if show:
            pygame.init()
            pygame.font.init()
            self.win = pygame.display.set_mode((540, 560))
            pygame.display.set_caption("Sudoku")
        self.start_time = time.time()
        self.iterations = 0

    def update_stats(self):
        pygame.draw.rect(self.win, (0, 0, 0), (0, 0, 540, 20))
        elapsed_time = time.time() - self.start_time
        font = pygame.font.SysFont("comicsans", 13)
        iterations_text = font.render(
            f"Iterations: {self.iterations}", True, (255, 255, 255)
        )
        time_text = font.render(f"Elapsed: {elapsed_time:.2f} s", True, (255, 255, 255))

        self.win.blit(iterations_text, (0, 0), (0, 0, 270, 20))
        self.win.blit(time_text, (270, 0), (0, 0, 270, 20))

    @staticmethod
    def different_values_constraint(A, a, B, b):
        return a != b

    def update(self, delay=0):
        if not self.show:
            return
        self.update_stats()
        newCube = not hasattr(self, "cubes")
        if newCube:
            self.cubes = [
                [Cube(self.domains[i][0], i, j, 540, 540) for j in range(9)]
                for i in range(9)
            ]
        for i, item in enumerate(self.variables):
            row = i // 9
            col = i % 9
            value = self.infer_assignment().get(item, 0)
            if newCube:
                self.cubes[row][col].set(value)
                self.cubes[row][col].set_temp(value)
            else:
                self.cubes[row][col].set_temp(value)
            changed = self.cubes[row][col].temp != self.cubes[row][col].value
            if changed or newCube:
                self.cubes[row][col].set(value)
                self.cubes[row][col].draw_change(self.win, True)
                pygame.display.update()
                pygame.time.delay(delay)

    def draw_init(self):
        if not self.show:
            return
        self.update_stats()
        self.update()
        # Draw Grid Lines
        gap = 540 / 9
        for i in range(9 + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(
                self.win, (0, 0, 0), (0, (i * gap) + 20), (540, (i * gap) + 20), thick
            )
            pygame.draw.line(
                self.win,
                (0, 0, 0),
                ((i * gap), 0 + 20),
                ((i * gap), 540 + 20),
                thick,
            )

        # Draw Cubes
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].draw(self.win)
