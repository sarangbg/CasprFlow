
process create_genome {

    input:
    path library
    val threads
    val library_mode

    output:
    path "genome"

    script:
    """
    fake_genome.sh ${library} ${threads} . ${library_mode}
    """
}