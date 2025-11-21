import numpy as np
import plotly.graph_objects as go

from core.physics import GodelUniverse


def generate_light_cone_vectors(omega: float, n_radii: int = 5):
    """Generate positions and direction vectors representing light cones.

    The cones are arranged along the x-axis with increasing radius. A heuristic
    tilt factor increases with radius, making cones more horizontal as they
    approach the critical radius returned by ``GodelUniverse``.
    """
    gu = GodelUniverse(omega=omega)
    r_crit = gu.find_critical_radius() or 5.0

    radii = np.linspace(0.0, r_crit, n_radii)
    xs, ys, zs = [], [], []
    u, v, w = [], [], []

    for r in radii:
        # Place cones along x-axis for visualization (y=0)
        x = r
        y = 0.0
        z = 0.0

        # Heuristic tilt: at r=0 -> mostly vertical; at r=r_crit -> mostly horizontal
        tilt_factor = min(r / (r_crit + 1e-6), 1.0)
        # Spatial length vs time component
        spatial_mag = tilt_factor
        time_mag = 1.0 - 0.7 * tilt_factor  # never fully vanish, just for aesthetics

        xs.append(x)
        ys.append(y)
        zs.append(0.0)

        u.append(spatial_mag)   # x-direction
        v.append(0.0)           # y-direction
        w.append(time_mag)      # t-direction

    return xs, ys, zs, u, v, w, r_crit


def render_light_cones(omega: float):
    """Render a Plotly 3D figure showing light cone tilting."""
    xs, ys, zs, u, v, w, r_crit = generate_light_cone_vectors(omega)

    fig = go.Figure()

    fig.add_trace(
        go.Cone(
            x=xs,
            y=ys,
            z=zs,
            u=u,
            v=v,
            w=w,
            sizemode="absolute",
            sizeref=0.5,
            colorscale=[[0, "#00FFFF"], [1, "#00FFFF"]],
            showscale=False,
            name="Light Cones",
        )
    )

    # Add critical radius marker as a red ring in x-y plane (z=0)
    theta = np.linspace(0, 2 * np.pi, 100)
    ring_x = r_crit * np.cos(theta)
    ring_y = r_crit * np.sin(theta)

    fig.add_trace(
        go.Scatter3d(
            x=ring_x,
            y=ring_y,
            z=[0.0] * len(theta),
            mode="lines",
            line=dict(color="#FF0000", width=4),
            name="Critical Radius",
        )
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="Space X",
            yaxis_title="Space Y",
            zaxis_title="Time",
            xaxis=dict(backgroundcolor="#0e1117", gridcolor="#444"),
            yaxis=dict(backgroundcolor="#0e1117", gridcolor="#444"),
            zaxis=dict(backgroundcolor="#0e1117", gridcolor="#444"),
        ),
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="#f5f5f5"),
        title="Spacetime Light Cones in Gödel-like Universe",
    )

    return fig
