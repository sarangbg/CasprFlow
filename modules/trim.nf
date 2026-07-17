
process trim {

    input:
    path(fastq_forward)
    path(fastq_reverse)
    path(fastqc_html_file)
    val library
    val orientation
    val adapter_f
    val adapter_r
    val threads
    val root_dir

    output:
    path('intermediate/sgRNA2_sgRNA1_*')

    script:
    def script_path = root_dir + '/src/trimming_reads.sh'
    def fastq_reverse_2 = fastq_reverse.name== "NO_FILE" ? "" : "$fastq_reverse"
    """
    mkdir intermediate
    ${script_path} ${fastq_forward} "${fastq_reverse_2}" ${library} ${orientation} ${adapter_f} ${adapter_r} . ${threads} ${fastqc_html_file}
    """
}