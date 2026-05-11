#!/bin/bash
#SBATCH --job-name=mace-hbn-pt
#SBATCH --partition=boost_usr_prod
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-node=1
#SBATCH --time=12:00:00
#SBATCH --output=mace_%j.out

python -m mace.cli.run_train --train_file data/training/train.extxyz --valid_file data/training/valid.extxyz --model_dir models
