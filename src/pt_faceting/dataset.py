"""Dataset utilities for converting QE-relax snapshots to extxyz."""

from __future__ import annotations

import json
from pathlib import Path


def build_training_extxyz(input_json: str | Path, output_extxyz: str | Path) -> int:
    """Build extxyz from JSON records with symbols, positions, cell, and energy."""
    from ase import Atoms
    from ase.io import write

    records = json.loads(Path(input_json).read_text(encoding="utf-8"))
    atoms_list = []
    for i, rec in enumerate(records):
        for key in ("symbols", "positions"):
            if key not in rec:
                raise ValueError(f"Missing required field '{key}' in record index {i}")
        atoms = Atoms(symbols=rec["symbols"], positions=rec["positions"], cell=rec.get("cell"), pbc=rec.get("pbc", True))
        if "energy" in rec:
            atoms.info["energy"] = rec["energy"]
        if "forces" in rec:
            atoms.arrays["forces"] = rec["forces"]
        if "stress" in rec:
            atoms.info["stress"] = rec["stress"]
        atoms_list.append(atoms)

    write(str(output_extxyz), atoms_list, format="extxyz")
    return len(atoms_list)
