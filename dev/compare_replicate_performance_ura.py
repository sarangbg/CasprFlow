#!/usr/bin/env python3
"""
Compare two MAGeCK screen analyses across three replicate-reproducibility
metrics and draw a bar plot.

Each input folder is expected to contain two replicate files in MAGeCK
gene_summary format:
    results_MAGeCK_1.gene_summary.txt   (replicate 1)
    results_MAGeCK_2.gene_summary.txt   (replicate 2)

For each folder the following metrics are computed *between its two
replicates*:

  1. Top-5% overlap   -> number of genes shared in the top 5% by pos|rank
  2. FDR-hit overlap  -> number of genes shared with pos|fdr < 0.01
  3. LFC correlation  -> Pearson r of neg|lfc across all shared genes

The two folders are then compared side by side (one panel per metric).

Usage:
    python compare_screens.py FOLDER_A FOLDER_B [-o out.png]
                              [--top-frac 0.05] [--fdr 0.01]
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt

REP_FILES = ("results_MAGeCK_1.gene_summary.txt",
             "results_MAGeCK_2.gene_summary.txt")

REQUIRED_COLS = ("id", "pos|rank", "pos|fdr")


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def load_replicate(path):
    """Read one MAGeCK gene_summary file into a tidy DataFrame."""
    if not os.path.isfile(path):
        sys.exit(f"ERROR: file not found: {path}")
    # MAGeCK output is tab-separated; be tolerant of stray whitespace.
    df = pd.read_csv(path, sep="\t")
    df.columns = [c.strip() for c in df.columns]

    if 'neg|lfc' not in df.columns:
        df['pos|rank'] = df.index
        df = df.rename(columns={'group_id':'id', 'FDR':'pos|fdr'})

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        sys.exit(f"ERROR: {path} is missing required column(s): {missing}\n"
                 f"       found columns: {list(df.columns)}")

    df = df[list(REQUIRED_COLS)].copy()
    df["id"] = df["id"].astype(str).str.strip()
    df = df.drop_duplicates(subset="id")
    for col in ("pos|rank", "pos|fdr"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_folder(folder):
    """Load both replicate files from a folder; return (rep1, rep2)."""
    if not os.path.isdir(folder):
        sys.exit(f"ERROR: not a directory: {folder}")
    paths = [os.path.join(folder, f) for f in REP_FILES]
    return load_replicate(paths[0]), load_replicate(paths[1])


# --------------------------------------------------------------------------- #
# Metrics
# --------------------------------------------------------------------------- #
def top_rank_overlap(rep1, rep2, frac):
    """Number of genes shared in the top `frac` fraction by pos|rank."""
    # Use the shared gene universe so the top-N is defined consistently.
    genes = set(rep1["id"]) & set(rep2["id"])
    n_top = max(1, int(round(frac * len(genes))))
    top1 = set(rep1.nsmallest(n_top, "pos|rank")["id"])
    top2 = set(rep2.nsmallest(n_top, "pos|rank")["id"])
    return len(top1 & top2), n_top


def fdr_hit_overlap(rep1, rep2, thr):
    """Number of genes called a hit (pos|fdr < thr) in *both* replicates."""
    hits1 = set(rep1.loc[rep1["pos|fdr"] < thr, "id"])
    hits2 = set(rep2.loc[rep2["pos|fdr"] < thr, "id"])
    return len(hits1 & hits2)


def lfc_correlation(rep1, rep2):
    """Pearson correlation of neg|lfc across shared genes."""
    merged = rep1[["id", "neg|lfc"]].merge(
        rep2[["id", "neg|lfc"]], on="id", suffixes=("_1", "_2")
    ).dropna()
    if len(merged) < 2:
        return np.nan
    return merged["neg|lfc_1"].corr(merged["neg|lfc_2"])


def compute_metrics(folder, frac, fdr):
    rep1, rep2 = load_folder(folder)
    overlap, n_top = top_rank_overlap(rep1, rep2, frac)
    return {
        "top_overlap": overlap,
        "n_top": n_top,
        "fdr_overlap": fdr_hit_overlap(rep1, rep2, fdr)
    }


# --------------------------------------------------------------------------- #
# Plotting
# --------------------------------------------------------------------------- #
def make_plot(labels, results, frac, fdr, out_path):
    """One panel per metric, one bar per input folder."""
    panels = [
        ("top_overlap", f"Top {frac*100:.0f}% rank overlap\n(shared genes)", "count"),
        ("fdr_overlap", f"Hit overlap at FDR < {fdr}\n(shared genes)", "count")
    ]
    colors = ["#4C72B0", "#DD8452"]
    x = np.arange(len(labels))

    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    for ax, (key, title, kind) in zip(axes, panels):
        vals = [results[lab][key] for lab in labels]
        bars = ax.bar(x, vals, color=colors[: len(labels)], width=0.6)
        ax.set_title(title, fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=15, ha="right")
        ax.spines[["top", "right"]].set_visible(False)
        if kind == "corr":
            ax.set_ylim(0, 1.05)
        # value labels on top of each bar
        for bar, v in zip(bars, vals):
            txt = f"{v:.2f}" if kind == "corr" else f"{int(v)}"
            ax.annotate(txt,
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=10)

    fig.suptitle("Replicate reproducibility: comparison between analyses",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"Saved plot -> {out_path}")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folder_a", help="first input folder (two replicate files)")
    p.add_argument("folder_b", help="second input folder (two replicate files)")
    p.add_argument("-o", "--output", default="screen_comparison.png",
                   help="output image path (default: screen_comparison.png)")
    p.add_argument("--top-frac", type=float, default=0.05,
                   help="top fraction by rank to overlap (default: 0.05)")
    p.add_argument("--fdr", type=float, default=0.01,
                   help="FDR threshold for hit calling (default: 0.01)")
    args = p.parse_args()

    folders = [args.folder_a, args.folder_b]
    labels = [os.path.basename(os.path.normpath(f)) or f for f in folders]
    # guard against identical basenames
    if labels[0] == labels[1]:
        labels = folders

    results = {}
    for lab, folder in zip(labels, folders):
        results[lab] = compute_metrics(folder, args.top_frac, args.fdr)

    # console summary
    print("\nMetric summary")
    print("-" * 60)
    for lab in labels:
        r = results[lab]
        print(f"{lab}")
        print(f"    top {args.top_frac*100:.0f}% rank overlap : "
              f"{r['top_overlap']} / {r['n_top']} genes")
        print(f"    hits overlap (FDR<{args.fdr}) : {r['fdr_overlap']} genes")
    print("-" * 60)

    make_plot(labels, results, args.top_frac, args.fdr, args.output)

if __name__ == "__main__":
    main()