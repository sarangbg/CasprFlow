
process test {

    input:
    path experiment_design
    val fdr_threshold
    val rra_controls
    val root_dir
    path count_file

    output:
    path("outputs_$count_file.simpleName/*")

    script:
    def src_dir = root_dir + '/bin'
    """
    mkdir intermediate
    mkdir outputs
    test.sh ${experiment_design} ${fdr_threshold} . ${src_dir} ${rra_controls} ${count_file}
    mv outputs outputs_${count_file.simpleName}
    """
}