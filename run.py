import prompt.prompt as prompt
import prompt.result as result
import pygame
from sudoku import Sudoku
import json
from search.backtrack_search import backtracking_search
import random

with open("./data/sudoku.json") as pzf:
    puzzles = json.load(pzf)


def run():
    print("Running")
    usr_input = prompt.prompt()
    # print(usr_input)
    puzzle = (
        usr_input.get("puzzle")
        if usr_input.get("puzzle") is not None
        else puzzles.get(usr_input.get("difficulty"))[
            random.randint(0, len(puzzles.get(usr_input.get("difficulty"))) - 1)
        ]
    )
    # print(puzzle)
    solve_status = 0  # 0: not solved yet | result: solved | None: unsolveable
    e = Sudoku(puzzle)
    e.draw_init()
    pygame.display.update()
    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if solve_status == 0:
                    solve_status = backtracking_search(
                        e,
                        usr_input["args"]["Variable selection"],
                        usr_input["args"]["Value ordering"],
                        usr_input["args"]["Inference"],
                        usr_input["args"]["Delay"],
                    )
                    # print(solve_status)
                else:
                    if solve_status is not None:
                        again = result.solved_screen()
                    else:
                        again = result.invalid_screen()
                    game_on = again
                    pygame.display.quit()
                    # pygame.quit()
                    break
        try:
            pygame.display.update()
        except:
            if again is not None and again:
                run()
