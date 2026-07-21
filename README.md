# CasprFlow

**CasprFlow** is a pipeline for end-to-end analysis of pooled CRISPR screens.

It is built on top of [CASPR](https://doi.org/10.1093/bioinformatics/btz811) with several key improvements:
1. **Nextflow implementation:** Provides built-in parallelism, portability, and reproducibility.
2. **UMI-based analysis:** Supports both sgRNA and pgRNA screens with unique molecular identifiers (UMIs).
3. **Comprehensive benchmarking:** Includes full benchmarking of the UMI mode. 

**Tutorial**

1. It currently runs using Singularity/Apptainer. Start exploring [here](run.sh).

2. For the first two examples, the data is same as described in the original [CASPR repository](https://github.com/judithbergada/CASPR), included [here](testdata) as well. Run the pipeleine, check if the outputs match [this](outputs).

3. For the third example with UMIs, the data was obtained from [Schmierer et al](https://link.springer.com/article/10.15252/msb.20177834) and subsampled using [this](dev/subsample_fastq_umi.py) script.

    a) This subsampled data can be downloaded from here: zenodo link to be added soon.

    b) Place the data in [this folder](testdata/sgrna_umi) and run the pipeline.

    c) The results will contain two folders corresponding to the TCA and LDA mode. Using these two as inputs to [this script](dev/compare_replicate_performance.py), compare the TCA vs LDA results. The script will generate a plot like [this](outputs/sgrna_lda/screen_comparison.png). As reported by Schmierer et al, the performance in LDA mode is better than that of TCA mode.

4. For the fourth example with UMIs, the data was obtained from [Zhu et al](https://link.springer.com/article/10.1186/s13059-019-1628-0) for the TcdB toxicity screening at MOI of 0.3.

    a) Download the data using SRA tools with these IDs: SRR7975589, SRR7975590, SRR7975591 and SRR7975592

    b) Place the forward fastq files in [this folder](testdata/sgrna_ura) and run the pipeline.

    c) The results will contain two folders corresponding to the TCA and URA mode. Using these two as inputs to [this script](dev/compare_replicate_performance.py), compare the TCA vs URA results. The script will generate a plot like [this](outputs/sgrna_lda/screen_comparison.png). As reported by Schmierer et al, the performance in LDA mode is better than that of TCA mode.

Read more in our upcoming manuscript!

---

Copyright © 2026 [Sarang Bhutada](https://www.linkedin.com/in/sarang-bhutada/).