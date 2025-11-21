import pandas as pd

from core.entropy import TimeLoopConsistency


def run_batch_simulation(
    max_complexity: int = 200,
    iterations: int = 500,
    noise_level: float = 0.5,
    rng_seed: int | None = 123,
) -> pd.DataFrame:
    """Estimate survival rates across a sweep of state complexities.

    For each complexity from 1 to ``max_complexity`` inclusive, simulate a
    number of loop traversals and compute the fraction that remain unchanged.
    Results are returned as a :class:`pandas.DataFrame` and also written to a
    CSV file named ``simulation_results.csv`` in the working directory.
    """

    if max_complexity < 1:
        raise ValueError("max_complexity must be at least 1")
    if iterations < 1:
        raise ValueError("iterations must be at least 1")

    tlc = TimeLoopConsistency(rng_seed=rng_seed)
    records = []

    for complexity in range(1, max_complexity + 1):
        successes = 0
        for _ in range(iterations):
            if tlc.simulate_loop(complexity_score=complexity, noise_level=noise_level):
                successes += 1
        survival_rate = successes / iterations
        records.append({
            "complexity": complexity,
            "survival_rate": survival_rate,
        })

    df = pd.DataFrame(records)
    df.to_csv("simulation_results.csv", index=False)
    return df
