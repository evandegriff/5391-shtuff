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

ae_files = sorted(glob(f'./{input_dir}/*.pkl'))

def plot_all_ae(ae_file_list):
    fig = plt.figure(figsize=(11,5))
    fig.suptitle(f'AE Calculated with varying numbers of magnetometers', fontsize=16)
    ax = plt.subplot(111)

    for ae_file in ae_files:
        num_stations = int(ae_file[-7:-4])
        print(num_stations)
        with open(ae_file, 'rb') as f: ae_pkl = load(f)
        dts = np.array(ae_pkl['epochs'])
        ae = ae_pkl['ae']
        ax.plot(dts, ae, label=f'{num_stations} mags')
    ax.set_ylabel(f'AE (nT)')
    ax.set_xlim(dts[0], dts[-1])
    ax.legend(loc="upper left", ncol=5, fontsize='x-small')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/all_ae.png')
    plt.close('all')


# plot_all_ae(ae_files)


def plot_ae_rmse(ae_file_list):
    rmse_vals = []
    num_mags = []
    ae_360_file = ae_files[-1]
    with open(ae_360_file, 'rb') as f: ae_360_pkl = load(f)
    dts = np.array(ae_360_pkl['epochs'])
    ae_360 = ae_360_pkl['ae']
    ae_files.pop()
    for ae_file in ae_files:
        num_mags_each = int(ae_file[-7:-4])
        num_mags.append(num_mags_each)
        with open(ae_file, 'rb') as f: ae_pkl = load(f)
        ae_temp = ae_pkl['ae']
        mean_sq_err = np.square(np.subtract(ae_360, ae_temp)).mean() 
        rmse = np.sqrt(mean_sq_err)
        rmse_vals.append(rmse)
    
    fig = plt.figure(figsize=(15,7))
    fig.suptitle(f'AE RMSE as a function of number of magnetometers', fontsize=16)
    ax = plt.subplot(111)
    ax.plot(num_mags, rmse_vals)
    ax.set_ylabel('RMSE')
    ax.set_xlabel('Number of Magnetometers used in AE calculation')
    ax.set_xlim(num_mags[0], num_mags[-1])
    plt.xticks(np.arange(num_mags[0], num_mags[-1]+1, 10))
    plt.tight_layout()
    plt.savefig(f'{output_dir}/rmse_v_num_mags.png')
    plt.close('all')

plot_ae_rmse(ae_files)



def plot_each_ae(ae_file_list):
    fig = plt.figure(figsize=(11,5))
    fig.suptitle(f'AE Calculated with varying numbers of magnetometers', fontsize=16)
    ax = plt.subplot(111)
    ax.set_ylabel(f'AE (nT)')
    for ae_file in ae_files:
        num_stations = int(ae_file[-7:-4])
        print(num_stations)
        with open(ae_file, 'rb') as f: ae_pkl = load(f)
        dts = np.array(ae_pkl['epochs'])
        ae = ae_pkl['ae']
        ax.plot(dts, ae, label=f'{num_stations} mags')
        ax.set_xlim(dts[0], dts[-1])
        ax.legend(loc="upper left", ncol=5, fontsize='x-small')
        plt.tight_layout()
        out_dir = f'{output_dir}/individual_plots'
        if not os.path.exists(out_dir): os.makedirs(out_dir)
        plt.savefig(f'{out_dir}/ae_to{num_stations}.png')
    plt.close('all')


plot_each_ae(ae_files)