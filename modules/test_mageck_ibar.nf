
process test_mageck_ibar {

    input:
    path experiment_design
    val fdr_threshold
    path count_file

    output:
    path("outputs_$count_file.simpleName/*")

    script:
    """
    mkdir intermediate
    mkdir outputs
    python test_mageck_ibar.py ${experiment_design} ${fdr_threshold} ${count_file}
    mv outputs outputs_${count_file.simpleName}
    """
}