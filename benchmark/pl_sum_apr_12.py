#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
" @author: Ziqing Guo
" @date: 2023-10-12
" @description: This script generates synthetic convergence data for QUBO optimization
"""
import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter

def roys_fontset(plt):
    print('load Roys fontest')
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    
    # Check if 'Arial' is available, otherwise use a different font
    if 'Arial' not in [f.name for f in font_manager.fontManager.ttflist]:
        plt.rcParams['font.sans-serif'] = "DejaVu Sans"  # Use 'DejaVu Sans' as an alternative
        plt.rcParams['font.family'] = "sans-serif"
    else:
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.rcParams['font.family'] = "sans-serif"
    
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    tick_major = 6
    tick_minor = 4
    plt.rcParams["xtick.major.size"] = tick_major
    plt.rcParams["xtick.minor.size"] = tick_minor
    plt.rcParams["ytick.major.size"] = tick_major
    plt.rcParams["ytick.minor.size"] = tick_minor

    font_small = 12
    font_medium = 13
    font_large = 14
    plt.rc('font', size=font_small)          # controls default text sizes
    plt.rc('axes', titlesize=font_medium)    # fontsize of the axes title
    plt.rc('axes', labelsize=font_medium)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=font_small)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=font_small)    # fontsize of the tick labels
    plt.rc('legend', fontsize=font_small)    # legend fontsize
    plt.rc('figure', titlesize=font_large)   # fontsize of the figure title

if __name__ == "__main__":
    roys_fontset(plt)

    # Read back and plot
    with h5py.File('cd_apr_12.h5', 'r') as h5f:
        it = h5f['iter'][:]
        qe1 = h5f['new'][:]
        qe2 = h5f['qaoa'][:]
        err1 = h5f['f1'][:]
        err2 = h5f['f2'][:]

    # Create the main convergence plot with error bars
    fig, ax = plt.subplots(figsize=(5.5, 7))
    ax.errorbar(it, qe1, yerr=err1, label='Ours', 
                marker='o', linestyle='-', linewidth=2, markersize=8, capsize=4)
    ax.errorbar(it, qe2, yerr=err2, label='QAOA', 
                marker='s', linestyle='-', linewidth=2, markersize=8, capsize=4)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Global Energy")
    ax.legend(loc='upper right')

    # Inset heatmap
    heat_data = np.vstack([qe1, qe2])
    inset_ax = fig.add_axes([0.55, 0.55, 0.35, 0.25])
    im = inset_ax.imshow(heat_data, extent=[it[0], it[-1], 0, 2], 
                        aspect='auto', cmap='viridis', origin='lower')
    inset_ax.set_yticks([0.5, 1.5])
    inset_ax.set_yticklabels(['DEAL', 'QAOA'])
    inset_ax.set_xlabel("Iteration", fontsize=8)
    inset_ax.tick_params(axis='both', labelsize=8)
    cbar = plt.colorbar(im, ax=inset_ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=8)

    plt.tight_layout()
    plt.savefig('converge.pdf', format='pdf')
    plt.show()
