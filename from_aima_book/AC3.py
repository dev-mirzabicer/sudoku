# Propagation with AC-3 (as explained in my slides)


def AC3(csp, queue=None, removals=None):
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        # print(len(queue))
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xi:
                    queue.append((Xk, Xi))
            # csp.update()
    return True


def revise(csp, Xi, Xj, removals):
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised
