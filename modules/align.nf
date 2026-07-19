
process align {

    input:
    path fastq_reverse
    val library
    val mismatches
    val bases_aligned
    val threads
    val root_dir
    val info_alignment
    val genome_dir
    path trimmed_fastq

    output:
    path('alignment/*.bam'), emit: bam_files_ch
    path "table.counts.txt", emit: count_file

    script:
    def script_path = root_dir + '/src/alignment_counts.sh'
    def fastq_reverse_2 = fastq_reverse.name=="NO_FILE" ? "" : "$fastq_reverse"
    // TODO run alignment info script
    """
    mkdir alignment
    mkdir alignment/intermediate
    ${script_path} ${mismatches} ${bases_aligned} ${threads} alignment "${fastq_reverse_2}" ${library}  ${info_alignment} ${genome_dir} "${trimmed_fastq}"
    """
}