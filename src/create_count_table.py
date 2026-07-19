import sys
import os
import pandas as pd

TCA_COUNT_FILE = 'tca_counts.tsv'
URA_COUNT_FILE = 'ura_counts.tsv'
LDA_COUNT_FILE = 'lda_counts.tsv'

# for a UMI-barcode combination to be included, it should have at least these many reads
MIN_READ_COUNT = 2

def create_count_table(library_file, count_file_list):
    count_df = pd.DataFrame()
    for i, count_file in enumerate(count_file_list):
        # TODO: this should be part of the input, the pattern is {name}_Aligned_count.tsv
        bam_name = '_'.join(os.path.basename(count_file).split('.')[0].split('_')[:-2])
        tmp_df = pd.read_csv(count_file,sep='\t',header=None).rename(columns={0:'guide_id',1:'barcode',2:bam_name}).set_index(['guide_id','barcode'])
        if i==0:
            count_df = tmp_df.copy()
        else:
            count_df = count_df.join(tmp_df,how='outer').fillna(0).astype(int)

    lib_df = pd.read_csv(library_file, sep='\t',header=None).rename(columns={0:'guide_id',1:'gene'})
    lib_df.drop(columns=2,inplace=True)

    # create URA table (like mageck-ibar)
    count_df = lib_df.merge(count_df.reset_index(), on='guide_id')
    count_df.rename(columns={'guide_id':'guide'},inplace=True)
    count_df = count_df.sort_values(by=['gene','guide'])
    count_df.to_csv(URA_COUNT_FILE, index=None,sep='\t')

    # create TCA table
    # as per mageck, 1st column should be sgrna and 2nd column should be gene
    # as per CASPR, the name of the columns should be 'Gene' and 'ID' 
    tca_count_df = count_df.groupby(by=['guide','gene']).aggregate(sum).reset_index().rename(columns={'guide':'ID', 'gene':'Gene'})
    tca_count_df.to_csv(TCA_COUNT_FILE, sep='\t', index=None)

    # create LDA table
    sample_cols = sorted(list(count_df.columns)[3:]) 
    df_list = []
    for col in sample_cols:
        count_df[col] = pd.to_numeric(count_df[col])
        tmp_df = count_df[count_df[col]>=MIN_READ_COUNT].groupby(by=['guide','gene']).size().to_frame().rename(columns={0:col})
        df_list.append(tmp_df)    
    lda_count_df = pd.concat(df_list,axis=1).fillna(0).astype(int).reset_index().rename(columns={'guide':'ID', 'gene':'Gene'})
    lda_count_df.to_csv(LDA_COUNT_FILE, sep='\t', index=None)

if __name__ == "__main__":    
    create_count_table(sys.argv[1], sys.argv[2:])