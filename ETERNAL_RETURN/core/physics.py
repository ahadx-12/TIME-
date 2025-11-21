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
