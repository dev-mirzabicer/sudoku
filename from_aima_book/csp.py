from from_aima_book.utils import count, first


class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(
                var, val, var2, assignment[var2]
            )

        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        # Subclasses can print in a prettier way, or display with a GUI
        print("CSP:", self, "with assignment:", assignment)

    # Methods for the tree and graph-search interface:

    def actions(self, state):
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [
                (var, val)
                for val in self.domains[var]
                if self.nconflicts(var, val, assignment) == 0
            ]

    def result(self, state, action):
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        assignment = dict(state)
        return len(assignment) == len(self.variables) and all(
            self.nconflicts(variables, assignment[variables], assignment) == 0
            for variables in self.variables
        )

    # For constraint propagation

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        self.support_pruning()
        return {
            v: self.curr_domains[v][0]
            for v in self.variables
            if 1 == len(self.curr_domains[v])
        }

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        return [
            var
            for var in self.variables
            if self.nconflicts(var, current[var], current) > 0
        ]

    def update(self):
        pass
