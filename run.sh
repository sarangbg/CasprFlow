#!/bin/bash

# module load nextflow/26.04

# SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR="$PWD"

# paths are symlinked in a typical HPC setup
SCRIPT_DIR=$(realpath "$SCRIPT_DIR")
DATA_DIR="$SCRIPT_DIR/testdata/sgrna"

cmd="nextflow run . -profile singularity -resume -o results_sgrna --fastq_forward $DATA_DIR/week0.1.fastq.gz,$DATA_DIR/week0.2.fastq.gz,$DATA_DIR/week4.1.fastq.gz,$DATA_DIR/week4.2.fastq.gz --experiment_design $DATA_DIR/expdesign.txt --library $DATA_DIR/library.txt"

echo "$cmd"

$cmd