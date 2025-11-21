from pathlib import Path

import numpy as np


class GodelUniverse:
    """Simplified Gödel-like metric utilities.

    The metric follows a rotating-universe form with coordinates
    (t, r, φ, z) ordered as (0, 1, 2, 3). The off-diagonal term
    between t and φ introduces rotation, while the φφ component
    depends on radius to mimic closed timelike curve structure.
    """

    def __init__(self, omega: float, R: float | None = None):
        """
        Parameters
        ----------
        omega:
            Rotation parameter controlling the scale relationship for R.
        R:
            Scale parameter; if ``None`` we set ``R = 1 / omega``.
        """
        if omega == 0:
            raise ValueError("omega must be non-zero to define a rotating metric")

        self.omega = float(omega)
        self.R = float(R) if R is not None else 1.0 / self.omega

    def metric_tensor(self, r: float) -> np.ndarray:
        r"""Return the 4x4 metric tensor :math:`g_{\mu\nu}` at radius ``r``.

        The coordinate ordering is (t, r, φ, z).
        """
        R = self.R

        g = np.zeros((4, 4), dtype=float)
        # g_tt
        g[0, 0] = -1.0
        # g_rr
        g[1, 1] = 1.0
        # g_φφ
        g[2, 2] = -(r**2 - (R**2) / (r**2))
        # g_tφ and g_φt (off-diagonal)
        g[0, 2] = g[2, 0] = -R / (r**2)
        # g_zz
        g[3, 3] = 1.0

        return g

    def interval_squared(self, dt, dr, dphi, dz, r: float) -> float:
        r"""Compute :math:`ds^2 = g_{\mu\nu} dx^\mu dx^\nu` at radius ``r``."""
        g = self.metric_tensor(r)
        dx = np.array([dt, dr, dphi, dz], dtype=float)
        return float(dx @ g @ dx)

    def is_timelike(self, dt, dr, dphi, dz, r: float) -> bool:
        """Return ``True`` when the interval is timelike (``ds^2 < 0``)."""
        ds2 = self.interval_squared(dt, dr, dphi, dz, r)
        return ds2 < 0.0

    def is_phi_loop_timelike(self, r: float, dphi: float = 1.0) -> bool:
        """Check whether a closed loop in ``φ`` at radius ``r`` is timelike.

        This uses the approximation ``dt = dr = dz = 0`` with a small ``dphi``
        increment to probe the sign of ``ds^2`` for the loop.
        """
        ds2 = self.interval_squared(dt=0.0, dr=0.0, dphi=dphi, dz=0.0, r=r)
        return ds2 < 0.0

    def find_critical_radius(self, r_min=0.1, r_max=10.0, steps=1000) -> float | None:
        """Search for the radius where φ-loops transition to timelike.

        The scan checks the sign of the loop interval across uniformly spaced
        radii and performs a short bisection refinement when a sign change is
        detected. Returns an approximate ``r_crit`` or ``None`` if no
        transition is found within the range.
        """
        radii = np.linspace(r_min, r_max, steps)
        previous = self.is_phi_loop_timelike(radii[0])

        for r in radii[1:]:
            current = self.is_phi_loop_timelike(r)
            if current != previous:
                low, high = (r - (radii[1] - radii[0]), r)
                for _ in range(20):
                    mid = 0.5 * (low + high)
                    if self.is_phi_loop_timelike(mid) == previous:
                        low = mid
                    else:
                        high = mid
                return 0.5 * (low + high)
        return None


def log_transition_examples(log_path: str | Path | None = None) -> None:
    """Compute sample critical radii and append results to a log file."""
    if log_path is None:
        project_root = Path(__file__).resolve().parent.parent
        log_path = project_root / "transition_log.txt"

    entries = []
    for omega in (0.5, 1.0):
        gu = GodelUniverse(omega=omega)
        r_crit = gu.find_critical_radius()
        entries.append(f"omega={omega}, r_crit={r_crit}\n")

    with open(log_path, "a", encoding="utf-8") as handle:
        handle.writelines(entries)


if __name__ == "__main__":
    log_transition_examples()
