
process align {

    input:
    val fastq_reverse
    val library
    val mismatches
    val bases_aligned
    val threads
    val root_dir
    val info_alignment
    val genome_dir
    val trim_dir

    output:
    path "alignment", emit: alignment_dir
    path "table.counts.txt", emit: count_file

    script:
    // def f = '"' + fastq_forward.split(',').join(' ') + '"'
    def r = '"' + fastq_reverse.split(',').join(' ') + '"'
    def script_path = root_dir + '/src/alignment_counts.sh'
    // TODO run alignment info script
    """
    mkdir alignment
    mkdir alignment/intermediate
    ${script_path} ${mismatches} ${bases_aligned} ${threads} alignment ${r} ${library}  ${info_alignment} ${genome_dir} ${trim_dir}
    """
}