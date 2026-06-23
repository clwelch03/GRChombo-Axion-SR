# GRChombo-Axion-SR

Numerical GR simulations of axion superradiance around black holes, built on GRChombo.
This repo is a fork of GRTLCollaboration/GRChombo. Physics code lives in Examples/AxionSuperradiance/.

## Cluster: Lawrencium (LBNL)

Always load the environment before building or running anything:

```bash
source env/lawrencium.sh
```

This loads gcc/11.4.0, openmpi/4.1.6, hdf5/1.14.3, intel-oneapi-mkl/2023.2.0,
and sets CHOMBO_HOME and GRCHOMBO_SOURCE.

## Directory layout

```
GRChombo-Axion-SR/
├── env/lawrencium.sh          # module loads + env vars
├── chombo-config/
│   └── Make.defs.local        # Chombo build config (symlinked into Chombo/lib/mk/)
├── Examples/
│   └── AxionSuperradiance/    # our physics code
└── Source/                    # upstream GRChombo source (don't modify)
```

## Dependencies (already built — don't need to redo)

- **Chombo**: `/global/scratch/projects/pc_heptheory/clwelch/software/Chombo/`
  - Compiled with `make lib -j 8` from `Chombo/lib/`
  - Config symlinked from `chombo-config/Make.defs.local`
- **GRChombo fork**: this repo
  - `origin` = clwelch03/GRChombo-Axion-SR (push your work here)
  - `upstream` = GRTLCollaboration/GRChombo (pull GRChombo updates from here)

## Building an example

```bash
source env/lawrencium.sh
cd Examples/AxionSuperradiance
make all -j 8
```

## Pulling upstream GRChombo updates

```bash
git fetch upstream
git merge upstream/main
```
