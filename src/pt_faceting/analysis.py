"""Analysis helpers for adsorption energetics and geometry."""

from __future__ import annotations

import math


def compute_adsorption_energy(interface_energy: float, slab_energy: float, hbn_energy: float) -> float:
    """Compute adsorption energy as E(interface) - E(slab) - E(hBN)."""
    return float(interface_energy - slab_energy - hbn_energy)


def tilt_angle_degrees(zigzag_vector, step_edge_vector) -> float:
    """Return the angle between hBN zigzag and Pt step-edge vectors in degrees."""
    zz = [float(v) for v in zigzag_vector]
    se = [float(v) for v in step_edge_vector]
    zz_norm = math.sqrt(sum(v * v for v in zz))
    se_norm = math.sqrt(sum(v * v for v in se))
    if zz_norm == 0 or se_norm == 0:
        raise ValueError("Vectors must be non-zero")
    cosine = sum(a * b for a, b in zip(zz, se)) / (zz_norm * se_norm)
    cosine = max(-1.0, min(1.0, cosine))
    return math.degrees(math.acos(cosine))
