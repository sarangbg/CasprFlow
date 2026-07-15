#!/usr/bin/env nextflow

include { check } from './modules/check.nf'
include { create_genome } from './modules/create_genome.nf'
include { quality_control } from './modules/quality_control.nf'
include { trim } from './modules/trim.nf'
include { align } from './modules/align.nf'
include { test } from './modules/test.nf'

/*
 * Pipeline parameters
 */
params {
    fastq_forward: String ='""'
    fastq_reverse: String = '""'
    experiment_design: String = '""'
    library: String = '""'
    library_mode: String = 'sgrna'
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
    // create a channel for inputs from a CSV file
    // greeting_ch = channel.fromPath(params.input)
    //                     .splitCsv()
    //                     .map { line -> line[0] }

    // step 1: check if the inputs are correct
    check(params.fastq_forward, params.fastq_reverse, params.experiment_design, params.library, params.orientation, params.adapter_f, params.adapter_r, params.mismatches, params.bases_aligned, params.fdr_threshold, params.rra_controls,
    params.threads, workflow.launchDir)

    // step 2: create STAR genome from the library file
    create_genome(params.library, params.threads, workflow.launchDir)

    // step 3: quality control of input fastq files
    quality_control(params.fastq_forward, params.fastq_reverse, params.threads)

    // step 4: adapter trimming
    trim(params.fastq_forward, params.fastq_reverse, params.library, params.orientation, params.adapter_f, params.adapter_r, params.threads, workflow.launchDir, quality_control.out)

    // step 5: map the guide reads to the library and count
    align(params.fastq_reverse, params.library, params.mismatches, params.bases_aligned, params.threads, workflow.launchDir, params.info_alignment, create_genome.out, trim.out)

    // step 6: statistical testing to identify hits
    test(params.experiment_design, params.fdr_threshold, params.rra_controls, workflow.launchDir, align.out.count_file)

    publish:
    input_parameters = check.out
    library_genome = create_genome.out
    qc = quality_control.out
    trim = trim.out
    alignment_dir = align.out.alignment_dir
    count_file = align.out.count_file
    test_outputs = test.out
}

output {
    input_parameters {
        path '.'
        mode 'copy'
    }
    library_genome {
        path '.'
    }
    qc {
        path '.'
    }
    trim {
        path '.'
    }
    alignment_dir {
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
