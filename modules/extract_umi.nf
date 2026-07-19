
process extract_umi {

    input:
    path fastq_forward
    val umi_regex
    val threads
    val root_dir

    output:
    path("umi/*.gz")

    script:
    def script_path = root_dir + '/src/extract_umi.py'
    def fastq_forward_name = fastq_forward.simpleName
    """
    mkdir umi
    python ${script_path} ${fastq_forward} ${umi_regex}
    bgzip -@ ${threads} umi/${fastq_forward_name}*
    """
}