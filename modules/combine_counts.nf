
process combine_counts {

    input:
    path count_files
    path library
    val root_dir

    output:
    path('tca_counts.tsv'), emit: tca_counts
    path('ura_counts.tsv'), emit: ura_counts
    path('lda_counts.tsv'), emit: lda_counts

    script:
    def script_path = root_dir + '/src/create_count_table.py'
    """
    python ${script_path} ${library} ${count_files}
    """
}