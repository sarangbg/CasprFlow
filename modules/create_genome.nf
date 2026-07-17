
process create_genome {

    input:
    path library
    val threads
    val root_dir
    val library_mode

    output:
    path "genome"

    script:
    def script_path = root_dir + '/src/fake_genome.sh'
    """
    ${script_path} ${library} ${threads} . ${library_mode}
    """
}