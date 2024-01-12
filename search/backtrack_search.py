from search import inference
from search import value_ordering
from search import variable_selection


helper_fn = {
    "variable_selections": {
        "first_unassigned_variable": variable_selection.first_unassigned_variable,
        "mrv": variable_selection.mrv,
    },
    "value_orderings": {
        "unordered_domain_values": value_ordering.unordered_domain_values,
        "lcv": value_ordering.lcv,
    },
    "inferences": {
        "no_inference": inference.no_inference,
        "forward_checking": inference.forward_checking,
        "mac": inference.mac,
    },
}


def backtracking_search(
    csp,
    select_unassigned_variable_str="first_unassigned_variable",
    order_domain_values_str="unordered_domain_values",
    inference_str="no_inference",
    delay=0,
):
    select_unassigned_variable = helper_fn["variable_selections"][
        select_unassigned_variable_str
    ]
    order_domain_values = helper_fn["value_orderings"][order_domain_values_str]
    inference = helper_fn["inferences"][inference_str]

    def backtrack(assignment):
        csp.update(delay)
        csp.iterations += 1
        if csp.iterations > 100000:
            return None
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result
