# hBN zigzag tilt relative to Pt step edge

This report measures the in-plane tilt angle between the hBN zigzag direction
and the Pt step-edge direction. The first table uses relaxed Pt(hkl)/hBN
structures; the second table checks the unrelaxed/start CIFs.

## Method

- **hBN zigzag direction**: nearest same-sublattice B-B / N-N vectors in the relaxed hBN sheet (period ~ a_hBN = 2.515 Å)
- **Pt step-edge direction**: the crystallographic supercell vector used to set the step edge during construction (`cell a` or `cell b`, listed below)
- **Tilt angle**: minimum hBN zigzag-step angle, folded by hBN 60° symmetry
- **Classification**: `aligned` = 0–2°, `small` = 2–10°, `moderate` = 10–20°, `large` = >20°
- **Experimental expectation** (LEED/STM, Bakhit et al.): hBN zigzag aligned with step → tilt ≈ 0–2°

## Combined table — tilt angle and adsorption energy

| Facet / cell | Step vec | BN pairs | Tilt (°) | Class | E_ads/BN (eV) | Notes |
|---|:--:|:---:|:---:|---|:---:|---|
| Pt(111) | a (ref) | 21 | 10.72 | (no step) | −0.208 | flat — no real step edge |
| Pt(110) | b | 33 | 11.49 | moderate | −0.625 | strong binder |
| Pt(221) main (60-atom small) | a | 16 | **4.51** | **small** | −0.373 | high hBN strain (+10%) |
| **Pt(221) match003** ⭐ NEW | a | 50 | **29.27** | **LARGE** | **−0.180** | low mismatch, **rotated** |
| **Pt(221) match004** ⭐ NEW | a | 34 | **28.73** | **LARGE** | **−0.184** | low mismatch, **rotated** |
| Pt(331) | b | 50 | 16.67 | moderate | −0.183 | unstable |
| Pt(441) Saad sc3 | a | 129 | 23.07 | LARGE | −0.232 | |
| Pt(441) Alaa Chapter-5 rerun | b | 36 | 29.45 | LARGE | −0.250 | |
| Pt(443) S3 | a | 84 | 28.38 | LARGE | −0.181 | unstable |
| Pt(553) | a | 85 | 22.74 | LARGE | −0.160 | unstable |
| **Pt(881) old partial small** | a | 14 | **2.03** | **ALIGNED** ✓ | (small cell) | high mismatch but step-aligned |
| **Pt(881) match003 small** ⭐ NEW | a | 64 | **22.86** | **LARGE** | **−0.285** | low mismatch, **rotated** |
| Pt(991) old S3 | a | 84 | 28.83 | LARGE | −0.271 | |
| Pt(991) match001 | a | 73 | 22.08 | LARGE | −0.216 | |

## Unrelaxed / start CIF check

This checks whether the rotation was already present in the starting
geometries. For most structures, the tilt changes very little after relaxation,
so the large tilts mainly come from the chosen supercell/orientation.

| Unrelaxed / start structure | Source file | Step vec | BN pairs | hBN zigzag dir (°) | Pt step-edge dir (°) | Tilt (°) | Comment |
|---|---|:--:|:---:|:---:|:---:|:---:|---|
| Pt(111) initial | `cif_structures/before_relaxation/[converged]_pt111_interface_initial.cif` | a (ref) | 21 | 49.11 | 0.00 | 10.89 | reference only; flat surface |
| Pt(110) initial | `cif_structures/before_relaxation/[converged]_pt110_interface_initial.cif` | b | 33 | 78.57 | 90.00 | 11.43 | moderate |
| Pt(221) main initial | `cif_structures/before_relaxation/[converged]_pt221_interface_initial.cif` | a | 16 | 56.31 | 0.00 | 3.69 | small |
| Pt(221) match003 start | `pt_rerun_uspp_vac20/pt221/pt221_match003_r1_vac20_uspp/hbn_pt221_match003_r1_uspp_start.cif` | a | 50 | 90.80 | 0.00 | 29.20 | large |
| Pt(221) match004 start | `pt_rerun_uspp_vac20/pt221/pt221_match004_r1_vac20_uspp/hbn_pt221_match004_r1_uspp_start.cif` | a | 34 | 91.19 | 0.00 | 28.81 | large |
| Pt(221) bigger match001 initial | `pt_rerun_uspp_vac20/pt221/pt_bigger_supercell/match_001_r1_interface_half_layers.cif` | a | 137 | 76.87 | 0.00 | 16.87 | moderate |
| Pt(331) initial | `cif_structures/before_relaxation/[converged]_pt331_interface_initial.cif` | b | 50 | 60.16 | 77.08 | 16.92 | moderate |
| Pt(441) initial | `cif_structures/before_relaxation/[converged]_pt441_interface_initial.cif` | a | 129 | 23.06 | 0.00 | 23.06 | large |
| Pt(441) Saad sc3 start | `pt_rerun_uspp_vac20/pt441/pt441_sc3_vac20/hbn_pt441_sc3_relax_start.cif` | a | 129 | 23.05 | 0.00 | 23.05 | large |
| Pt(443) initial | `cif_structures/before_relaxation/[converged]_pt443_interface_initial.cif` | a | 84 | 148.62 | 0.00 | 28.62 | large |
| Pt(443) S3 start | `pt_rerun_uspp_vac20/pt443/pt443_s3_vac20/hbn_pt443_s3_relax_start.cif` | a | 84 | 31.38 | 0.00 | 28.62 | large |
| Pt(553) initial | `cif_structures/before_relaxation/[converged]_pt553_interface_initial.cif` | a | 85 | 82.58 | 0.00 | 22.58 | large |
| Pt(553) start | `pt_rerun_uspp_vac20/pt553/hbn_pt553_relax_start.cif` | a | 85 | 82.58 | 0.00 | 22.58 | large |
| Pt(881) old partial initial | `cif_structures/before_relaxation/[partial_small_cell]_pt881_interface_initial.cif` | a | 14 | 58.35 | 0.00 | 1.65 | aligned |
| Pt(881) match003 small start | `pt_rerun_uspp_vac20/pt881/pt881_match003_r1_small_vac20_uspp/hbn_pt881_match003_r1_small_uspp_start.cif` | a | 64 | 97.03 | 0.00 | 22.97 | large |
| Pt(881) match003 large start | `pt_rerun_uspp_vac20/pt881/pt881_match003_r1_vac20/hbn_pt881_match003_r1_relax_start.cif` | a | 64 | 97.03 | 0.00 | 22.97 | large |
| Pt(881) S3 start | `pt_rerun_uspp_vac20/pt881/pt881_s3_vac20/hbn_pt881_s3_relax_start.cif` | a | 150 | 31.54 | 0.00 | 28.46 | large |
| Pt(991) initial | `cif_structures/before_relaxation/[converged]_pt991_interface_initial.cif` | a | 84 | 31.81 | 0.00 | 28.19 | large |
| Pt(991) match001 start | `pt_rerun_uspp_vac20/pt991/pt991_match001_r1_vac20_uspp/hbn_pt991_match001_r1_uspp_start.cif` | a | 73 | 81.97 | 0.00 | 21.97 | large |
| Pt(991) S3 initial CIF | `pt_rerun_uspp_vac20/pt991/pt991_s3_vac20_uspp/pt991_interface_S3.cif` | a | 84 | 31.30 | 0.00 | 28.70 | large |

## Short interpretation for Maria

### The experimental expectation
Experimentally, hBN aligns its zigzag chains parallel to the Pt step edges
(tilt ≈ 0–2°), because B atoms bond directly to Pt step-edge atoms — and that
geometry is only available when the zigzag runs along the step.

### What we find in the DFT structures

- **Only one cell is genuinely step-aligned**: the old partial Pt(881) small
  cell, with tilt ≈ 2°.
- **Almost every other cell has a large tilt** (>20°), regardless of vicinal
  angle, BN-pair count, or stable/unstable classification.
- **The new low-mismatch cells (Pt(221) match003, match004; Pt(881) match003
  small; Pt(991) match001) all have large tilts** — even though their lattice
  matching is much better than the older constructions.
- **Pt(441) Alaa Chapter-5 and Saad sc3 are both large-tilt** (29.45° and 23.07°),
  so the Pt(441) Eads disagreement may be partly geometric and not just from
  parameters.

### Implication

For the relaxed rerun structures, **several of the most different Eads results
are systematically associated with large hBN zigzag-step tilt**. The DFT supercells
we built force hBN into a rotated configuration that does not match the
experimental step-aligned binding geometry. That alone could account for a
significant fraction of the energy disagreement with Alaa's Chapter 5 and with
experiment, even before we discuss pseudopotentials or cutoffs.

### What this suggests doing next

1. For the cells where tilt is large, build alternative supercells where the
   hBN zigzag is **forced** to lie along the step direction (constrained
   integer-matrix search with a tilt < 5° constraint).
2. Re-relax those step-aligned variants with the same project parameters and
   compare Eads.
3. If Eads moves significantly toward Alaa's values when tilt is small, that
   confirms Maria's hypothesis: the discrepancies are dominated by hBN
   orientation, not by pseudopotentials.
