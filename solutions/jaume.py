from ortools.sat.python import cp_model

def knapsack_with_boosts(
    weights: list[int],
    volumes: list[int],
    values: list[float],
    boosts: list[tuple[int,int,float]],
    max_weight: int,
    max_volume: int,
    time_limit_s: float = 10.0
):
    """
    0/1 knapsack with weight & volume caps, plus pairwise boost triplets.

    Args:
      weights, volumes    : lists of ints, len = n
      values               : list of floats, len = n
      boosts               : list of (a, b, boost_factor)
                             — when x[b]=1 and x[a]=1, a’s value *= boost_factor
      max_weight, max_volume: capacity limits
      time_limit_s         : solver time limit in seconds

    Returns:
      selected_indices, total_value
    """
    n = len(values)
    model = cp_model.CpModel()

    # Decision vars: x[i]=1 if we pick item i
    x = [model.NewBoolVar(f"x[{i}]") for i in range(n)]

    # For each (a,b,boost) define z_ab = x[a] AND x[b]
    z = []
    for (a, b, _) in boosts:
        z_var = model.NewBoolVar(f"z[{a},{b}]")
        # z_var ⇒ x[a], x[b]
        model.Add(z_var <= x[a])
        model.Add(z_var <= x[b])
        # x[a] + x[b] ⇒ z_var
        model.Add(z_var >= x[a] + x[b] - 1)
        z.append(((a, b), z_var))

    # Capacity constraints
    model.Add(sum(weights[i] * x[i] for i in range(n)) <= max_weight)
    model.Add(sum(volumes[i] * x[i] for i in range(n)) <= max_volume)

    # Build objective: base values + extra from boosts
    obj_terms = []
    for i in range(n):
        obj_terms.append(values[i] * x[i])
    # now add boost extras
    for ((a, b), z_var), (_, _, boost) in zip(z, boosts):
        # when z_var=1, item a contributes an extra (boost-1)*values[a]
        extra = values[a] * (boost - 1)
        obj_terms.append(extra * z_var)

    model.Maximize(sum(obj_terms))

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, None

    selected = [i for i in range(n) if solver.Value(x[i])]

    # DEBUGGING PRINTS
    tw = sum(weights[i] for i in selected)
    tv = sum(volumes[i] for i in selected)
    print(f"--> weight {tw} (≤{max_weight}), volume {tv} (≤{max_volume})")
    
    total = solver.ObjectiveValue()
    return selected, total


if __name__ == "__main__":
    # Example data
    max_w, max_v = 1000, 2500

    weights = [180, 430, 230, 240, 10, 30, 10, 240, 80, 10, 10, 40, 40, 56, 9, 300, 140, 400, 200, 100, 80, 10, 200, 74, 81, 59, 20, 92, 100, 73, 81, 7, 19, 120, 180, 220, 30, 400, 100, 80, 10, 1, 1, 20, 40, 130, 50, 22, 10, 320]
    volumes = [379, 269, 410, 280, 165, 26, 77, 400, 90, 26, 40, 60, 80, 33, 22, 680, 80, 230, 165, 80, 40, 10, 120, 140, 90, 77, 26, 60, 77, 230, 33, 10, 26, 165, 240, 939, 963, 524, 159, 313, 792, 679, 26, 962, 81, 40, 540, 59, 10, 441]
    values = [24446, 23955, 17275, 24913, 11589, 5953, 2249, 17730, 8497, 7824, 2536, 9288, 6331, 7052, 1582, 21619, 5128, 7374, 2658, 6720, 2288, 1688, 1749, 6188, 7146, 9754, 2575, 1017, 8918, 27957, 7465, 13744, 9943, 8099, 12159, 2354, 8244, 7220, 6266, 5364, 8918, 1091, 896, 15000, 1590, 16630, 8750, 4974, 4000, 14626]
    boosts = [(0, 47, 1.47), (0, 4, 0.64), (1, 24, 1.12), (1, 6, 0.55), (2, 22, 1.26), (2, 23, 0.33), (3, 12, 1.29), (3, 32, 0.7), (4, 1, 1.82), (4, 40, 0.89), (5, 30, 1.77), (5, 26, 0.58), (6, 2, 1.31), (6, 32, 1.0), (7, 0, 1.81), (7, 9, 0.38), (8, 35, 1.8), (8, 38, 0.18), (9, 47, 1.35), (9, 48, 0.78), (10, 7, 1.13), (10, 9, 1.0), (11, 0, 1.73), (11, 1, 0.67), (12, 13, 1.6), (12, 27, 0.64), (13, 32, 1.43), (13, 26, 0.71), (14, 27, 1.43), (14, 23, 1.0), (15, 4, 1.48), (15, 8, 0.7), (16, 31, 1.56), (16, 5, 0.27), (17, 15, 2.11), (17, 39, 0.31), (18, 8, 1.96), (18, 32, 1.0), (19, 28, 1.65), (19, 42, 0.33), (20, 21, 1.49), (20, 35, 1.0), (21, 20, 1.6), (21, 8, 1.0), (22, 1, 1.57), (22, 3, 1.0), (23, 41, 1.49), (23, 5, 0.21), (24, 36, 1.33), (24, 47, 0.16), (25, 28, 1.77), (25, 30, 0.25), (26, 35, 1.75), (26, 17, 1.0), (27, 16, 1.99), (27, 14, 1.0), (28, 39, 1.84), (28, 25, 0.12), (29, 3, 1.8), (29, 23, 0.48), (30, 9, 1.98), (30, 25, 0.79), (31, 48, 1.42), (31, 1, 0.64), (32, 9, 1.7), (32, 45, 0.4), (33, 37, 1.87), (33, 44, 0.49), (34, 38, 1.42), (34, 6, 0.23), (35, 6, 1.16), (35, 20, 1.0), (36, 37, 1.48), (36, 15, 0.21), (37, 24, 1.95), (37, 11, 0.51), (38, 28, 1.18), (38, 14, 0.65), (39, 31, 1.83), (39, 38, 0.35), (40, 28, 1.79), (40, 47, 0.5), (41, 37, 1.15), (41, 24, 1.0), (42, 5, 1.83), (42, 44, 1.0), (43, 29, 1.62), (43, 39, 0.69), (44, 6, 1.98), (44, 18, 1.0), (45, 42, 1.7), (45, 0, 0.8), (46, 34, 1.65), (46, 22, 0.33), (47, 3, 1.49), (47, 28, 0.71), (48, 22, 1.57), (48, 42, 0.18), (49, 48, 1.85), (49, 19, 0.42)]
        
    # Triplets: (a, b, boost)
    # – Picking item 2 with item 0 doubles item 2’s value
    # – Picking item 3 with item 1 gives item 3 a 1.5× boost
    sel, val = knapsack_with_boosts(
        weights, volumes, values, boosts, max_w, max_v
    )
    print("Selected items:", sel)
    print("Total boosted value:", val)
