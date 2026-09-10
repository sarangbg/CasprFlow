#!/usr/bin/env python3

import os
import sys

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt

import helper_functions

# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main(mageck_result_file, caspr_result_file):
    RESULTS_BASE_DIR = os.path.dirname(mageck_result_file)
    print(mageck_result_file)
    print(caspr_result_file)

    casprDf = pd.read_csv(caspr_result_file, sep='\t')

    casprflowDf = pd.read_csv(mageck_result_file, sep='\t')

    plotDf = pd.merge(casprDf[['id', 'neg|lfc', 'neg|rank']], casprflowDf[['id', 'neg|lfc', 'neg|rank']], on='id')

    helper_functions.sns_set_my_style('whitegrid')
    fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(170*helper_functions.mm, 80*helper_functions.mm))

    helper_functions.plot_correlation(plotDf["neg|lfc_x"], plotDf["neg|lfc_y"], ax=axs[0], title="LFC correlation", xlabel='LFC using CASPR', ylabel='LFC using CasprFlow')
    helper_functions.plot_correlation(plotDf["neg|rank_x"], plotDf["neg|rank_y"], ax=axs[1], title="Rank correlation", xlabel='Rank using CASPR', ylabel='Rank using CasprFlow')
    figPath = os.path.join(RESULTS_BASE_DIR, 'caspr_correlation.png')
    plt.savefig(figPath)
    print(figPath)

# the first file is expected to be the mageck result from your local run of CasprFLow
# the second file should be the mageck result from the respective outputs folder in this repo 
# eg python dev/compare_sgrna_correlation.py results_sgrna/outputs_table/results_MAGeCK_3.gene_summary.txt outputs/sgrna/outputs_table/results_MAGeCK_3.gene_summary.txt
if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2])
    except Exception as err:
        print('Provide the correct mageck result file!')
        print(err)