
process count_umi {

    input:
    path bam_file

    output:
    path("*.tsv")

    script:
    def count_file_name = bam_file.simpleName + '_count.tsv'
    """
    count_umi.sh ${bam_file} ${count_file_name}
    """ 
}