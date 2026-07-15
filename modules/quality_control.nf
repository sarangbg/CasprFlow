
process quality_control {

    input:
    val fastq_forward
    val fastq_reverse
    val threads

    output:
    path "qc"

    script:
    def f = fastq_forward.split(',').join(' ')
    def r = fastq_reverse.split(',').join(' ')
    """
    mkdir qc
    fastqc -t ${threads} -o ./qc ${f}
    if [[ ${fastq_reverse} != "" ]]; then
        fastqc -t ${threads} -o ./qc ${r}
    fi
    """
}