import sys
import os
import pandas as pd
import concurrent.futures
import multiprocessing

TCA_COUNT_FILE = 'tca_counts.tsv'
URA_COUNT_FILE = 'ura_counts.tsv'
URA_RAW_FILE = 'ura_counts_raw.tsv' # ibar counts before clustering
LDA_COUNT_FILE = 'lda_counts.tsv'

# for a UMI-barcode combination to be included, it should have at least these many reads
MIN_READ_COUNT = 2

# maximum number of mismatches allowed to cluster the UMIs
UMI_CLUSTER_THRESHOLD = 2

# Helper function to calculate differences between two strings
def hamming_distance(s1, s2):
    d = sum(c1 != c2 for c1, c2 in zip(s1, s2))
    # print(d)
    return d

def _find_closest_match(target, string_list):

    # print(target, string_list)
    
    # Find the string with the minimum distance to the target
    # closest_string = min(string_list, key=lambda x: hamming_distance(target, x))

    min_score = 6
    closest_string = 'X'
    for g in string_list:
        score = hamming_distance(target, g)
        if score<min_score and score<=UMI_CLUSTER_THRESHOLD:
            # print(score, g)
            min_score = score
            closest_string = g
    
    return closest_string

def find_closest_match(x):

    target = x['guide']
    umi = x['barcode']

    # ibarlist = guideIbarDf[guideIbarDf[0]==target]['iBAR'].values[0]
    # ibarlist = saveDf[saveDf.sgRNA_seq==sgRNA]['iBAR']
    ibarlist = x['umi']

    closest_string = _find_closest_match(umi, ibarlist)

    return closest_string

def process_group(group_df):
    """
    This function runs in an isolated process. 
    Cluster the UMI for a given gene
    """
    group_df['ibar'] = group_df.apply(lambda row: find_closest_match(row), axis=1)
    group_df = group_df[group_df['ibar']!='X']
    gdf = group_df.drop(columns='barcode')
    gdf2 = gdf.groupby(['guide', 'gene', 'ibar']).aggregate('sum').reset_index(drop=False)
    gdf2 = gdf2.rename(columns={'ibar':'barcode'})
    return gdf2

def cluster_umi(ibar_file):
    print(f'Clustering UMIs based on {ibar_file}')
    libDf = pd.read_csv(ibar_file, sep='\t', header=None)
    libDf.columns = ['guide', 'gene', 'sgRNA_seq', 'umi']
    guideIbarDf = libDf.groupby('guide').aggregate({'umi':list}).reset_index(drop=False)

    count_df = pd.read_csv(URA_COUNT_FILE, sep='\t')
    # count_df = count_df.rename(columns={'ID':'guide', 'Gene':'gene'})
    count_df = pd.merge(count_df, guideIbarDf, on='guide')

    groups = [group for _, group in count_df.groupby('gene')]
    # groups = groups[:50]

    results = []

    # num_cores = multiprocessing.cpu_count()
    num_cores = 5
    
    # Spin up the Process Pool
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
        # executor.map automatically handles passing the chunks to the workers
        # and guarantees that the results list is in the same order as the input list.
        results = list(executor.map(process_group, groups))
        
    # Concatenate everything back together
    final_df = pd.concat(results, ignore_index=True)
    os.rename(URA_COUNT_FILE, URA_RAW_FILE)
    final_df.to_csv(URA_COUNT_FILE, index=None,sep='\t')

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
    # lib_df.drop(columns=2,inplace=True)
    lib_df = lib_df[['guide_id', 'gene']].copy()

    # create URA table (like mageck-ibar)
    count_df = lib_df.merge(count_df.reset_index(), on='guide_id')
    count_df.rename(columns={'guide_id':'guide'},inplace=True)
    count_df = count_df.sort_values(by=['gene','guide'])
    count_df.to_csv(URA_COUNT_FILE, index=None, sep='\t')

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
    create_count_table(sys.argv[1], sys.argv[3:])
    ibar_file = sys.argv[2]
    if os.path.basename(ibar_file)!='NO_FILE':
        cluster_umi(ibar_file)