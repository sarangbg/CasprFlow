#!/bin/bash

################################################
## make sure that nextflow 26.04 is installed ##
## uncomment the relevent examples below      ##
################################################

# module load nextflow/26.04

# SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR="$PWD"

# paths are symlinked in a typical HPC setup
SCRIPT_DIR=$(realpath "$SCRIPT_DIR")

######################
## example 1: sgrna ##
######################

DATA_DIR="$SCRIPT_DIR/testdata/sgrna"
#-dump-hashes
# -resume
cmd="nextflow run . -ansi-log true -profile singularity -o results_sgrna \
    --samplesheet $DATA_DIR/samplesheet.csv \
    --experiment_design $DATA_DIR/expdesign.txt --library $DATA_DIR/library.txt --rra_controls $DATA_DIR/controlfile.txt"

echo "$cmd"

# $cmd > run2.log 2>&1
$cmd

######################
## example 2: pgrna ##
######################

# DATA_DIR="$SCRIPT_DIR/testdata/pgrna"

# cmd="nextflow run . -profile singularity -o results_pgrna --library_mode pgrna --bases_aligned 30 \
#     --samplesheet $DATA_DIR/samplesheet.csv \
#     --experiment_design $DATA_DIR/expdesign.txt --library $DATA_DIR/library.txt --rra_controls $DATA_DIR/controlfile.txt"

# echo "$cmd"

# $cmd

######################################
## example 3: sgrna umi in lda mode ##
######################################

# DATA_DIR="$SCRIPT_DIR/testdata/sgrna_umi"

# cmd="nextflow run . -profile singularity --analysis_mode lda --umi_regex '' -o results_sgrna_lda \
#     --samplesheet $DATA_DIR/samplesheet.csv \
#     --experiment_design $DATA_DIR/experiment_design.txt --library $DATA_DIR/library.txt"

# echo "$cmd"

# $cmd

######################################
## example 4: sgrna umi in ura mode ##
######################################

# DATA_DIR="$SCRIPT_DIR/testdata/sgrna_ura"

# cmd="nextflow run . -profile singularity --analysis_mode ura --umi_regex 'TGGA(......)AACA' -o results_sgrna_ura \
#     --adapter_f 'ACCG...GTTT' --samplesheet $DATA_DIR/samplesheet_moi_03.csv \
#     --experiment_design $DATA_DIR/experiment_design_moi_03.txt \
#     --library $DATA_DIR/library.tsv --umi_library $DATA_DIR/library_ibar.tsv"

# echo "$cmd"

# $cmd

######################################
## example 5: pegrna in tca mode ##
######################################

# DATA_DIR="$SCRIPT_DIR/testdata/pegrna"

# cmd="nextflow run . -ansi-log false --threads 8 -profile singularity --analysis_mode tca --library_mode pegrna -o results_pegrna \
#     --adapter_f 'CCTTGTTT...GTTTAGAG' --adapter_r 'GTGTTAGG...GCACCGAC' --samplesheet $DATA_DIR/samplesheet.csv \
#     --experiment_design $DATA_DIR/expdesign.txt --library $DATA_DIR/ren_library_casprflow.tsv \
#     --rra_controls $DATA_DIR/ren_library_neutral_controls.tsv"

# echo "$cmd"

# $cmd