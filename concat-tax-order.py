import os
import numpy
import argparse
import pandas as pd
from shutil import copyfile

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--pf-directory', help='Phyloflash superdir')
parser.add_argument('-o', '--output-dir', help='Output directory name')
args = parser.parse_args()
unique = pd.read_excel('unique.xlsx', engine='openpyxl')

bad = [
    'ROV16-R01-I',
    'ROV14-R02',
    'ROV14-R04',
    'ROV14-R05',
    'ROV16-R02-I',
    'ROV16-R02-O'
]
for f, file in enumerate(os.listdir('../PF_superdir_euks_stripped/')):
    if any(file in b for b in bad):
        continue
    if 'abundance' in file:
        path = str('../PF_superdir_euks_stripped/' + '/' + file)
        df = pd.read_csv(path, sep=';|,', header=None, engine='python')
        df_no_class = df.drop(columns=[3])  # [2,3] for phyla level concatenation
        df_no_class.set_index([0, 1, 2], inplace=True) #[0,1] for phyla level concatenation
        df_sum = df_no_class.groupby(df_no_class.index)[4].sum().reset_index()
        df_sum[[0, 1, 2]] = pd.DataFrame(df_sum['index'].tolist(), index=df_sum.index) #[0,1] fplc
        to_desired_df = df_sum[[0, 1, 2, 4]]
        final_df = to_desired_df
        for r, row in to_desired_df.iterrows():
            if 'FOV-ROV16-R01-M.phyloFlash.NTUabundance' in file:
                print('stop')
                if r == 129:
                    print('please stop')
            ser = unique['Taxa']
            phyla = 'Desulfo'
            vals = ser.values
            if any(row[2] in s for s in vals):
                if any(row[1] in s for s in vals):
                    continue
                else:
                    final_df.drop([r], inplace=True)
            else:
                final_df.drop([r], inplace=True)

        final_df.to_csv('../PF_superdir_to_order_filtered/' + file, sep=';', header=False, index=False)
        csv_file = open('../PF_superdir_to_order_filtered/' + file, 'rt')
        lal = csv_file.readlines()
        for l, lines in enumerate(lal):
            lis = list(lines)
            sep_counter = 0
            colon_counter = 0
            for c, chr in enumerate(lines):
                if chr == ';':
                    colon_counter += 1
                if colon_counter == 3:  # 2 for phyla level
                    sep_counter += c
                    break
            lis[sep_counter] = ','
            lal[l] = "".join(lis)
        csv_file.close()
        csv_file = open('../PF_superdir_to_order_filtered/' + file, 'wt')
        csv_file.writelines(l for l in lal)
        csv_file.close()

    else:
        copyfile('../PF_superdir_euks_stripped/' + file,
                 '../PF_superdir_to_order_filtered/' + file)

