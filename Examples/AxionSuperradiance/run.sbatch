#!/bin/bash
#SBATCH --job-name=axion_run
#SBATCH --account=pc_heptheory
#SBATCH --partition=lr6
#SBATCH --qos=lr_debug
#SBATCH --nodes=1
#SBATCH --ntasks=32          # full lr6 node (32 cores) for faster turnaround
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00      # headroom; expect ~20-35 min
#SBATCH --output=run_%j.out
#SBATCH --error=run_%j.err

# Re-load the build environment ON the compute node.
source /global/scratch/projects/pc_heptheory/clwelch/software/GRChombo-Axion-SR/env/lawrencium.sh

cd /global/scratch/projects/pc_heptheory/clwelch/software/GRChombo-Axion-SR/Examples/AxionSuperradiance

export OMP_NUM_THREADS=1     # pure MPI

mkdir -p hdf5 pout data      # output subdirs (defensive; usually auto-created)

mpirun ./Main_AxionSuperradiance3d.Linux.64.mpicxx.gfortran.OPTHIGH.MPI.ex params.txt
