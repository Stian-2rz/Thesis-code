#!usr/bin/env/python3
# AUTHOR: STIAN TORSET
# INSTITUTION: UNIVERSITY OF BERGEN
# DATE: 08/03/2021
# PURPOSE: Creates a line plot with BCD scores between geochemical models and pf relabs


import os
import argparse
from subprocess import check_output, run
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import openpyxl
from alive_progress import alive_bar
from time import sleep

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--pfinput', '-p', help='PF excelsheet annotated with metabollic groups. Will use the Rscript'
                                           'get-normalized-df.R to normalize abundances')
group.add_argument('--normalized-abundance', '-n', help='Call this if you allready an abundance table you want to use'
                                                        'Mutually exclusive with --pfinput')
parser.add_argument('-g', '--GWB-dir of abundance', help='output excel sheet with intreseting taxa')
#  parser.add_argument('-c','--ntu-cuttof', help='Ntu cuttof, default is 0.01')
args = parser.parse_args()

print(os.getcwd())

test = True
# gwb_dir = args.g
gwb_dir = '../../Geochemical Moddeling/scriptlab/model_endpoint_results/'
if not test:
    command = 'C:/Program Files/R/R-4.0.2/bin/Rscript'
    rargs = 'fov_n_lok_autotrophs.csv'
    otp = check_output([command, 'get-normalized-df.R', rargs])

norm_df = pd.read_csv("normalized_df_04.csv", index_col="Unnamed: 0")

bcd_df = norm_df.transpose()
bcd_df.drop(bcd_df.index, inplace=True)

lok_list = []
fov_list = []

# sepperating based on sites
for i, cols in bcd_df.iteritems():
    if 'FOV' not in i:
        lok_list.append(i)
    else:
        fov_list.append(i)

bcd_df_lok = bcd_df[lok_list].copy()
bcd_df_fov = bcd_df[fov_list].copy()


fig, axs = plt.subplots(4, 2, figsize=(8.27, 11.69), dpi=300, sharex='all', sharey='all')
x_test = np.linspace(0, 2 * np.pi, 400)
y_test = np.sin(x_test ** 2)
test_dict_for_test_df = {'FOV1': [0.8, 0.1, 0.05, 0.05], 'FOV2': [0.02, 0.2, 0.28, 0.5]}
temp_dict = [0, 20, 50, 100]
test_df = pd.DataFrame(data=test_dict_for_test_df, index=temp_dict)
dfs = []
axs_title = ''
for y_cont, files in enumerate(os.listdir(gwb_dir)):
    # print('I found these two residence times ' + files)
    filepath = gwb_dir + files + '/'
    counter = 0
    x_cont = 0

    if 'long' in files:
        axs_title += 'Slow Flow \n'
    elif 'no' in files:
        axs_title += 'Fast flow \n'

    for i, sites in enumerate(os.listdir(filepath)):
        sitepath = filepath + '/' + sites
        loke = None
        fovne = None

        for s_dir_counter, sulph_cor_dirs in enumerate(os.listdir(sitepath)):
            if 'LOK_' in sites:
                loke = True
                final_df = bcd_df_lok.copy()
                axs_title += 'LOK '
            elif 'FOV_' in sites:
                fovne = True
                final_df = bcd_df_fov.copy()
                axs_title += 'FOV '
            else:
                continue

            if '10' in sulph_cor_dirs:
                axs_title += '10% ASR '
            else:
                axs_title += ' No ASR'

            if 'abs' in os.listdir(sitepath + '/' + sulph_cor_dirs):
                is_data_dir = True
            else:
                is_data_dir = False
            if is_data_dir:
                data_dir = sitepath + '/' + sulph_cor_dirs
                if 'abs' not in os.listdir(data_dir):
                    print('Could not find abs and ener files in ' + data_dir)
                    print('As data dirs could not be found, this directory was skipped')
                    continue
                elif 'abs' in os.listdir(data_dir):
                    for model_types in os.listdir(data_dir):
                        if model_types != 'abs':
                            continue
                        model_path = data_dir + '/' + model_types
                        if 'excel' not in os.listdir(model_path):
                            print('Found no data files in ' + model_path + '. Continuing')
                            continue

                        excel_dir = model_path + '/excel'

                        abs_df = pd.read_csv(excel_dir + '/groups_df.csv')
                        print(excel_dir)
                        final_df['Temp'] = abs_df['Temp']
                        abs_df.set_index(['Temp'], inplace=True)
                        final_df.set_index(['Temp'], inplace=True)
                        final_df.fillna(0, inplace=True)
                        for temp, groups in abs_df.iterrows():
                            if temp == 4.1:
                                print('showtime')
                            theoreticals = {}
                            theoreticals['SHO'] = groups['sulfox']
                            theoreticals['MO'] = groups['methox']
                            theoreticals['AMO'] = groups['anme'] + groups['amo']
                            theoreticals['SRB'] = groups['srb']
                            theoreticals['Methanogenic'] = groups['methanogens']
                            theoreticals['FO'] = groups['feo']
                            theoreticals['AO'] = groups['ao']
                            for site, norm_groups in norm_df.iterrows():
                                if site in final_df.columns:
                                    s_theoretical = groups.sum()
                                    s_actual = norm_groups.sum()
                                    C_samples = 0
                                    for grp, abundance in norm_groups.iteritems():
                                        if abundance != 0 and theoreticals[grp] != 0:
                                            C_samples += min(theoreticals[grp], abundance)
                                    site_bcd = 1 - ((2 * C_samples) / (s_actual + s_theoretical))
                                    final_df.at[temp, site] = site_bcd

            x_supp = s_dir_counter
            if s_dir_counter == 2:
                x_supp -= 1

            final_df.plot(ax=axs[x_cont, y_cont], title=axs_title, legend=False, xlim=(0,120))

            print(axs_title)
            print('Sample\tTemp\tBCDvalue ')
            for i, cols in final_df.iteritems():
                col_lim = cols[cols.index < 120]
                col_min = min(col_lim)
                print(i, '\t', col_lim[col_lim == col_min].index[0], '\t', '%04.3f' % col_min)
            dfs.append(final_df)
            axs_title = ''
            # axs[y_cont, x_cont].set_title(axs_title)
            print(x_cont)
            x_cont += 1
            print(x_cont)

        # test_df.plot(ax=axs[x_cont, y_cont])
        # axs[y_cont, x_cont].set_title(files + sites[0:3])
        print('I found following sample sites: ' + sites)

for ax in axs.flat:
    ax.set(xlabel='Temperature', ylabel='BC Dissimilarity')
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels)

#uber_df = pd.concat(dfs)
#uber_df.to_csv('bcd_ubder_df.csv')
#plt.legend()
plt.tight_layout()
# plt.savefig('bcd_second.svg')
plt.show()

# print(bcd_df)
