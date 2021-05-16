#!usr/bin/env/python3
# AUTHOR: STIAN TORSET
# INSTITUTION: UNIVERSITY OF BERGEN
# DATE: 08/01/2021
# PURPOSE: CREATE NEW FASTA FILE WITH BIN DESIGNATIONS

import os
import argparse
import pandas as pd
from alive_progress import alive_bar
from time import sleep


# PARSER

parser = argparse.ArgumentParser()
parser.add_argument('--fasta-file', '-f', help='A fasta file resulting from anvi-get-sequences-for-gene calls')
parser.add_argument('--bin-file', '-b', help='File with contigs belonging to bins from abnvi-export-collection')
parser.add_argument('--output', '-o', help='output fasta file with the bin and taxonomy added to the fasta line')
parser.add_argument('--taxonomy-file', '-t', help='file with gtdbtk taxonomy data from anvi-get-taxonomy')
parser.add_argument('--test', action='store_true')

args = parser.parse_args()

fasta = args.fasta_file
bins = args.bin_file
taxa = args.taxonomy_file
test = True
if args.test:
    test = False

if test:
    fasta = '../Loke/seqs_aa_pfam_adh.fa'
    bins = '../Loke/contigs_4_DT.txt'
    taxa = '../Loke/DAS_Tool/DAS_TOOL_taxonomy.txt'
    scores = '../Loke/DAS_Tool/_DASTool_summary.txt'


def make_bar(ffile):
    with open(ffile) as ffile:
        counter = 0
        for lines in ffile:
            if '>' == lines[0]:
                counter += 1
        print('Found ' + str(counter) + ' sequences')
        return counter


def make_fasta_line(fasta_line):
    line_as_list = fasta_line.split(sep='|')[:2]
    caller = line_as_list[0]
    contig = line_as_list[1][7:]
    bin = ''
    "Try-except loops to avoid kicking when key error occurs"
    try:
        contig_split_1 = contig + '_split_00001'
        bin = bins_ser.loc[contig_split_1]
    except KeyError:
        pass
    try:
        contig_split_2 = contig + '_split_00002'
        bin = bins_ser.loc[contig_split_2]
    except KeyError:
        pass
    try:
        contig_split_3 = contig + '_split_00003'
        bin = bins_ser.loc[contig_split_3]
    except KeyError:
        if bin == '':
            bin = 'Not Found'

    binned = True
    found = True
    if 'UNBINNED' in bin:
        line_as_list.extend(['Bin= Unbinned', 'Tax= na'])
        binned = False
    if 'Not Found' in bin:
        contigs_not_found.append(contig)
        include = input("""
                        Whoa there, I couldn't find % in the exported bins file. Its not a disaster, but do you want to include
                        it in the output fasta anyway y | [n]?
                        """)
        if include == 'n':
            found = False
        else:
            line_as_list.extend(['Bin= Not found', 'Tax= na'])

    if binned:
        line_as_list.append(bin)
        taxonomy = taxa_df.loc[taxa_df['bin_name'] == bin]
        line_as_list.extend('Tax= ' + taxonomy['t_order'])
    return line_as_list


if __name__ == '__main__':
    bins_ser = pd.read_csv(bins, delimiter='\t', names=['contig', 'bin'], index_col='contig')['bin']
    taxa_df = pd.read_csv(taxa, delimiter='\t')
    bar_counter = make_bar(fasta)

    with open(fasta) as fasta_file:
        contigs_not_found = []
        aa_seq = ''
        with alive_bar(bar_counter, spinner='fish') as bar:
            for line in fasta_file:
                new_line = ''
                if line[0] == '>':
                    line_as_list = make_fasta_line(line)

                else:
                    aa_seq += line

                if line[0] == '>':
                    # print(len(aa_seq))
                    if len(aa_seq) > 100:
                        line_as_list.append('length=' + str(len(aa_seq)))
                        new_file = open(args.output, 'a+')
                        fa_line = '|'.join(map(str, line_as_list)) + '\n'
                        # print(fa_line)
                        new_file.write(fa_line)
                        new_file.write(aa_seq)
                        aa_seq = ''

                    sleep(0.03)
                    bar()








