"""
Subsample a fastq file to only keep reads where the UMI starts with the given string
Usage: python subsample_fastq_umi.py /path/tp/fastq umi_start
eg: python subsample_fastq_umi.py ntu_r1_d4.fq.gz ag
this will create a new file named 'ntu_r1_d4_ag.fq.gz'
"""

import os, sys, subprocess
# import dnaio
import pysam

def subsample_fastq_umi(input_fasta, output_fasta, umi_start):
    print(input_fasta, output_fasta, umi_start)
    n_total = n_kept = 0

    # with dnaio.open(input_fasta) as reader, dnaio.open(output_fasta, mode='w') as writer:
    with pysam.FastxFile(input_fasta) as reader, open(output_fasta, 'w') as writer:
        for rec in reader:
            n_total += 1
            # the indices are stored in the format i7+i5 at the end of the read header
            # umi = rec.name.split(':')[-1].split('+')[0]
            umi = rec.comment.split(':')[-1].split('+')[0]
            if umi.startswith(umi_start) and 'N' not in umi:
                # writer.write(rec)
                writer.write(str(rec) + '\n')
                n_kept += 1

    print(f"# total reads : {n_total}")
    print(f"# kept        : {n_kept}")

if __name__ == "__main__":
    input_fasta = sys.argv[1]
    umi_start = sys.argv[2]
    base_dir, fasta_name = os.path.split(input_fasta)
    fasta_name_split = fasta_name.split('.')
    # output_fasta_name = [fasta_name_split[0] + '_' + umi_start]
    # output_fasta_name.extend(fasta_name_split[1:])
    # output_fasta_name = '.'.join(output_fasta_name)
    output_fasta_name = f"{fasta_name_split[0]}_{umi_start}.{fasta_name_split[1]}"
    # print(output_fasta_name)
    output_fasta = os.path.join(base_dir, output_fasta_name)
    subsample_fastq_umi(input_fasta, output_fasta, umi_start.upper())

    runCmd = f"bgzip -@ 10 {output_fasta}"
    subprocess.run(runCmd, shell=True, executable="/bin/bash")