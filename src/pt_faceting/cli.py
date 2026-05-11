"""CLI entry points for Pt faceting workflow."""

from __future__ import annotations

import argparse
import json

from .analysis import compute_adsorption_energy
from .parsers import parse_projwfc_output, parse_pw_output


def parse_qe_output_cmd() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("pw_output")
    p.add_argument("--projwfc_output")
    args = p.parse_args()
    out = {"pw": parse_pw_output(args.pw_output)}
    if args.projwfc_output:
        out["projwfc"] = parse_projwfc_output(args.projwfc_output)
    print(json.dumps(out, indent=2))


def build_training_set_cmd() -> None:
    from .dataset import build_training_extxyz

    p = argparse.ArgumentParser()
    p.add_argument("input_json")
    p.add_argument("output_extxyz")
    args = p.parse_args()
    n = build_training_extxyz(args.input_json, args.output_extxyz)
    print(f"Wrote {n} structures to {args.output_extxyz}")


def train_mace_cmd() -> None:
    from .mace_wrapper import train_mace

    p = argparse.ArgumentParser()
    p.add_argument("train_file")
    p.add_argument("valid_file")
    p.add_argument("model_dir")
    args = p.parse_args()
    raise SystemExit(train_mace(args.train_file, args.valid_file, args.model_dir))


def predict_adsorption_cmd() -> None:
    from .mace_wrapper import predict_mace

    p = argparse.ArgumentParser()
    p.add_argument("--interface_energy", type=float)
    p.add_argument("--slab_energy", type=float)
    p.add_argument("--hbn_energy", type=float)
    p.add_argument("--model")
    p.add_argument("--structures")
    p.add_argument("--output")
    args = p.parse_args()

    if args.interface_energy is not None and args.slab_energy is not None and args.hbn_energy is not None:
        print(compute_adsorption_energy(args.interface_energy, args.slab_energy, args.hbn_energy))
        return

    if args.model and args.structures and args.output:
        raise SystemExit(predict_mace(args.model, args.structures, args.output))

    raise SystemExit(
        "Provide either (--interface_energy, --slab_energy, --hbn_energy) "
        "or (--model, --structures, --output)."
    )


def plot_pdos_cmd() -> None:
    from .plotting import plot_pdos

    p = argparse.ArgumentParser()
    p.add_argument("projwfc_file")
    p.add_argument("output_png")
    args = p.parse_args()
    print(plot_pdos(args.projwfc_file, args.output_png))
