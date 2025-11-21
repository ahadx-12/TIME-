"""Phase diagram experiment combining Gödel geometry and loop consistency.

This script scans over rotation strength (omega) and noise level (eta) to
construct a loop-support index L(omega, eta) that multiplies geometric
permission for closed timelike curves with an information-theoretic survival
probability. Results are written to ``phase_diagram_results.csv`` and an
optional heatmap ``phase_diagram_heatmap.png`` if plotting succeeds.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from core.physics import GodelUniverse
from core.simulation import run_batch_simulation


OMEGAS = np.linspace(0.1, 2.0, 10)
NOISE_LEVELS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
COMPLEXITIES = [100, 150, 200, 250, 300]
EPSILON_LOW = 0.01
EPSILON_HIGH = 0.20
RESULTS_CSV = Path("phase_diagram_results.csv")
HEATMAP_PATH = Path("phase_diagram_heatmap.png")


def _extract_survival_mean(df: pd.DataFrame, complexities: Iterable[int]) -> float:
    """Average survival rates for a subset of complexities.

    The helper looks up the survival rate for each requested complexity. If an
    exact row is missing, it falls back to the nearest available complexity.
    The mean of the collected survival rates is returned.
    """

    available = df.set_index("complexity")
    collected: list[float] = []

    for target in complexities:
        if target in available.index:
            collected.append(float(available.loc[target, "survival_rate"]))
            continue

        # Fallback to nearest complexity if the exact value is absent.
        nearest_idx = (available.index.to_series().sub(target).abs()).idxmin()
        collected.append(float(available.loc[nearest_idx, "survival_rate"]))

    return float(np.mean(collected)) if collected else float("nan")


def compute_information_index(noise_level: float, complexities: Iterable[int]) -> float:
    """Compute L_info(eta) by averaging survival probabilities."""

    df = run_batch_simulation(
        max_complexity=max(complexities),
        iterations=1000,
        noise_level=noise_level,
    )
    return _extract_survival_mean(df, complexities)


def determine_phase(geometry_has_ctc: bool, L_combined: float) -> str:
    """Assign a phase label based on geometry and loop-support index."""

    if not geometry_has_ctc:
        return "Linear Phase"
    if L_combined <= EPSILON_LOW:
        return "Frustrated Circular Phase"
    if L_combined >= EPSILON_HIGH:
        return "Circular Time Phase"
    return "Intermediate / Crossover"


def generate_phase_diagram() -> pd.DataFrame:
    """Compute the phase diagram grid and persist to CSV."""

    results: list[dict[str, float | bool | str | None]] = []

    # Precompute information index for each noise level (geometry-independent).
    info_index = {
        eta: compute_information_index(eta, COMPLEXITIES)
        for eta in NOISE_LEVELS
    }

    for omega in OMEGAS:
        gu = GodelUniverse(omega=omega)
        r_crit = gu.find_critical_radius()
        geometry_has_ctc = r_crit is not None
        geometry_flag = 1 if geometry_has_ctc else 0

        for eta in NOISE_LEVELS:
            L_info = info_index[eta]
            L_combined = geometry_flag * L_info
            phase = determine_phase(geometry_has_ctc, L_combined)

            results.append(
                {
                    "omega": float(omega),
                    "noise": float(eta),
                    "r_crit": float(r_crit) if r_crit is not None else None,
                    "geometry_has_ctc": geometry_has_ctc,
                    "L_info": float(L_info),
                    "L_combined": float(L_combined),
                    "phase": phase,
                }
            )

    df_results = pd.DataFrame(results)
    df_results.to_csv(RESULTS_CSV, index=False)
    return df_results


def maybe_plot_heatmap(df_results: pd.DataFrame) -> None:
    """Attempt to save a heatmap of L_combined; warn gracefully if plotting fails."""

    try:
        import plotly.express as px

        pivot = df_results.pivot(index="noise", columns="omega", values="L_combined")
        geometry_mask = df_results.pivot(index="noise", columns="omega", values="geometry_has_ctc")

        fig = px.imshow(
            pivot.sort_index(ascending=False),
            color_continuous_scale="Viridis",
            origin="lower",
            aspect="auto",
            labels={"color": "L_combined"},
        )

        # Add text annotations to highlight regions without CTC geometry.
        text_values = []
        for eta in pivot.index:
            row_text = []
            for omega in pivot.columns:
                if geometry_mask.loc[eta, omega]:
                    row_text.append(f"{pivot.loc[eta, omega]:.2f}")
                else:
                    row_text.append("no CTC")
            text_values.append(row_text)

        fig.update_traces(text=text_values, texttemplate="%{text}", hovertemplate="omega=%{x}<br>noise=%{y}<br>L_combined=%{z}<extra></extra>")
        fig.update_layout(title="Loop-support index L(omega, eta)")

        fig.write_image(str(HEATMAP_PATH))
    except Exception as exc:  # pragma: no cover - plotting is optional
        print(f"[warning] Plotting skipped: {exc}")


def main() -> None:
    df_results = generate_phase_diagram()
    maybe_plot_heatmap(df_results)
    print(df_results.head())
    print(f"Saved results to {RESULTS_CSV.resolve()}")
    if HEATMAP_PATH.exists():
        print(f"Saved heatmap to {HEATMAP_PATH.resolve()}")


if __name__ == "__main__":
    main()
