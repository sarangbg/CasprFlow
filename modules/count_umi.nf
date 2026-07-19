
process count_umi {

    input:
    path bam_file
    val root_dir

    output:
    path("*.tsv")

    script:
    def count_file_name = bam_file.simpleName + '_count.tsv'
    def script_path = root_dir + '/src/count_umi.sh'
    """
    ${script_path} ${bam_file} ${count_file_name}
    """ 
}