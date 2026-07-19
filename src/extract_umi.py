import os, sys
import re
import pysam

UMI_SEP = '+'

# extract umi from sequence or index and add it to the read id, so that the umi is preserved during the mapping step
def extract_umi_from_fastq(input_fastq_forward, output_fastq_forward, umi_pattern):
    has_regex = False
    if len(umi_regex)>0:
        pattern = re.compile(umi_pattern, re.IGNORECASE)
        has_regex = True
        if pattern.groups != 1:
            raise ValueError("umi_pattern must contain exactly one capture group")

    n_total = n_kept = 0

    # FastxFile reads plain or gzipped FASTQ transparently and splits each
    # record into name / comment / sequence / quality.
    with pysam.FastxFile(input_fastq_forward) as reader, open(output_fastq_forward,'w') as out:
        for rec in reader:
            n_total += 1

            # if regex is not provided then the i7 index is the umi
            if has_regex:
                m = pattern.search(rec.sequence)
                if m is None:
                    n_bad += 1
                    continue

                umi = m.group(1)
            else:
                umi = rec.comment.split(':')[-1].split('+')[0]
            
            umi = umi.upper()
            if 'N' in umi:
                continue

            rec.name = f"{rec.name}{UMI_SEP}{umi}"
            out.write(str(rec) + '\n')            # str(rec) has no trailing newline
            n_kept += 1

    print(f"# total reads : {n_total}")
    print(f"# kept        : {n_kept}")

def get_fasta_output_path(input_fasta):
    base_dir, fasta_name = os.path.split(input_fasta)
    # print(base_dir, fasta_name)
    # out_dir = os.path.join(base_dir, 'umi')
    out_dir = 'umi'
    os.makedirs(out_dir, exist_ok=True)
    fasta_name_split = fasta_name.split('.')
    output_fasta_name = f'{fasta_name_split[0]}.{fasta_name_split[1]}'
    # output_fasta_name = f'{fasta_name_split[0]}_umi.{fasta_name_split[1]}'
    output_fasta = os.path.join(out_dir, output_fasta_name)
    return output_fasta

if __name__ == "__main__":
    # print(sys.argv[1:])
    input_fastq_forward = sys.argv[1]
    umi_regex = sys.argv[2]

    output_fastq_forward = get_fasta_output_path(input_fastq_forward)
    print(f"Extracting UMI from {input_fastq_forward}")
    extract_umi_from_fastq(input_fastq_forward, output_fastq_forward, umi_regex)