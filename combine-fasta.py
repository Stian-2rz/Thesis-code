#!usr/bin/env/python3
# AUTHOR: STIAN TORSET
# INSTITUTION: UNIVERSITY OF BERGEN
# DATE: 01/04/2021
# PURPOSE: Combine two fasta files and delete duplicates




import os
import argparse

# PARSER
parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='comma delim list with fasta sequences: file1,file2')
parser.add_argument('-o', help='output file')
args = parser.parse_args()


def create_prote_object(file):
    """

    :param file: input txt file with fasta sequences from blast
    :return: Nothing, appends to an external list of protein classes
    """
    file_as_list = file.readlines()
    new_prot = False
    new_prot_index = 0
    for i, line in enumerate(file_as_list):
        acc = ''
        ptype = []
        taxa = []
        seq = ''
        if '>' in line:
            for pind, pline in enumerate(file_as_list[i:]):  # protein index and protein line
                line_as_list = pline.split()
                if '>' in pline and (pind + i) != i:  # sets the criteria for new proteins
                    break
                if '>' in pline:
                    in_taxonomy = False
                    for x, entries in enumerate(line_as_list):
                        if '[' in entries:
                            in_taxonomy = True
                        if x == 0:
                            acc += entries[1:]
                        if x != 0 and not in_taxonomy:
                            ptype.append(entries)
                        if in_taxonomy:
                            taxa.append(entries)
                else:
                    seq += pline.strip()
            list_of_proteins.append(Protein(acc, ptype, taxa, seq))


class Protein:
    def __eq__(self, other):
        return self.accession == other.accession and self.sequence

    def __hash__(self):
        return hash(('accession', self.accession, 'sequence', self.sequence))

    def __init__(self, accession, protein_type, organism, sequence):
        self.accession = accession
        self.protein_type = protein_type
        self.organism = organism
        self.sequence = sequence
        self.ordered_line = ''

    def order_line(self):
        new_line = '>' + '_'.join(map(str, self.organism)).strip('[]') + '_' + self.accession
        return new_line


if __name__ == '__main__':
    list_of_proteins = []
    list_o_files = args.input.split(',')
    #print(list_o_files)
    for f, file in enumerate(list_o_files):
        with open(file) as blast_file:
            create_prote_object(blast_file)
    unique = set(list_of_proteins)
    # print(list_of_proteins[0].accession)
    for obi, protes in enumerate(unique):
        print(protes.order_line())
        print(protes.sequence)