# CasprFlow

**CasprFlow** is a pipeline for end-to-end analysis of pooled CRISPR screens.

It is built on top of [CASPR](https://doi.org/10.1093/bioinformatics/btz811) with several key improvements:
1. **Nextflow implementation:** Provides built-in parallelism, portability, and reproducibility.
2. **UMI-based analysis:** Supports both sgRNA and pgRNA screens with unique molecular identifiers (UMIs).
3. **Comprehensive benchmarking:** Includes full benchmarking of the UMI mode. 

It currently runs using Singularity/Apptainer. Start exploring [here](run.sh).

---

Copyright © 2026 [Sarang Bhutada](https://www.linkedin.com/in/sarang-bhutada/).