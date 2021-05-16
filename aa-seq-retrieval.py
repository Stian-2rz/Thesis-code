import os
import argparse
import pandas as pd
import openpyxl

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='input text file of gene calls from anvio summarize')
args = parser.parse_args()

gene_calls = pd.read_csv(args.input, delimiter='\t')
filename = os.path.basename(os.path.normpath(args.input))[:-15]
for i, row in gene_calls.iterrows():
    print('>' + filename + '_' + str(row['gene_callers_id']))
    print(row['aa_sequence'])