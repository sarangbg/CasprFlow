# CasprFlow

**CasprFlow** is a pipeline for end-to-end analysis of pooled CRISPR screens.

It is build on top of [CASPR](https://doi.org/10.1093/bioinformatics/btz811) with further improvements:
1. Nextflow implementation provides built-in parallelism, portability and reproducibility.
2. UMI based analysis for both sgRNA and pgRNA screens.
3. Comprehensive benchamrking of the UMI mode. 

It currently runs using singularty/apptainer. Start exploring [here](run.sh).

Copyright © 2026 [Sarang Bhutada](https://www.linkedin.com/in/sarang-bhutada/).