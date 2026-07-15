
process trim {

    input:
    val fastq_forward
    val fastq_reverse
    val library
    val orientation
    val adapter_f
    val adapter_r
    val threads
    val root_dir
    val qc_dir

    output:
    path "intermediate"

    script:
    def f = '"' + fastq_forward.split(',').join(' ') + '"'
    def r = '"' + fastq_reverse.split(',').join(' ') + '"'
    def script_path = root_dir + '/src/trimming_reads.sh'
    """
    mkdir intermediate
    ${script_path} ${f} ${r} ${library} ${orientation} ${adapter_f} ${adapter_r} . ${threads} ${qc_dir}
    """
}