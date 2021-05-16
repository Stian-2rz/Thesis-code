#!usr/bin/env/python3
# AUTHOR: STIAN TORSET
# INSTITUTION: UNIVERSITY OF BERGEN
# DATE: 12/01/2021
# PURPOSE: ITERATE OVER PF NTU'S AND GIVE RELEVANT SPECIES AS A TABLE


import os
import argparse
import pandas as pd
import openpyxl
from alive_progress import alive_bar
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='PF directory with all pF files')
parser.add_argument('-o', help='output excel sheet with intreseting taxa')
parser.add_argument('-c','--ntu-cuttof', help='Ntu cuttof, default is 0.01')
args = parser.parse_args()


final_df = pd.DataFrame(columns=['Sample', 'Taxa', 'relabs'])
for file_name in os.listdir(args.input):
    if 'NTUabundance' in file_name and 'svg' not in file_name and 'unass' not in file_name:
        print('Extracting form file', file_name)
        temp_df = pd.DataFrame(columns=['Sample', 'Taxa', 'relabs'])
        sample = ' '.join(map(str, file_name.split(sep='.')[0:2]))
        file_path = args.input + '/' + file_name
        with open(file_path) as NTU_file:
            df = pd.read_csv(NTU_file, delimiter=',', names=['Taxa', 'NTUs']).astype(float, errors='ignore')
            total_ntu = df['NTUs'].sum()
            df['relabs'] = df.NTUs.div(total_ntu)
            new_df = df.loc[(df['relabs'] > .01), ['Taxa', 'relabs']]
            new_df['Sample'] = sample
            temp_df = temp_df.append(new_df)
        final_df = final_df.append(temp_df)


# final_df.drop_duplicates(subset='Taxa', inplace=True)
print(final_df)
final_df.to_excel('interesting_taxa_all.xlsx', engine='openpyxl')
