
process quality_control {

    input:
    path(fastq_file)
    val threads

    output:
    tuple path('*.html'), path('*.zip')

    script:
    def fastq_name = fastq_file.name
    """
    if [[ "$fastq_name" != "NO_FILE" ]]; then
        fastqc -t ${threads} ${fastq_file}
    else
        touch dummy.html
        touch dummy.zip
    fi
    """
}