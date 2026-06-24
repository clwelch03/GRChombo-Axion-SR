#!/usr/bin/env python
"""Render 2D slices of GRChombo (Chombo AMR HDF5) plot files with yt.

Usage:
    python slice.py <plotfile.hdf5> [field1 field2 ...] [--axis z] [--outdir plots]

By default it slices through the grid centre along the z-axis and writes one
PNG per field (defaulting to phi and chi). Run inside the grviz conda env, e.g.:

    CONDA=/global/scratch/projects/pc_heptheory/clwelch/software/envs/grviz
    $CONDA/bin/python slice.py hdf5/Axionp_000000.3d.hdf5
"""
import argparse
import os
import yt

yt.set_log_level(40)  # warnings+ only, keep stdout clean


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("plotfile", help="GRChombo plot file (.3d.hdf5)")
    ap.add_argument("fields", nargs="*", default=["phi", "chi"],
                    help="fields to slice (default: phi chi)")
    ap.add_argument("--axis", default="z", choices=["x", "y", "z"],
                    help="slice-normal axis (default: z)")
    ap.add_argument("--outdir", default="plots", help="output dir for PNGs")
    args = ap.parse_args()

    ds = yt.load(args.plotfile)
    # centre of the domain = where the BH sits (kerr_center defaults to centre)
    center = 0.5 * (ds.domain_left_edge + ds.domain_right_edge)

    os.makedirs(args.outdir, exist_ok=True)
    base = os.path.splitext(os.path.splitext(os.path.basename(args.plotfile))[0])[0]

    for field in args.fields:
        p = yt.SlicePlot(ds, args.axis, ("chombo", field), center=center)
        p.set_cmap(("chombo", field), "viridis")
        p.annotate_grids()           # show the AMR box structure
        p.annotate_title(f"{field}  ({base}, {args.axis}-slice through centre)")
        out = os.path.join(args.outdir, f"{base}_{field}_{args.axis}.png")
        p.save(out)
        print("wrote", out)


if __name__ == "__main__":
    main()
