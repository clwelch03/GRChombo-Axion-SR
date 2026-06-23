#!/usr/bin/env bash
# Environment for building and running GRChombo on Lawrencium.
# Usage: source env/lawrencium.sh

module purge
module load gcc/11.4.0
module load openmpi/4.1.6
module load hdf5/1.14.3
module load intel-oneapi-mkl/2023.2.0

export CHOMBO_HOME=/global/scratch/projects/pc_heptheory/clwelch/software/Chombo/lib
export GRCHOMBO_SOURCE=/global/scratch/projects/pc_heptheory/clwelch/software/GRChombo-Axion-SR

echo "GRChombo environment loaded."
echo "  CHOMBO_HOME=$CHOMBO_HOME"
echo "  GRCHOMBO_SOURCE=$GRCHOMBO_SOURCE"
