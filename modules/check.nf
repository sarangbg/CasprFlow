
process check {

    input:
    val fastq_forward
    val fastq_reverse
    val experiment_design
    val library
    val orientation
    val adapter_f
    val adapter_r
    val mismatches
    val bases_aligned
    val fdr_threshold
    val rra_controls
    val threads
    val root_dir

    output:
    path "inputs.txt"

    script:
    def f = '"' + fastq_forward.split(',').join(' ') + '"'
    def r = '"' + fastq_reverse.split(',').join(' ') + '"'
    def script_path = root_dir + '/src/basic_errors.sh'
    // TODO run basic_error_test also
    """
    ${script_path} ${f} ${r} ${library} ${experiment_design} ${orientation} ${adapter_f} ${adapter_r} ${mismatches} ${bases_aligned} ${fdr_threshold} ${threads} . ${rra_controls}
    """
}