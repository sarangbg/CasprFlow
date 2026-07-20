import os, sys
import re
import pysam
from itertools import zip_longest
from contextlib import ExitStack

UMI_SEP='+'

def add_umi_to_name(name, umi, sep=UMI_SEP):
    """pysam separates the read ID (name) from the comment, so appending here
    keeps the UMI on the ID token, where it survives alignment."""
    return f"{name}{sep}{umi}"

def _core_id(name):
    """Strip old-style /1 or /2 mate suffixes for the mate-name comparison."""
    return name[:-2] if name.endswith(('/1', '/2')) else name

def extract_umi_from_fastq(input_fastq_forward, output_fastq_forward, umi_regex, input_fastq_reverse=None, output_fastq_reverse=None):
    has_regex = False
    if umi_regex!='X':
        pattern = re.compile(umi_regex, re.IGNORECASE)
        has_regex = True
        if pattern.groups != 1:
            raise ValueError("umi_pattern must contain exactly one capture group")

    paired = input_fastq_reverse is not None

    n_total = n_kept = 0

    with ExitStack() as stack:
        # FastxFile reads plain or gzipped FASTQ transparently and splits each
        # record into name / comment / sequence / quality.
        r1_in = stack.enter_context(pysam.FastxFile(input_fastq_forward))
        o1 = stack.enter_context(open(output_fastq_forward, 'w'))

        if paired:
            r2_in = stack.enter_context(pysam.FastxFile(input_fastq_reverse))
            o2 = stack.enter_context(open(output_fastq_reverse, 'w'))
            read_iter = zip_longest(r1_in, r2_in)      # zip_longest catches desync
        else:
            read_iter = ((rec, None) for rec in r1_in)

        for rec1, rec2 in read_iter:
            # zip_longest yields None once one mate file runs out before the other
            if rec1 is None or (paired and rec2 is None):
                raise ValueError("R1 and R2 have different numbers of reads")
            # if paired and _core_id(rec1.name) != _core_id(rec2.name):
            #     raise ValueError(
            #         f"mate names differ: {rec1.name!r} vs {rec2.name!r}")
            
            n_total += 1

            if has_regex:
                # barcode lives in R1
                m = pattern.search(rec1.sequence)
                if m is None:
                    continue

                umi = m.group(1)
            else:
                # if regex is not provided then the i7 index is the umi
                umi = rec1.comment.split(':')[-1].split('+')[0]
            
            umi = umi.upper()
            if 'N' in umi:
                continue

            rec1.name = add_umi_to_name(rec1.name, umi)
            o1.write(str(rec1) + '\n')                  # str(rec) has no trailing newline
            if paired:
                rec2.name = add_umi_to_name(rec2.name, umi)
                o2.write(str(rec2) + '\n')
            n_kept += 1

    print(f"# total reads : {n_total}")
    print(f"# kept        : {n_kept}")

def get_fasta_output_path(input_fasta):
    base_dir, fasta_name = os.path.split(input_fasta)
    fasta_name_split = fasta_name.split('.')
    output_fasta_name = f'{fasta_name_split[0]}.{fasta_name_split[1]}'
    # print(base_dir, fasta_name)
    # out_dir = os.path.join(base_dir, 'outputs')
    out_dir = 'umi'
    os.makedirs(out_dir, exist_ok=True)
    output_fasta = os.path.join(out_dir, output_fasta_name)
    return output_fasta

if __name__ == "__main__":
    # print(sys.argv[1:])
    input_fastq_forward = sys.argv[1]
    input_fastq_reverse = sys.argv[2]
    umi_regex = sys.argv[3]

    output_fastq_forward = get_fasta_output_path(input_fastq_forward)
    input_fastq_reverse = input_fastq_reverse if len(input_fastq_reverse)>1 else None
    output_fastq_reverse = None if input_fastq_reverse is None else get_fasta_output_path(input_fastq_reverse)
    print(f"Extracting UMI from {input_fastq_forward} {input_fastq_reverse}")
    extract_umi_from_fastq(input_fastq_forward, output_fastq_forward, umi_regex, input_fastq_reverse, output_fastq_reverse)