
process test {

    input:
    path experiment_design
    val fdr_threshold
    val rra_controls
    val root_dir
    path count_file

    output:
    path "outputs"

    script:
    def src_dir = root_dir + '/src'
    def script_path = root_dir + '/src/test.sh'
    """
    mkdir intermediate
    mkdir outputs
    ${script_path} ${experiment_design} ${fdr_threshold} . ${src_dir} ${rra_controls} ${count_file}
    """
}