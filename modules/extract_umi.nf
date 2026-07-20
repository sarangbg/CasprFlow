
process extract_umi {

    input:
    path fastq_forward
    path fastq_reverse
    val umi_regex
    val threads
    val root_dir

    output:
    path("umi/$fastq_forward.simpleName*"), emit: fastq_forward_umi
    path("umi/$fastq_reverse.simpleName*"), emit: fastq_reverse_umi

    script:
    def script_path = root_dir + '/src/extract_umi.py'
    def fastq_forward_name = fastq_forward.simpleName
    def fastq_reverse_name = fastq_reverse.simpleName
    def fastq_reverse_2 = fastq_reverse_name=="NO_FILE" ? "X" : "$fastq_reverse"
    """
    mkdir umi
    gzip -tv ${fastq_forward}
    python ${script_path} ${fastq_forward} ${fastq_reverse_2} ${umi_regex}
    bgzip -@ ${threads} umi/${fastq_forward_name}*
    if [[ "$fastq_reverse_name" == "NO_FILE" ]]; then
        cp ${fastq_reverse} umi/
    else
        bgzip -@ ${threads} umi/${fastq_reverse_name}*
    fi
    """
}