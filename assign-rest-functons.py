#!usr/bin/env/python3
# AUTHOR: STIAN TORSET
# INSTITUTION: UNIVERSITY OF BERGEN
# DATE: 30/01/2021
# PURPOSE: TAKE THE ANNOTATED SPECIES FROM GET-RELEVANT-SPECIES.PY AND UPPDATES THE SAME SPECIES ANNOTATION THROUGHOUT

import pandas as pd
import xlrd
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--i', help='Input excel sheet that has some annotations allongside the relabs data')
args = parser.parse_args()


df = pd.read_excel('speed_annotated_all2.xlsx', engine='openpyxl')
#df = df_read[['Sample', 'Taxa', 'relabs', 'Metabollic group', 'Notes', 'Source']].copy()
annotated_taxa = {}
for index, row in df.iterrows():
    annotated = False
    sample = row[0]
    taxa = row[1]
    group = str(row[3])
    notes = str(row[4])
    source = str(row[5])


    if group != 'nan' and notes != 'nan':
        annotated = True
        if taxa not in annotated_taxa.keys():
            annotated_taxa[taxa] = [group, notes, source]

    if taxa in annotated_taxa.keys() and not annotated:
        ant_grp = annotated_taxa[taxa][0]
       #  df.loc[index, 'Metabollic group'] = ant_grp
        df.loc[index, ['Metabollic group','Notes', 'Source']] = annotated_taxa[taxa]

print(df)
df = df.drop_duplicates(subset='Taxa').set_index('Sample')
df.to_excel('unique.xlsx')


