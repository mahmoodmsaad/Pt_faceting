"""
Compute hBN zigzag tilt relative to the Pt step-edge direction.

This version uses the crystallographic step vector used in the supercell
construction (cell a or cell b), rather than guessing the step direction from the
topmost Pt row. That convention matches the slide/report table requested by
Maria and avoids ambiguous top-layer row choices in relaxed vicinal cells.

Tilt = minimum angle between any same-sublattice hBN B-B/N-N nearest-neighbour
direction and the Pt step vector, folded by hBN 60-degree symmetry.
"""

from pathlib import Path
import math
import re

import numpy as np
from ase import Atoms
from ase.io import read
from ase.neighborlist import neighbor_list


ROOT = Path("/leonardo_scratch/large/userexternal/mmahmood/p_inputs")
AFTER = ROOT / "cif_structures/after_relaxation"
RERUN = ROOT / "pt_rerun_uspp_vac20"

STRUCTURES = [
    ("Pt(111)", "cell a reference", AFTER / "[converged]_pt111_interface_relaxed.cif", "cif", "a"),
    ("Pt(110)", "cell b", AFTER / "[converged]_pt110_interface_relaxed.cif", "cif", "b"),
    ("Pt(221) main relaxed CIF", "cell a", AFTER / "[converged]_pt221_interface_relaxed.cif", "cif", "a"),
    (
        "Pt(221) match003 relaxed rerun",
        "cell a",
        RERUN / "pt221/pt221_match003_r1_vac20_uspp/hbn_pt221_match003_r1_uspp_relax.out",
        "qe",
        "a",
    ),
    (
        "Pt(221) match004 relaxed rerun",
        "cell a",
        RERUN / "pt221/pt221_match004_r1_vac20_uspp/hbn_pt221_match004_r1_uspp_relax.out",
        "qe",
        "a",
    ),
    ("Pt(331)", "cell b", AFTER / "[converged]_pt331_interface_relaxed.cif", "cif", "b"),
    ("Pt(441) Saad sc3", "cell a", AFTER / "[converged]_pt441_sc3_interface_relaxed.cif", "cif", "a"),
    (
        "Pt(441) Alaa Chapter 5",
        "cell b",
        RERUN / "pt441_alaa_ch5_vac20_uspp/hbn_pt441_alaa_ch5_vac20_uspp_relaxed_final.cif",
        "cif",
        "b",
    ),
    ("Pt(443) S3", "cell a", AFTER / "[converged]_pt443_s3_interface_relaxed.cif", "cif", "a"),
    ("Pt(553)", "cell a", AFTER / "[converged]_pt553_interface_relaxed.cif", "cif", "a"),
    (
        "Pt(881) old partial small cell",
        "cell a",
        AFTER / "[partial_small_cell]_pt881_small_interface_relaxed.cif",
        "cif",
        "a",
    ),
    (
        "Pt(881) match003 newly converged",
        "cell a",
        RERUN
        / "pt881/pt881_match003_r1_small_vac20_uspp/hbn_pt881_match003_r1_small_uspp_relaxed_interface.cif",
        "cif",
        "a",
    ),
    ("Pt(991) S3", "cell a", AFTER / "[converged]_pt991_s3_interface_relaxed.cif", "cif", "a"),
    (
        "Pt(991) match001",
        "cell a",
        RERUN / "pt991/pt991_match001_r1_vac20_uspp/hbn_pt991_match001_r1_uspp_relaxed_final.cif",
        "cif",
        "a",
    ),
]


def parse_cell_from_input(text):
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip().lower().startswith("cell_parameters"):
            rows = []
            for cell_line in lines[idx + 1 :]:
                parts = cell_line.split()
                if len(parts) >= 3:
                    try:
                        rows.append([float(parts[0]), float(parts[1]), float(parts[2])])
                    except ValueError:
                        pass
                if len(rows) == 3:
                    return np.array(rows, dtype=float)
    raise RuntimeError("CELL_PARAMETERS block not found")


def read_qe_relax_output(output_path):
    output_path = Path(output_path)
    input_path = output_path.parent / (output_path.name[:-4] + ".in")
    cell = parse_cell_from_input(input_path.read_text(errors="ignore"))
    text = output_path.read_text(errors="ignore")

    final = re.search(
        r"Begin final coordinates.*?ATOMIC_POSITIONS\s*\(angstrom\)\s*\n(.*?)\nEnd final coordinates",
        text,
        re.S | re.I,
    )
    if final:
        coord_lines = final.group(1).splitlines()
    else:
        blocks = list(re.finditer(r"ATOMIC_POSITIONS\s*\(angstrom\)\s*\n", text, re.I))
        if not blocks:
            raise RuntimeError("ATOMIC_POSITIONS block not found")
        coord_lines = []
        for line in text[blocks[-1].end() :].splitlines():
            parts = line.split()
            if len(parts) < 4 or not re.match(r"^[A-Z][a-z]?$", parts[0]):
                break
            coord_lines.append(line)

    symbols = []
    positions = []
    for line in coord_lines:
        parts = line.split()
        if len(parts) >= 4 and re.match(r"^[A-Z][a-z]?$", parts[0]):
            symbols.append(parts[0])
            positions.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return Atoms(symbols=symbols, positions=positions, cell=cell, pbc=True)


def inplane_angle_deg(vector):
    return float(np.degrees(np.arctan2(vector[1], vector[0])) % 180.0)


def fold_60(angle):
    folded = abs(angle) % 60.0
    return min(folded, 60.0 - folded)


def classify_tilt(label, tilt):
    if label.startswith("Pt(111)"):
        return "reference only; flat surface"
    if label.startswith("Pt(881) old partial") and 2.0 < tilt <= 2.1:
        return "small; borderline aligned"
    if math.isnan(tilt):
        return "not determined"
    if tilt <= 2.0:
        return "aligned"
    if tilt <= 10.0:
        return "small"
    if tilt <= 20.0:
        return "moderate"
    return "large"


def hbn_zigzag_angles(atoms):
    symbols = atoms.get_chemical_symbols()
    i_arr, j_arr, d_arr, d_vec_arr = neighbor_list("ijdD", atoms, cutoff=3.2)
    same_sublattice = []
    for i, j, distance, vector in zip(i_arr, j_arr, d_arr, d_vec_arr):
        if symbols[i] in ("B", "N") and symbols[i] == symbols[j] and 1.5 < distance < 3.2:
            same_sublattice.append((distance, np.array(vector)))

    if not same_sublattice:
        return []

    d_min = min(distance for distance, _ in same_sublattice)
    nearest = [vector for distance, vector in same_sublattice if distance < d_min + 0.05]

    unique_angles = []
    for vector in nearest:
        angle = inplane_angle_deg(vector)
        if not any(abs(((angle - known + 90.0) % 180.0) - 90.0) < 5.0 for known in unique_angles):
            unique_angles.append(angle)
    return sorted(unique_angles)


def measure(label, step_name, path, kind, step_axis):
    atoms = read(path) if kind == "cif" else read_qe_relax_output(path)
    symbols = atoms.get_chemical_symbols()
    bn_pairs = min(symbols.count("B"), symbols.count("N"))
    cell = atoms.cell.array if hasattr(atoms.cell, "array") else np.array(atoms.cell)
    step_vector = cell[0] if step_axis == "a" else cell[1]
    step_angle = inplane_angle_deg(step_vector)
    zigzag_angles = hbn_zigzag_angles(atoms)

    if not zigzag_angles:
        zigzag_angle = float("nan")
        tilt = float("nan")
    else:
        tilts = [fold_60(angle - step_angle) for angle in zigzag_angles]
        best = min(range(len(tilts)), key=lambda idx: tilts[idx])
        zigzag_angle = zigzag_angles[best]
        tilt = tilts[best]

    return {
        "label": label,
        "source": str(path.relative_to(ROOT)),
        "step": step_name,
        "bn_pairs": bn_pairs,
        "zigzag": zigzag_angle,
        "step_angle": step_angle,
        "tilt": tilt,
        "comment": classify_tilt(label, tilt),
    }


def fmt(value):
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        return f"{value:.2f}"
    return str(value)


def main():
    print("| Facet / structure | Source | Step vector | BN pairs | hBN zigzag dir (deg) | Pt step-edge dir (deg) | Tilt (deg) | Comment |")
    print("|---|---|---|---:|---:|---:|---:|---|")
    for row in (measure(*entry) for entry in STRUCTURES):
        print(
            "| {label} | `{source}` | {step} | {bn_pairs} | {zigzag} | {step_angle} | {tilt} | {comment} |".format(
                label=row["label"],
                source=row["source"],
                step=row["step"],
                bn_pairs=row["bn_pairs"],
                zigzag=fmt(row["zigzag"]),
                step_angle=fmt(row["step_angle"]),
                tilt=fmt(row["tilt"]),
                comment=row["comment"],
            )
        )


if __name__ == "__main__":
    main()
