#!/usr/bin/env python3

import os
import sys

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt

import helper_functions

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REN_ET_AL_TABLE_S1 = os.path.join(REPO_DIR, 'testdata', 'pegrna', 'ren_library.xlsx')

# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main(mageck_result_file):
    RESULTS_BASE_DIR = os.path.dirname(mageck_result_file)
    print(mageck_result_file)
    print(REN_ET_AL_TABLE_S1)

    renDf = pd.read_excel(REN_ET_AL_TABLE_S1, sheet_name=2, skiprows=0, header=1)
    renDf['common_id'] = renDf['id'].apply(lambda x : '_'.join(x.split('_')[1:]))

    casprflowDf = pd.read_csv(mageck_result_file, sep='\t')
    casprflowDf['common_id'] = casprflowDf['id'].apply(lambda x : '_'.join(x.split('_')[2:]))

    plotDf = pd.merge(renDf[['common_id', 'neg|lfc', 'neg|rank']], casprflowDf[['common_id', 'neg|lfc', 'neg|rank']], on='common_id')

    helper_functions.sns_set_my_style('whitegrid')
    fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(170*helper_functions.mm, 80*helper_functions.mm))

    helper_functions.plot_correlation(plotDf["neg|lfc_x"], plotDf["neg|lfc_y"], ax=axs[0], title="LFC correlation", xlabel='LFC from Ren et al.', ylabel='LFC using CasprFlow')
    helper_functions.plot_correlation(plotDf["neg|rank_x"], plotDf["neg|rank_y"], ax=axs[1], title="Rank correlation", xlabel='Rank from Ren et al.', ylabel='Rank using CasprFlow')
    figPath = os.path.join(RESULTS_BASE_DIR, 'ren_correlation.png')
    plt.savefig(figPath)
    print(figPath)

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except Exception as err:
        print('Provide the correct mageck result file!')
        print(err)