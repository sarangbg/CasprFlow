#!/usr/bin/env nextflow

include { check } from './modules/check.nf'
include { create_genome } from './modules/create_genome.nf'
include { quality_control as qc_f } from './modules/quality_control.nf'
include { quality_control as qc_r } from './modules/quality_control.nf'
include { trim } from './modules/trim.nf'
include { align } from './modules/align.nf'
include { test as test_tca } from './modules/test.nf'
include { test as test_lda } from './modules/test.nf'
include { test_mageck_ibar } from './modules/test_mageck_ibar.nf'
include { extract_umi } from './modules/extract_umi.nf'
include { count_umi } from './modules/count_umi.nf'
include { combine_counts } from './modules/combine_counts.nf'

/*
 * Pipeline parameters
 */
params {
    samplesheet: Path
    experiment_design: Path
    bamsheet: String = ''
    countfile: String = ''
    countfilelda: String = ''
    countfileura: String = ''
    library: Path
    umi_library: String = ''
    library_mode: String = 'sgrna'
    analysis_mode: String = 'tca'
    // 'TGGA(......)AACT'
    umi_regex: String = 'X'
    orientation: Integer = 53
    adapter_f: String = 'ACCG'
    adapter_r: String = 'AAAC'
    mismatches: Integer = 0
    bases_aligned: Integer = 20
    fdr_threshold: Float = 0.25
    rra_controls: String = '""'
    threads: Integer = 5
    info_alignment: String = '0'
}

workflow {

    main:

    // create channel for inputs from the samplesheet CSV file
    // TODO: can we merge the samplesheet and experiment_design file and just take one file as input
    // TODO: use the names provided in the samplesheet 
    fastq_forward_ch = channel
        .fromPath(params.samplesheet, checkIfExists: true)
        .splitCsv(header: true)
        .map { row -> file(row.fastq_1, checkIfExists: true)}

    fastq_reverse_ch = channel
        .fromPath(params.samplesheet, checkIfExists: true)
        .splitCsv(header: true)
        .map { row -> row.fastq_2?.trim() ? file(row.fastq_2, checkIfExists: true) : file("$projectDir/assets/NO_FILE")}

    // create empty channels which will be populated depending on the input parameters
    qc_output_ch = channel.empty()
    trimmed_fastq_ch = channel.empty()
    count_file_lda = channel.empty()
    count_file_ura = channel.empty()
    test_outputs_umi = channel.empty()

    if (params.bamsheet==''){
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

        // optional step 2.0: only for UMI analysis
        if (params.analysis_mode!='tca'){
            println "${params.analysis_mode}"
            extract_umi(fastq_forward_ch, fastq_reverse_ch, params.umi_regex, params.threads, workflow.launchDir)
            fastq_forward_ch = extract_umi.out.fastq_forward_umi
            fastq_reverse_ch = extract_umi.out.fastq_reverse_umi
        }
        
        // step 2: adapter trimming
        trim(fastq_forward_ch, fastq_reverse_ch, fastq_forward_html_ch, params.library, params.orientation, params.adapter_f, params.adapter_r, params.threads, workflow.launchDir)
        trimmed_fastq_ch = trim.out

        // step 3: create STAR genome from the library file
        create_genome(params.library, params.threads, workflow.launchDir, params.library_mode)

        // step 4: map the guide reads to the library and count
        // the genome is loaded in the ram only once when aligning on all the samples in the same process, so not passing the channel directly
        align(fastq_reverse_ch.first(), params.library, params.mismatches, params.bases_aligned, params.threads, workflow.launchDir, params.info_alignment, create_genome.out, trimmed_fastq_ch.collect())
        bam_files_ch = align.out.bam_files_ch.flatten().view()
    } else{
        bam_files_ch = channel
            .fromPath(params.bamsheet, checkIfExists: true)
            .splitCsv(header: true)
            .map { row -> file(row.bam, checkIfExists: true)}
            .view()
    }

    // step 5: count the abundannce of guide rnas from the bam files
    if (params.countfile==''){
        if (params.analysis_mode=='tca'){
            count_file = align.out.count_file
        } else{
            count_umi(bam_files_ch, workflow.launchDir)
            umi_library_file = params.umi_library=='' ? file("$projectDir/assets/NO_FILE") : file(params.umi_library, checkIfExists: true)
            combine_counts(count_umi.out.collect(), params.library, umi_library_file, workflow.launchDir)
            count_file_ura = combine_counts.out.ura_counts
            count_file = combine_counts.out.tca_counts
            count_file_lda = combine_counts.out.lda_counts
        }
    } else{
        count_file = file(params.countfile, checkIfExists: true)
        count_file_ura = file(params.countfileura, checkIfExists: true)
        count_file_lda = file(params.countfilelda, checkIfExists: true)
    }
    
    // step 6: statistical testing to identify hits
    test_tca(params.experiment_design, params.fdr_threshold, params.rra_controls, workflow.launchDir, count_file)
    if (params.analysis_mode=='lda'){
        test_lda(params.experiment_design, params.fdr_threshold, params.rra_controls, workflow.launchDir, count_file_lda)
        test_outputs_umi = test_lda.out
    } else if (params.analysis_mode=='ura'){
        test_mageck_ibar(params.experiment_design, params.fdr_threshold, workflow.launchDir, count_file_ura)
        test_outputs_umi = test_mageck_ibar.out
    }

    publish:
    qc = qc_output_ch
    umi = fastq_forward_ch
    trim = trimmed_fastq_ch
    count_file = count_file
    count_file_lda = count_file_lda
    count_file_ura = count_file_ura
    test_outputs = test_tca.out
    test_outputs_umi = test_outputs_umi
}

output {
    qc {
        path 'qc'
    }
    umi {
        path '.'
    }
    trim {
        path '.'
    }
    count_file {
        path '.'
        mode 'copy'
    }
    count_file_lda {
        path '.'
        mode 'copy'
    }
    count_file_ura {
        path '.'
        mode 'copy'
    }
    test_outputs {
        path '.'
        mode 'copy'
    }
    test_outputs_umi {
        path '.'
        mode 'copy'
    }
}
