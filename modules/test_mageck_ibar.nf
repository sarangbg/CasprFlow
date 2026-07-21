
process test_mageck_ibar {

    input:
    path experiment_design
    val fdr_threshold
    val root_dir
    path count_file

    output:
    path("outputs_$count_file.simpleName/*")

    script:
    def src_dir = root_dir + '/src'
    def script_path = root_dir + '/src/test_mageck_ibar.py'
    """
    mkdir intermediate
    mkdir outputs
    python ${script_path} ${experiment_design} ${fdr_threshold} ${count_file}
    mv outputs outputs_${count_file.simpleName}
    """
}