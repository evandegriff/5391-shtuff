#!/usr/bin/env python3
"""
File docs
"""


from pickle import load, dump
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime as dt
from glob import glob

debug = False

input_dir = 'ae_pkls'
output_dir = './ae_plots'
if not os.path.exists(output_dir): os.makedirs(output_dir)

ae_files = sorted(glob('./ae_pkls/*.pkl'))

def plot_all_ae():
    fig = plt.figure(figsize=(11,5))
    fig.suptitle(f'AE Calculated with varying numbers of stations', fontsize=16)
    ax = plt.subplot(211)

    for ae_file in ae_files:
        num_stations = int(ae_file[-7:-4])
        print(num_stations)
        with open(ae_file, 'rb') as f: ae_pkl = load(f)
        dts = np.array(ae_pkl['epochs'])
        ae = ae_pkl['ae']
        ax.plot(dts, ae, label=f'{num_stations} stations')
    ax.set_ylabel(f'x (Re)')
    ax.set_xlim(dts[0], dts[-1])
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/all_ae.png')
    plt.close('all')


plot_all_ae()