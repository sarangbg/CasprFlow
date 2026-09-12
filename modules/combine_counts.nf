
process combine_counts {

    input:
    path count_files
    path library
    path umi_library

    output:
    path('tca_counts.tsv'), emit: tca_counts
    path('ura_counts.tsv'), emit: ura_counts
    path('lda_counts.tsv'), emit: lda_counts

    script:
    """
    python create_count_table.py ${library} ${umi_library} ${count_files}
    """
}