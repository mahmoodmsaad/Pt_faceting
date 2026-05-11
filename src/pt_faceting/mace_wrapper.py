"""Thin wrappers around mace-torch training and inference CLIs."""

from __future__ import annotations

import subprocess
from pathlib import Path


def train_mace(train_file: str | Path, valid_file: str | Path, model_dir: str | Path) -> int:
    cmd = [
        "python",
        "-m",
        "mace.cli.run_train",
        "--train_file",
        str(train_file),
        "--valid_file",
        str(valid_file),
        "--model_dir",
        str(model_dir),
    ]
    return subprocess.run(cmd, check=False).returncode


def predict_mace(model: str | Path, structures: str | Path, output: str | Path) -> int:
    cmd = [
        "python",
        "-m",
        "mace.cli.run_eval",
        "--model",
        str(model),
        "--configs",
        str(structures),
        "--output",
        str(output),
    ]
    return subprocess.run(cmd, check=False).returncode
