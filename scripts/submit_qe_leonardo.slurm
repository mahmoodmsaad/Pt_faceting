#!/bin/bash
#SBATCH --job-name=qe-hbn-pt
#SBATCH --partition=boost_usr_prod
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --time=24:00:00
#SBATCH --output=qe_%j.out

module load quantum-espresso
srun pw.x -in qe_input.in > qe_output.out
