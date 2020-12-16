#!/usr/bin/env python3
"""
Functions to plot AE data
plot_all_ae:
    Produces single plot with AE plotted over time, one curve for each file in 
    the chosen folder.
plot_each_ae:
    Produces successive plots of AE over time, adding one curve at a time from 
    specified folder. Used to make animated GIF.
plot_ae_rmse:
    Produces single plot of rmse as a function of number of magnetometers used 
    to calculate AE. AE calculated using 360 mags is used as the 'actual' 
    value, and all other AE calculations are compared to this one.
"""

# start with our imports
from pickle import load # to load pkls with AE data
import matplotlib.pyplot as plt # to do our plotting
import os # to check if output folder exists and make it if not
import numpy as np # many calculation, yes
from glob import glob # collecting the files we need into a list

# set input and output directories here
# chose not to use argparse this time since there are individual functions
input_dir = 'ae_pkls'
output_dir = './ae_plots'

# check if desired output folder exists, if not, create it
if not os.path.exists(output_dir): os.makedirs(output_dir)

# use glob to collect all magnetometer files, sort by filename
ae_files = sorted(glob(f'./{input_dir}/*.pkl'))


def plot_all_ae(ae_file_list):
    """
    Produces single plot with AE plotted over time, one curve for each file in 
    the chosen folder.

    Parameters
    ----------
    ae_file_list : list
        List of filename strings (including filepath) that will be used to 
        produce the plot.

    Returns
    -------
    None.

    """
    
    # define a new figure
    fig = plt.figure(figsize=(11,5))
    # give figure a title
    fig.suptitle(f'AE Calculated with varying numbers of magnetometers', fontsize=16)
    # define axes
    ax = plt.subplot(111)
    # loop through pkls, get ae data, and plot on same axes
    for ae_file in ae_file_list:
        # get number of stations used in AE calculation from filename
        num_stations = int(ae_file[-7:-4])
        # open pkl
        with open(ae_file, 'rb') as f: ae_pkl = load(f)
        # save datetimes to an array
        dts = np.array(ae_pkl['epochs'])
        # save AE data to an array
        ae = ae_pkl['ae']
        # plot AE over all datetimes
        ax.plot(dts, ae, label=f'{num_stations} mags')
    # after all files are plotted, set y-axis label
    ax.set_ylabel(f'AE (nT)')
    # set x-axis limits (first and last datetime)
    ax.set_xlim(dts[0], dts[-1])
    # show legend in upper left, placement optimized to not obstruct data
    ax.legend(loc="upper left", ncol=5, fontsize='x-small')
    # make plot compact and neat
    plt.tight_layout()
    # save the figure to file
    plt.savefig(f'{output_dir}/all_ae.png')
    # close the figure
    plt.close('all')

# run the above function, using globbed ae files from beginning of script
plot_all_ae(ae_files)



def plot_each_ae(ae_file_list):
    """
    Produces successive plots of AE over time, adding one curve at a time from 
    specified folder. Used to make animated GIF.

    Parameters
    ----------
    ae_file_list : list
        List of filename strings (including filepath) that will be used to 
        produce the plots.

    Returns
    -------
    None.

    """
    # define a new figure
    fig = plt.figure(figsize=(11,5))
    # give figure a title
    fig.suptitle(f'AE Calculated with varying numbers of magnetometers', fontsize=16)
    # define axes
    ax = plt.subplot(111)
    # set global y-label
    ax.set_ylabel(f'AE (nT)')
    # loop through pkls, get ae data, and plot on same axes, saving each time
    for ae_file in ae_file_list:
        # get number of stations used in AE calculation from filename
        num_stations = int(ae_file[-7:-4])
        # open pkl
        with open(ae_file, 'rb') as f: ae_pkl = load(f)
        # save datetimes to an array
        dts = np.array(ae_pkl['epochs'])
        # save AE data to an array
        ae = ae_pkl['ae']
        # plot AE over all datetimes
        ax.plot(dts, ae, label=f'{num_stations} mags')
        # set x-axis limits (first and last datetime)
        ax.set_xlim(dts[0], dts[-1])
        # set y-axis limit to keep each plot consistent
        ax.set_ylim(0, 2250)
        # show legend in upper left, placement optimized to not obstruct data
        ax.legend(loc="upper left", ncol=5, fontsize='x-small')
        # make plot compact and neat
        plt.tight_layout()
        # create folder inside output folder to hold output from this function
        out_dir = f'{output_dir}/individual_plots'
        # check if desired output folder exists, if not, create it
        if not os.path.exists(out_dir): os.makedirs(out_dir)
        # save the figure to file
        plt.savefig(f'{out_dir}/ae_to{num_stations}.png')
    # once ALL plots are made, close figure
    plt.close('all')


# run the above function, using globbed ae files from beginning of script
plot_each_ae(ae_files)



def plot_ae_rmse(ae_file_list):
    """
    Produces single plot of rmse as a function of number of magnetometers used 
    to calculate AE. AE calculated using 360 mags is used as the 'actual' 
    value, and all other AE calculations are compared to this one.
    
    Note: 
        This function compares the last file in ae_file_list to all the 
        others. The assumption is that the last file will always be the AE
        values calculated using 360 magnetometers.

    Parameters
    ----------
    ae_file_list : list
        List of filename strings (including filepath) that will be used to 
        produce the plot.

    Returns
    -------
    None.

    """
    
    # create empty array for rmse values
    rmse_vals = []
    # create empty array for number of mags used in AE calc
    num_mags = []
    # get baseline AE file from end of list
    ae_360_file = ae_file_list[-1]
    # open baseline AE file
    with open(ae_360_file, 'rb') as f: ae_360_pkl = load(f)
    # save baseline dts
    dts = np.array(ae_360_pkl['epochs'])
    # save baseline AE
    ae_360 = ae_360_pkl['ae']
    # loop through remaining AE files and compare with baseline AE values
    for ae_file in ae_file_list[:-1]:
        # get number of stations used in AE calculation from filename
        num_mags_each = int(ae_file[-7:-4])
        # append num of mags to num_mags
        num_mags.append(num_mags_each)
        # open pkl
        with open(ae_file, 'rb') as f: ae_pkl = load(f)
        # save current AE data to an array
        ae_temp = ae_pkl['ae']
        # calculate MSE compared to the baseline AE data
        mean_sq_err = np.square(np.subtract(ae_360, ae_temp)).mean()
        # take the square root to get RMSE
        rmse = np.sqrt(mean_sq_err)
        # append RMSE to list of RMSE vals
        rmse_vals.append(rmse)
    # after collecting all RMSE and number of mags data, we can plot these
    # define a fig
    fig = plt.figure(figsize=(15,7))
    # give figure a title
    fig.suptitle(f'AE RMSE as a function of number of magnetometers', fontsize=16)
    # define axes
    ax = plt.subplot(111)
    # plot RMSE as a function of the number of mags used to calculate AE
    ax.plot(num_mags, rmse_vals)
    # set y-axis label
    ax.set_ylabel('RMSE')
    # sest x-axis label
    ax.set_xlabel('Number of Magnetometers used in AE calculation')
    # set x-axis limits (first and last datetime)
    ax.set_xlim(num_mags[0], num_mags[-1])
    # increase num of x-axis ticks to get better visual of where curve drops
    plt.xticks(np.arange(num_mags[0], num_mags[-1]+1, 10))
    # make plot compact and neat
    plt.tight_layout()
    # save the figure to file
    plt.savefig(f'{output_dir}/rmse_v_num_mags.png')
    # once plot is saved, close figure
    plt.close('all')


# run the above function, using globbed ae files from beginning of script
plot_ae_rmse(ae_files)