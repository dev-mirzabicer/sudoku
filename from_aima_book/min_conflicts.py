# Min-conflicts hillclimbing search for CSPs


import random

from from_aima_book.utils import argmin_random_tie


def min_conflicts(csp, max_steps=100000):
    # Generate a complete assignment for all variables (probably with conflicts)
    csp.current = current = {}
    for var in csp.variables:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            return current
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    return None


def min_conflicts_value(csp, var, current):
    return argmin_random_tie(
        csp.domains[var], key=lambda val: csp.nconflicts(var, val, current)
    )
