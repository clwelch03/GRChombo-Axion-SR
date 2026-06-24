#!/bin/bash
#SBATCH --job-name=axion_smoke
#SBATCH --account=pc_heptheory
#SBATCH --partition=lr6
#SBATCH --qos=lr_debug
#SBATCH --nodes=1
#SBATCH --ntasks=8           # 8 MPI ranks on one node
#SBATCH --cpus-per-task=1
#SBATCH --time=00:15:00      # well under the 3h lr_debug cap
#SBATCH --output=smoke_%j.out   # %j = job ID
#SBATCH --error=smoke_%j.err

# Re-load the build environment ON the compute node (login-node modules
# don't carry over to compute nodes).
source /global/scratch/projects/pc_heptheory/clwelch/software/GRChombo-Axion-SR/env/lawrencium.sh

cd /global/scratch/projects/pc_heptheory/clwelch/software/GRChombo-Axion-SR/Examples/AxionSuperradiance

export OMP_NUM_THREADS=1     # pure MPI for this test

mkdir -p hdf5 pout data      # output subdirs (defensive; usually auto-created)

mpirun ./Main_AxionSuperradiance3d.Linux.64.mpicxx.gfortran.OPTHIGH.MPI.ex params_smoke.txt
