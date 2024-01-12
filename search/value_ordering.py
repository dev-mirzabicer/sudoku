def unordered_domain_values(var, assignment, csp):
    return csp.choices(var)


def lcv(var, assignment, csp):
    return sorted(
        csp.choices(var), key=lambda val: csp.nconflicts(var, val, assignment)
    )
