from from_aima_book.csp import first, count
from from_aima_book.utils import argmin_random_tie


def first_unassigned_variable(assignment, csp):
    return first([var for var in csp.variables if var not in assignment])


def mrv(assignment, csp):
    return argmin_random_tie(
        [v for v in csp.variables if v not in assignment],
        key=lambda var: num_legal_values(csp, var, assignment),
    )


def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(
            csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var]
        )
