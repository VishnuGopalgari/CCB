import numpy as np

# ==========================================================
# Discrete propensities for the 3 reactions (from the PDF)
# R1: 2X1 + X2 -> 4X3      a1 = k1 * C(X1,2) * X2,  k1=1
# R2: X1 + 2X3 -> 3X2      a2 = k2 * X1 * C(X3,2),  k2=2
# R3: X2 + X3 -> 2X1       a3 = k3 * X2 * X3,       k3=3
# ==========================================================
def propensities(x1: int, x2: int, x3: int):
    # choose(n,2) = n(n-1)/2, but 0 if n<2
    c_x1_2 = (x1 * (x1 - 1)) // 2 if x1 >= 2 else 0
    c_x3_2 = (x3 * (x3 - 1)) // 2 if x3 >= 2 else 0

    a1 = 1.0 * c_x1_2 * x2
    a2 = 2.0 * x1 * c_x3_2
    a3 = 3.0 * x2 * x3
    a0 = a1 + a2 + a3
    return a1, a2, a3, a0


def pick_reaction(a1: float, a2: float, a3: float, rng: np.random.Generator):
    """Return 0/1/2 for R1/R2/R3 based on normalized propensities."""
    a0 = a1 + a2 + a3
    if a0 <= 0.0:
        return None  # no reaction can fire

    u = rng.random() * a0
    if u < a1:
        return 0
    if u < a1 + a2:
        return 1
    return 2


def apply_reaction(x1: int, x2: int, x3: int, r: int):
    """Stoichiometry updates."""
    if r == 0:   # R1
        return x1 - 2, x2 - 1, x3 + 4
    if r == 1:   # R2
        return x1 - 1, x2 + 3, x3 - 2
    if r == 2:   # R3
        return x1 + 2, x2 - 1, x3 - 1
    raise ValueError("Invalid reaction index")


def valid_state(x1: int, x2: int, x3: int) -> bool:
    return (x1 >= 0) and (x2 >= 0) and (x3 >= 0)


# ==========================================================
# PART 1(a): Long trajectory, estimate time-average of events
# C1: X1 >= 150
# C2: X2 < 10
# C3: X3 > 100
# ==========================================================
def part_a_time_average(N_steps=100_000, seed=0):
    rng = np.random.default_rng(seed)

    x1, x2, x3 = 110, 26, 55  # given initial condition

    hits = np.zeros(3, dtype=np.int64)  # [C1, C2, C3]

    for _ in range(N_steps):
        a1, a2, a3, a0 = propensities(x1, x2, x3)
        r = pick_reaction(a1, a2, a3, rng)
        if r is None:
            # System stuck (no feasible reactions)
            break

        nx1, nx2, nx3 = apply_reaction(x1, x2, x3, r)

        # If a reaction somehow produces invalid counts, stop loudly.
        # (With correct propensities, this shouldn't happen.)
        if not valid_state(nx1, nx2, nx3):
            raise RuntimeError(f"Invalid state reached: {(nx1, nx2, nx3)} from {(x1, x2, x3)} via R{r+1}")

        x1, x2, x3 = nx1, nx2, nx3

        # Check conditions AFTER update (as in your reference)
        hits[0] += (x1 >= 150)
        hits[1] += (x2 < 10)
        hits[2] += (x3 > 100)

    return hits / N_steps


# ==========================================================
# PART 1(b): Independent trials, exactly 7 reaction firings
# Starting state: (9,8,7)
# Return mean and variance of X1,X2,X3 after 7 firings
# ==========================================================
def simulate_k_firings(x0, k, rng):
    x1, x2, x3 = map(int, x0)

    for _ in range(k):
        a1, a2, a3, a0 = propensities(x1, x2, x3)
        r = pick_reaction(a1, a2, a3, rng)
        if r is None:
            # no more firings possible; stop early
            break

        x1, x2, x3 = apply_reaction(x1, x2, x3, r)
        if not valid_state(x1, x2, x3):
            raise RuntimeError("Invalid state reached; check propensity formulas and updates.")

    return x1, x2, x3


def part_b_trials(num_trials=70_000, k=7, seed=1):
    rng = np.random.default_rng(seed)
    x0 = (9, 8, 7)

    out = np.empty((num_trials, 3), dtype=np.int64)
    for i in range(num_trials):
        out[i] = simulate_k_firings(x0, k, rng)

    mean = out.mean(axis=0)
    var = out.var(axis=0)  # population variance (same as np.var default)
    return mean, var


if _name_ == "_main_":
    # ---------- Part 1(a)
    pC = part_a_time_average(N_steps=100_000, seed=42)
    print("----- PART 1(a) -----")
    print("Time-average estimates:")
    print(f"Pr(C1: X1>=150) ≈ {pC[0]:.6f}")
    print(f"Pr(C2: X2<10)   ≈ {pC[1]:.6f}")
    print(f"Pr(C3: X3>100)  ≈ {pC[2]:.6f}")

    # ---------- Part 1(b)
    mean, var = part_b_trials(num_trials=70_000, k=7, seed=99)
    print("\n----- PART 1(b) -----")
    print("After exactly 7 firings (Monte Carlo):")
    print(f"E[X1] ≈ {mean[0]:.6f},  Var[X1] ≈ {var[0]:.6f}")
    print(f"E[X2] ≈ {mean[1]:.6f},  Var[X2] ≈ {var[1]:.6f}")
    print(f"E[X3] ≈ {mean[2]:.6f},  Var[X3] ≈ {var[2]:.6f}")