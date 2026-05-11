"""Parsers for Quantum ESPRESSO pw.x and projwfc.x text outputs."""

from __future__ import annotations

import re
from pathlib import Path

ENERGY_RE = re.compile(r"!\s+total energy\s+=\s+([-+]?\d*\.?\d+)\s+Ry")
FERMI_RE = re.compile(r"the Fermi energy is\s+([-+]?\d*\.?\d+)\s+ev", re.IGNORECASE)


def parse_pw_output(path: str | Path) -> dict:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    energies = [float(v) for v in ENERGY_RE.findall(text)]
    fermi = None
    m = FERMI_RE.search(text)
    if m:
        fermi = float(m.group(1))
    return {
        "file": str(path),
        "total_energy_ry": energies[-1] if energies else None,
        "total_energy_history_ry": energies,
        "fermi_energy_ev": fermi,
    }


def parse_projwfc_output(path: str | Path) -> dict:
    rows = []
    for line in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        parts = line.split()
        if len(parts) >= 2:
            try:
                rows.append((float(parts[0]), float(parts[1])))
            except ValueError:
                continue
    return {
        "file": str(path),
        "energy_ev": [r[0] for r in rows],
        "density": [r[1] for r in rows],
    }
