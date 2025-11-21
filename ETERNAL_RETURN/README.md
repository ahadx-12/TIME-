# ETERNAL_RETURN: Project Nietzsche

A Streamlit dashboard that fuses Gödel-like rotating spacetime geometry with Nietzsche's idea of the eternal return. It visualizes light-cone tipping, estimates the onset of closed timelike curves (CTCs), and runs Monte Carlo experiments that show how information complexity suppresses self-consistent time loops.

## Conceptual overview
- **Gödel-like spacetime permits CTCs.** A rotating metric tips light cones until closed paths in the angular direction become timelike.
- **Critical radius detection.** We sample the metric to estimate the radius where φ-loops switch from causal to timelike (the emergence of the CTC region).
- **Information-theoretic constraints.** Monte Carlo simulations model how noisy, complex states struggle to remain self-consistent across a time loop—high entropy kills the return.

## Running the app locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch Streamlit:
   ```bash
   streamlit run app/main.py
   ```
3. Use the sidebar controls to set the universal rotation `ω`, the entropy sweep, and noise. Tab 1 shows the light-cone geometry and critical radius; Tab 2 plots survival probability versus complexity with status messaging.

## Testing
Run the full test suite with:
```bash
pytest
```

## Deployment (Railway)
The repository includes `Procfile` and `runtime.txt` to support Railway deployment. Deploy by pointing Railway at this repo; it will install `requirements.txt`, honor the Python runtime, and execute the Procfile command to start Streamlit.

## Current headline results
- For `ω = 0.5`, the estimated critical radius is `r_crit ≈ 1.414`, marking the onset of closed timelike curves.
- With noise level `0.5`, survival probability drops from ~0.47 at complexity 1 to ~0.033 by complexity 5, and reaches 0 by complexity 200—high entropy effectively forbids eternal return.
