#!/usr/bin/env python
"""Plot the volume-weighted L2 norm of the Hamiltonian (and momentum) constraint
vs. simulation time, across a set of GRChombo plot files.

This is the quantitative "are the constraints staying controlled?" check for a
run. The cloud is laid on the Kerr background without solving the constraints,
so we expect a nonzero but bounded ||Ham|| that should not grow without limit.

Usage (inside the grviz env):
    grviz/bin/python viz/constraint_norm.py "hdf5/Axionp_*.3d.hdf5"

Only files whose coarse-step index is a multiple of `--stride` (default 10) are
used, so leftover smoke-test frames are skipped.
"""
import argparse
import glob
import os
import re

import numpy as np
import yt

yt.set_log_level(50)


def l2_norm(ds, field):
    """Volume-weighted RMS of a field over the (AMR) domain."""
    ad = ds.all_data()
    vals = ad[("chombo", field)].to_ndarray()
    vol = ad[("index", "cell_volume")].to_ndarray()
    return float(np.sqrt(np.sum(vals**2 * vol) / np.sum(vol)))


def step_index(path):
    m = re.search(r"_(\d+)\.3d\.hdf5$", path)
    return int(m.group(1)) if m else -1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pattern", help="glob for plot files, e.g. 'hdf5/Axionp_*.3d.hdf5'")
    ap.add_argument("--stride", type=int, default=10,
                    help="only use files whose step index %% stride == 0 (default 10)")
    ap.add_argument("--out", default="plots/constraint_norm.png")
    args = ap.parse_args()

    files = sorted(glob.glob(args.pattern), key=step_index)
    files = [f for f in files if step_index(f) % args.stride == 0]
    if not files:
        raise SystemExit(f"no files matched {args.pattern!r}")

    times, ham, mom = [], [], []
    for f in files:
        ds = yt.load(f)
        t = float(ds.current_time)
        times.append(t)
        ham.append(l2_norm(ds, "Ham"))
        mom.append(l2_norm(ds, "Mom"))
        print(f"t={t:8.3f}   ||Ham||={ham[-1]:.4e}   ||Mom||={mom[-1]:.4e}")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axL = plt.subplots(figsize=(7, 4.5))
    axL.semilogy(times, ham, "o-", label="||Ham||")
    axL.semilogy(times, mom, "s--", label="||Mom||")
    axL.set_xlabel("time  (M)")
    axL.set_ylabel("volume-weighted L2 norm")
    axL.set_title("Constraint violation vs. time")
    axL.grid(True, which="both", alpha=0.3)
    axL.legend()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    fig.tight_layout()
    fig.savefig(args.out, dpi=120)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
