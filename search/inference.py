from from_aima_book.AC3 import AC3


def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True


def mac(csp, var, value, assignment, removals):
    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)
