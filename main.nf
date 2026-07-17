#!/usr/bin/env nextflow

include { check } from './modules/check.nf'
include { create_genome } from './modules/create_genome.nf'
include { quality_control as qc_f } from './modules/quality_control.nf'
include { quality_control as qc_r } from './modules/quality_control.nf'
include { trim } from './modules/trim.nf'
include { align } from './modules/align.nf'
include { test } from './modules/test.nf'
include { extract_umi } from './modules/extract_umi.nf'

/*
 * Pipeline parameters
 */
params {
    samplesheet: Path
    experiment_design: Path
    library: Path
    library_mode: String = 'sgrna'
    analysis_mode: String = 'tca'
    umi_regex: String = 'TGGA(......)AACT'
    orientation: Integer = 53
    adapter_f: String = 'ACCG'
    adapter_r: String = 'AAAC'
    mismatches: Integer = 0
    bases_aligned: Integer = 20
    fdr_threshold: Float = 0.1
    rra_controls: String = '""'
    threads: Integer = 5
    info_alignment: String = '0'
}

workflow {

    main:

    // create channel for inputs from the samplesheet CSV file
    // todo: can we merge the samplesheet and experiment_design file and just take one file as input
    fastq_forward_ch = channel
        .fromPath(params.samplesheet, checkIfExists: true)
        .splitCsv(header: true)
        .map { row -> file(row.fastq_1, checkIfExists: true)}
        .view()

    fastq_reverse_ch = channel
        .fromPath(params.samplesheet, checkIfExists: true)
        .splitCsv(header: true)
        .map { row -> row.fastq_2?.trim() ? file(row.fastq_2, checkIfExists: true) : file("$projectDir/assets/NO_FILE")}
        .view()

    // step 0: check if the inputs are correct
    // check(params.fastq_forward, params.fastq_reverse, params.experiment_design, params.library, params.orientation, params.adapter_f, params.adapter_r, params.mismatches, params.bases_aligned, params.fdr_threshold, params.rra_controls,
    // params.threads, workflow.launchDir)

    // step 1: quality control of input fastq files using fasqc
    qc_f(fastq_forward_ch, params.threads)
    fastq_forward_html_ch = qc_f.out.map {fastqc_html, fastqc_zip -> fastqc_html}
    
    if (params.library_mode=='sgrna'){
        qc_output_ch = qc_f.out
    } else{
        qc_r(fastq_reverse_ch, params.threads)
        qc_output_ch = qc_f.out.mix(qc_r.out)
    }
    
    // step 2: adapter trimming
    trim(fastq_forward_ch, fastq_reverse_ch, fastq_forward_html_ch, params.library, params.orientation, params.adapter_f, params.adapter_r, params.threads, workflow.launchDir)

    // step 3: create STAR genome from the library file
    create_genome(params.library, params.threads, workflow.launchDir, params.library_mode)

    // step 4: map the guide reads to the library and count
    // the genome is loaded in the ram only once when aligning on all the samples in the same process, so not passing the channel directly
    align(fastq_reverse_ch.first(), params.library, params.mismatches, params.bases_aligned, params.threads, workflow.launchDir, params.info_alignment, create_genome.out, trim.out.collect())

    // step 5: statistical testing to identify hits
    test(params.experiment_design, params.fdr_threshold, params.rra_controls, workflow.launchDir, align.out.count_file)

    publish:
    qc = qc_output_ch
    trim = trim.out
    count_file = align.out.count_file
    test_outputs = test.out
}

output {
    qc {
        path 'qc'
    }
    trim {
        path '.'
    }
    count_file {
        path '.'
        mode 'copy'
    }
    test_outputs {
        path '.'
        mode 'copy'
    }
}
