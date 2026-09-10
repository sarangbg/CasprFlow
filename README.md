# CasprFlow

**CasprFlow** is a pipeline for end-to-end analysis of pooled CRISPR screens.

It is built on top of [CASPR](https://doi.org/10.1093/bioinformatics/btz811) with several key improvements:
1. **Nextflow implementation:** Provides built-in parallelism, portability, and reproducibility.
2. **UMI-based modes:** Supports both sgRNA and pgRNA screens with unique molecular identifiers (UMIs).
3. **Diverse gRNA architecture:** Supports analysis of prime editing CRISPR screens with pegRNAs.
4. **Comprehensive benchmarking:** Includes full benchmarking of the UMI mode. 

**Tutorial**

1. It currently runs using Singularity/Apptainer. Start exploring [here](run.sh).

2. For the first two examples, the data is same as described in the original [CASPR repository](https://github.com/judithbergada/CASPR), included [here](testdata) as well. Run the pipeline, check if the outputs match [this](outputs).

3. For the third example with UMIs, the data was obtained from [Schmierer et al](https://link.springer.com/article/10.15252/msb.20177834) and subsampled using [this](dev/subsample_fastq_umi.py) script.

    a) This subsampled data can be downloaded from here: zenodo link to be added soon.

    b) Place the data in [this folder](testdata/sgrna_lda) and run the pipeline.

    c) The results will contain two folders corresponding to the TCA and LDA mode. Using these two as inputs to [this script](dev/compare_replicate_performance.py), compare the TCA vs LDA results. The script will generate a plot like [this](outputs/sgrna_lda/screen_comparison.png). As reported by Schmierer et al, the performance in LDA mode is better than that of TCA mode.

4. For the fourth example with UMIs, the data was obtained from [Zhu et al](https://link.springer.com/article/10.1186/s13059-019-1628-0) for the TcdB toxicity screening at MOI of 0.3.

    a) Download the data using SRA tools with these IDs: SRR7975589, SRR7975590, SRR7975591 and SRR7975592

    b) Place the forward fastq files in [this folder](testdata/sgrna_ura) and run the pipeline.

    c) The results will contain two folders corresponding to the TCA and URA mode. Using these two as inputs to [this script](dev/compare_replicate_performance.py), compare the TCA vs URA results. The script will generate a plot like [this](outputs/sgrna_lda/screen_comparison.png). As reported by Schmierer et al, the performance in LDA mode is better than that of TCA mode.

5. For the fifth example with pegRNAs, the data was obtained from [Ren et al](https://www.sciencedirect.com/science/article/pii/S1097276523009668) which tested the effect of single-nucleotide substitutions within an MCF7-specific MYC enhancer.

    a) Download the data using SRA tools with the run IDs from this [table](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP411650&o=acc_s%3Aa), Enh_D2 is the initial time point and Enh_D30 is the final time point (check the 'Sample Name' column).

    b) Place the fastq files in [this folder](testdata/pegrna), rename the samples as per the [samplesheet](testdata/pegrna/samplesheet.csv) and run the pipeline.

    c) Run [this script](dev/compare_ren_correlation.py) to compare the results from CasprFlow with the results from Ren et al (supplimentary table S1). The gene summary file from mageck, which looks like [this](outputs/pgrna/outputs_table/results_MAGeCK_1.gene_summary.txt), should be provided as input to this script. The script will generate a plot like [this](outputs/pegrna/ren_correlation.png). CasprFlow reproduced the results from the original study, as indicated by the high correlation of LFC and rank of the target base substitutions.

Read more in our upcoming manuscript!

---

Copyright © 2026 [Sarang Bhutada](https://www.linkedin.com/in/sarang-bhutada/).