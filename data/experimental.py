import time
from sudoku import Sudoku
import json
from search.backtrack_search import backtracking_search
import random

with open("./sudoku.json") as pzf:
    puzzles = json.load(pzf)

variable_selection = ""
value_ordering = ""
inference = ""
delay = 0

data = {
    "Easy": {},
    "Medium": {},
    "Hard": {},
    "Expert": {},
    "Master": {},
}


def run(
    count=0,
    dif=[
        (5, "Easy"),
        (80, "Medium"),
        (255, "Hard"),
        (355, "Expert"),
        (375, "Master"),
    ],
):
    diff = ""
    # print(usr_input)
    for i, (val, name) in enumerate(dif):
        if count > 375:
            return
        if count > val:
            continue
        else:
            diff = name
            # print(len(list(puzzles.keys())), list(puzzles.keys()), i)
            # print(puzzles.get(list(puzzles.keys())[i]))
            puzzle = puzzles.get(list(puzzles.keys())[i])[random.randint(0, 500)]
            if puzzle is None:
                print(count)
                return
            break
    # print(puzzle)
    # print(".")
    try:
        e = Sudoku(puzzle, False)
    except Exception as e:
        print("x")
        return
    solve_status = backtracking_search(
        e,
        variable_selection,
        value_ordering,
        inference,
        delay,
    )
    if solve_status is None:
        e.iterations = -1
    data[diff][str(count)] = {
        "variable_selection": variable_selection,
        "value_ordering": value_ordering,
        "inference": inference,
        "time": time.time() - e.start_time,
        "iterations": e.iterations if e.iterations >= 0 else ">100000",
    }
    run(count + 1)


if __name__ == "__main__":
    variable_selections = [
        "first_unassigned_variable",
        "mrv",
    ]
    value_orderings = [
        "unordered_domain_values",
        "lcv",
    ]
    inferences = ["no_inference", "forward_checking", "mac"]
    with open("./data.json", "w") as f:
        f.write('{\n"data:" [')
        f.close()
    for vs in variable_selections:
        for vo in value_orderings:
            for i in inferences:
                variable_selection = vs
                value_ordering = vo
                inference = i
                run()
                with open("./data.json", "a") as f:
                    json.dump(data, f)
                    f.write(",\n")
                    f.close()
                data = {
                    "Easy": {},
                    "Medium": {},
                    "Hard": {},
                    "Expert": {},
                    "Master": {},
                }
    with open("./data.json", "a") as f:
        f.write("\n]}")
        f.close()
