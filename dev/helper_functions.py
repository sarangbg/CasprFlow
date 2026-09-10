"""Correlation scatter plot with identity line and correlation annotations."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import matplotlib
import matplotlib.font_manager
import seaborn as sns

mm = 1/25.4

# GRAPHICAL OPTIONS
LEGEND_SIZE = 9 # 8
AXIS_LABEL = 9 # 8
AXIS_TICK = 7
PLOT_TITLE = 12
PLOT_TITLE_SMALL = 10

def sns_set_my_style(s):# white , whitegrid, ticks
    # sns.set_style(s)
    sns.set_theme(style=s, palette='colorblind')
    if 'grid' in s:
        plt.rc('grid', alpha=0.5)
        plt.rc('grid', linestyle='--')
    plt.rc('font', size=AXIS_TICK)
    plt.rc('axes', titlesize=PLOT_TITLE)     # fontsize of the axes title
    plt.rc('axes', labelsize=AXIS_LABEL)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=AXIS_TICK)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=AXIS_TICK)    # fontsize of the tick labels
    plt.rc('legend', fontsize=LEGEND_SIZE)    # legend fontsize
    plt.rc('legend', title_fontsize=LEGEND_SIZE)
    plt.rc('figure', titlesize=PLOT_TITLE)  # fontsize of the figure title
    plt.rc('figure', dpi=300)
    
    plt.rc('savefig', bbox='tight')
    plt.rc('savefig', pad_inches=0)

    tickPadding = -3

    matplotlib.rcParams['xtick.major.pad'] = tickPadding
    matplotlib.rcParams['ytick.major.pad'] = tickPadding
    matplotlib.rcParams['xtick.minor.pad'] = tickPadding
    matplotlib.rcParams['ytick.minor.pad'] = tickPadding
    matplotlib.rcParams['axes.labelpad'] = 0.5

def plot_correlation(x, y, ax=None, xlabel=None, ylabel=None, title=None,
                     log=False, pad=0.05, annot_loc="upper left",
                     scatter_kws=None, figSize = 85):
    """
    Scatter plot of two pandas Series with a y=x reference line, shared
    axis scaling, and Pearson/Spearman correlations annotated.

    Parameters
    ----------
    x, y : pd.Series (or array-like)
        Paired data. If both are Series they are aligned on their index;
        pairs where either value is NaN/inf are dropped.
    ax : matplotlib Axes, optional
        Axes to draw on. A new figure is created if None.
    xlabel, ylabel : str, optional
        Axis labels. Default to the Series names.
    title : str, optional
    log : bool
        Use log10 scale on both axes (non-positive values are dropped).
    pad : float
        Fractional padding added around the shared data range.
    annot_loc : {"upper left", "lower right"}
        Corner for the statistics box.
    scatter_kws : dict, optional
        Extra keyword arguments passed to ax.scatter.

    Returns
    -------
    ax : matplotlib Axes
    stats_dict : dict with keys 'n', 'pearson_r', 'pearson_p',
                 'spearman_rho', 'spearman_p'
    """
    sns_set_my_style('white')
    
    x = pd.Series(x)
    y = pd.Series(y)

    name_x = xlabel if xlabel is not None else (x.name or "x")
    name_y = ylabel if ylabel is not None else (y.name or "y")

    # Align on index and drop non-finite pairs
    df = pd.concat([x.rename("x"), y.rename("y")], axis=1, join="inner")
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    if log:
        df = df[(df["x"] > 0) & (df["y"] > 0)]

    n = len(df)
    if n < 2:
        raise ValueError(f"Need at least 2 paired finite values, got {n}.")

    xv = df["x"].to_numpy()
    yv = df["y"].to_numpy()

    r, p_r = stats.pearsonr(xv, yv)
    rho, p_rho = stats.spearmanr(xv, yv)

    if ax is None:
        _, ax = plt.subplots(figsize=(figSize*mm, figSize*mm))

    kws = dict(s=14, alpha=0.6, edgecolor="none", color="#2b6cb0")
    if scatter_kws:
        kws.update(scatter_kws)
    ax.scatter(xv, yv, **kws)

    # Shared limits so both axes are on the same scale
    lo = min(xv.min(), yv.min())
    hi = max(xv.max(), yv.max())
    if log:
        lo_l, hi_l = np.log10(lo), np.log10(hi)
        span = (hi_l - lo_l) or 1.0
        lims = (10 ** (lo_l - pad * span), 10 ** (hi_l + pad * span))
        ax.set_xscale("log")
        ax.set_yscale("log")
    else:
        span = (hi - lo) or 1.0
        lims = (lo - pad * span, hi + pad * span)

    ax.plot(lims, lims, ls="--", lw=1, color="grey", zorder=0, label="y = x")
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_aspect("equal", adjustable="box")  # equal visual scale

    def fmt_p(p):
        return "< 1e-300" if p == 0 else f"= {p:.2g}"

    text = (f"Pearson r = {r:.3f} (p {fmt_p(p_r)})\n"
            f"Spearman \u03c1 = {rho:.3f} (p {fmt_p(p_rho)})\n"
            f"n = {n:,}")
    if annot_loc == "upper left":
        xy, ha, va = (0.03, 0.97), "left", "top"
    else:
        xy, ha, va = (0.97, 0.03), "right", "bottom"
    ax.text(*xy, text, transform=ax.transAxes, ha=ha, va=va,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="0.7", alpha=0.85))

    ax.set_xlabel(name_x)
    ax.set_ylabel(name_y)
    if title:
        ax.set_title(title)
    ax.legend(loc="lower right" if annot_loc == "upper left" else "upper left", frameon=False)

    return ax, {"n": n, "pearson_r": r, "pearson_p": p_r,
                "spearman_rho": rho, "spearman_p": p_rho}