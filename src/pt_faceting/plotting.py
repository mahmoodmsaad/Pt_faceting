"""Plotting helpers for PDOS data."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from .parsers import parse_projwfc_output


def plot_pdos(projwfc_file: str | Path, output_png: str | Path) -> str:
    data = parse_projwfc_output(projwfc_file)
    plt.figure(figsize=(6, 4))
    plt.plot(data["energy_ev"], data["density"], lw=1.5)
    plt.xlabel("Energy (eV)")
    plt.ylabel("PDOS (arb. units)")
    plt.tight_layout()
    out = str(output_png)
    plt.savefig(out, dpi=200)
    plt.close()
    return out
