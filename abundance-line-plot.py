#!usr/bin/env/python3
# AUTHOR: STIAN TORSET
# INSTITUTION: UNIVERSITY OF BERGEN
# DATE: 11/03/2021
# PURPOSE: Creates a line plot with predicted relative abundances between geochemical models and pf relabs

import os
import argparse
from subprocess import check_output, run
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = 'Times New Roman'

gwb_dir = '../../Geochemical Moddeling/scriptlab/model_endpoint_results/'
axs_title = ''

colors = ['#9fc444ff',  # SHO
          '#00be67ff',  # MO
          '#cd9600ff',  # ANME?
          '#ff61ccff', # AMO
          '#00a9ffff', # SRB
          '#f8766dff',  # Methanogen
          '#c77cffff',  # FO
          '#00bfc4ff']  # AO


fig, axs = plt.subplots(4, 2, figsize=(8.27, 11.16), dpi=300, sharex='all', sharey='all')
abs_df = pd.DataFrame()
for y_cont, files in enumerate(os.listdir(gwb_dir)):
    # print('I found these two residence times ' + files)
    filepath = gwb_dir + files + '/'
    counter = 0
    x_cont = 0

    if 'long' in files:
        axs_title += 'Slow Flow\n'
    else:
        axs_title += 'Fast Flow\n'

    for i, sites in enumerate(os.listdir(filepath)):
        sitepath = filepath + '/' + sites
        loke = None
        fovne = None

        for s_dir_counter, sulph_cor_dirs in enumerate(os.listdir(sitepath)):
            if 'LOK_' in sites:
                loke = True
                axs_title += 'LOK_'
            elif 'FOV_' in sites:
                fovne = True
                axs_title += 'FOV_'
            else:
                continue

            if '10' in sulph_cor_dirs:
                axs_title += '0.1-ASR'
            else:
                axs_title += 'NoASR'

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
                        abs_df.set_index(['Temp'], inplace=True)
            x_supp = s_dir_counter
            if s_dir_counter == 2:
                x_supp -= 1

            abs_df.plot(ax=axs[x_cont, y_cont], title=axs_title, legend=False, xlim=(0,120), color=colors)
            axs_title = ''
            # axs[y_cont, x_cont].set_title(axs_title)
            # print(x_cont)
            x_cont += 1
            # print(x_cont)


for ax in axs.flat:
    ax.set(xlabel='Temperature', ylabel='Relative Abundance')
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, ncol=8)
#plt.legend()
plt.tight_layout()
plt.savefig('../../abs_akk.svg')
plt.show()