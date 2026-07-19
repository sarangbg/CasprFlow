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

# DATA_DIR="$SCRIPT_DIR/testdata/sgrna"

# cmd="nextflow run . -profile singularity -o results_sgrna \
#     --samplesheet $DATA_DIR/samplesheet.csv \
#     --experiment_design $DATA_DIR/expdesign.txt --library $DATA_DIR/library.txt --rra_controls $DATA_DIR/controlfile.txt"

# echo "$cmd"

# $cmd

######################
## example 2: pgrna ##
######################

# DATA_DIR="$SCRIPT_DIR/testdata/pgrna"

# cmd="nextflow run . -profile singularity -o results_pgrna --library_mode pgrna --bases_aligned 30 \
#     --samplesheet $DATA_DIR/samplesheet.csv \
#     --experiment_design $DATA_DIR/expdesign.txt --library $DATA_DIR/library.txt --rra_controls $DATA_DIR/controlfile.txt"

# echo "$cmd"

# $cmd

##########################
## example 3: sgrna umi ##
##########################

DATA_DIR="$SCRIPT_DIR/testdata/sgrna_umi"

cmd="nextflow run . -profile singularity --analysis_mode lda --umi_regex '' -o results_sgrna_lda \
    --samplesheet $DATA_DIR/samplesheet.csv \
    --bamsheet $DATA_DIR/ntu_bamsheet.csv \
    --experiment_design $DATA_DIR/experiment_design.txt --library $DATA_DIR/library.txt"

echo "$cmd"

$cmd