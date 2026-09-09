
process count_read {
    tag "${sample}:${step}"

    input:
    tuple val(step), path(reads), val(read_path)

    output:
    stdout

    script:
    // sample = reads.simpleName.replaceAll(/_Aligned$/, '').replaceAll(/^sgRNA2_sgRNA1_/, '')
    sample = reads.name.tokenize('.')[0..<2].join('.').replaceAll(/_Aligned$/, '').replaceAll(/^sgRNA2_sgRNA1_/, '')
    if( reads.name.endsWith('.bam') || reads.name.endsWith('.cram') )
        """
        printf '%s\\t%s\\t%s\\t%s\\n' ${sample} ${read_path} ${step} \$(samtools view -c -F 0x900 ${reads})
        """
    else
        """
        printf '%s\\t%s\\t%s\\t%s\\n' ${sample} ${read_path} ${step} \$(( \$(zcat -f ${reads} | wc -l) / 4 ))
        """
}