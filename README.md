# Pt_faceting

Computational materials-science workflow for **hBN adsorption on vicinal Pt surfaces** that combines:

- **DFT (Quantum ESPRESSO on Leonardo/CINECA)** with PBE + DFT-D3, ultrasoft PSLibrary pseudopotentials, `ecutwfc=80 Ry`, `ecutrho=640 Ry`
- **MACE machine-learning interatomic potentials** for accelerated facet/supercell screening

Target Pt facets: Pt(111), Pt(110), Pt(221), Pt(331), Pt(441), Pt(443), Pt(553), Pt(881), Pt(991), with focus on experimentally stable facets grown on curved Pt(331).

## Repository layout

- `data/` – CIF structures and training `extxyz`
- `src/pt_faceting/` – QE parsers, adsorption/tilt analysis, MACE wrappers
- `scripts/` – SLURM submission examples for Leonardo
- `notebooks/` – Jupyter analysis notebooks
- `tests/` – focused unit tests for core analysis/parsing logic

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## CLI entry points

- `parse_qe_output <pw.out> [--projwfc_output projwfc.out]`
- `build_training_set <records.json> <training.extxyz>`
- `train_mace <train.extxyz> <valid.extxyz> <model_dir>`
- `predict_adsorption --interface_energy Eint --slab_energy Eslab --hbn_energy Ehbn`
- `predict_adsorption --model model.pt --structures scan.extxyz --output pred.json`
- `plot_pdos <projwfc.out> <pdos.png>`

## Reproducing the workflow

1. Run QE slab/interface calculations (`pw.x`) and projected DOS (`projwfc.x`) on Leonardo.
2. Parse outputs with `parse_qe_output` and compute adsorption energies with `Eads = E(interface) - E(slab) - E(hBN)`.
3. Build train/validation/test `extxyz` from relaxed DFT trajectories via `build_training_set`.
4. Train MACE (`train_mace`) and evaluate on held-out structures (`predict_adsorption`).
5. Compare DFT vs MACE trends for adsorption energies, equilibrium geometry, hBN–Pt distance, and PDOS-related indicators.
6. Use trained MACE to scan larger facet models that are too expensive for direct DFT.

## Citation

```bibtex
@article{bakhit_hbn_pt_faceting,
  author  = {Bakhit, et al.},
  title   = {hBN growth on curved Pt(331): facet-dependent adsorption and stability},
  journal = {Please update with final publication metadata},
  year    = {202X}
}
```
