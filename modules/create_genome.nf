
process create_genome {

    // container 'ghcr.io/prithvirajgavai16/casprflow:latest'
    // container 'ghcr.io/gold-lab/casprflow:latest'
    // container '/home/people/22211214/scratch/tools/test_caspr_umi_diff/CasprFlow/casprflow.sif'

    input:
    val library
    val threads
    val root_dir

    output:
    path "genome"

    script:
    def script_path = root_dir + '/src/fake_genome.sh'
    """
    ${script_path} ${library} ${threads} .
    """
}