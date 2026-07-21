import sys
import os
import pandas as pd
import subprocess 

def test_mageck_ibar(experiment_design_file, fdr_threshold, count_file):
    exp_design_df = pd.read_csv(experiment_design_file,sep='\t',header=None)
    exp_design_df.columns = ['sample','rep','group']
    exp_design_df['group_index'] = exp_design_df['group'].apply(lambda x:x.replace('control','').replace('treated',''))
    exp_design_df['group_type'] = exp_design_df['group'].apply(lambda x:x[0])
    exp_design_df.sort_values(by=['group_index','group_type'],inplace=True)

    mageck_ibar_cmd = """mageck-ibar -i {count_table} -b --col-gene gene --col-guide guide --col-barcode barcode \
                         -t {treated} -c {control} --gene-test-fdr-threshold {fdr} -o intermediate/{prefix_name}"""

    for i, group_df in exp_design_df.groupby(by='group_index',sort=False):
        c = ' '.join(group_df[group_df['group_type']=='c']['sample'])
        t = ' '.join(group_df[group_df['group_type']=='t']['sample'])
        test_cmd = mageck_ibar_cmd.format(count_table=count_file, treated=t, control=c, fdr=fdr_threshold, prefix_name=f'results_MAGeCK_{i}')
        print(test_cmd)
        subprocess.run(test_cmd, shell=True, executable="/bin/bash")
        mv_cmd = f'mv intermediate/results_MAGeCK_{i}.gene.high.txt outputs/results_MAGeCK_{i}.gene_summary.txt'
        subprocess.run(mv_cmd, shell=True, executable="/bin/bash")

if __name__ == "__main__":    
    test_mageck_ibar(sys.argv[1], sys.argv[2], sys.argv[3])