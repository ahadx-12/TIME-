import numpy as np


class TimeLoopConsistency:
    """Simulate self-consistency of states traversing a time loop.

    The model is deliberately simple: states are represented as binary arrays.
    A loop evolves the state by flipping bits according to a Bernoulli noise
    process. Surviving the loop requires the state to be unchanged after the
    evolution step, which becomes increasingly unlikely as complexity grows or
    as the noise level rises.
    """

    def __init__(self, rng_seed: int | None = None):
        self.rng = np.random.default_rng(rng_seed)

    def generate_state(self, complexity_score: int) -> np.ndarray:
        """Generate a binary state of length ``complexity_score``.

        Complexity is represented purely by length; entries are uniformly
        random 0/1 values.
        """

        if complexity_score < 0:
            raise ValueError("complexity_score must be non-negative")

        return self.rng.integers(0, 2, size=complexity_score, dtype=np.int8)

    def evolve_state(self, state: np.ndarray, noise_level: float) -> np.ndarray:
        """Apply noisy evolution via random bit flips.

        Each bit flips independently with probability ``noise_level``.
        """

        if not 0.0 <= noise_level <= 1.0:
            raise ValueError("noise_level must be between 0 and 1")

        flips = self.rng.random(size=state.shape) < noise_level
        new_state = state.copy()
        new_state[flips] = 1 - new_state[flips]
        return new_state

    def simulate_loop(self, complexity_score: int, noise_level: float) -> bool:
        """Return ``True`` when the state survives one noisy loop unchanged."""

        state_initial = self.generate_state(complexity_score)
        state_final = self.evolve_state(state_initial, noise_level)
        return np.array_equal(state_initial, state_final)
