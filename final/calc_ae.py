#!/usr/bin/env python3
"""
Code to calculate AL, AU, AE, and AO index proxy from SWMF magnetometer output.
Requires input folder and output folder as args.
Can specify latitude range to use for calculations.
Produces pickled dictionary containing epochs and calculated auroral indices.

example:
    python calc_ae.py mag_files_debug/ temp_output/ -u 60 -l 80 -r 180

The above example reads mag files from 'mag_files_debug/', calculates auroral 
indices using 180 magnetometers from 60 degrees to 80 degrees latitude, and 
dumps the resulting pickle into 'temp_output/'
"""

# handle args first, import argparse
from argparse import ArgumentParser

# create parser object, set docstring as help
parser = ArgumentParser(description=__doc__)

# add all arguments, descriptions and defaults.
# magdir () is a required arg
parser.add_argument('magdir', help='File directory where mag files are.',
                    type=str)
# outdir is where the resulting pkls will be saved
parser.add_argument('outdir', help='Directory name for output pkls.'+
                    'Does not need to already exist', type=str)
# u is the upper latitude limit for the AE calculation
parser.add_argument('-u', '--u', help='Value of upper latitude limit. '+
                    'Defaults to 70 degrees.', type=int, default=70)
# l is the lower latitude limit for the AE calculation
parser.add_argument('-l', '--l', help='Value of lower latitude limit. '+
                    'Defaults to 65 degrees.', type=int, default=65)
# r is the resample rate - how many magnetometers to use for AE calculation
parser.add_argument('-r', '--r', help='Number of mags used at each latitude.'+
                    'Defaults to 360 (all).', type=int, default=360)


# collect args together
args = parser.parse_args()

# now start the rest of the file
# import necessary packages
import spacepy.pybats.bats as pbs # allows us to open the magnetometer files
import numpy as np # to get min/max of arrays
import os # to create output folders
from glob import glob # to assemble mag files
from pickle import load, dump # to store calculated AE
from scipy.signal import resample #to specify how many mags to use


# set a boolean to limit/add functionality during debugging/testing
# makes it easier to make small changes without re-running entire fileset
debug = False

# name variables from the arguments
output_folder = args.outdir
upper_lat = args.u
lower_lat = args.l
resample_rate = args.r

# if in debugging mode, print latitude limits
if debug: print(upper_lat, lower_lat)

# check if desired output folder exists, if not, create it
if not os.path.exists(output_folder): os.makedirs(output_folder)

# use glob to collect all magnetometer files, sort by filename
mag_files = sorted(glob(f'./{args.magdir}/mag*.out'))

# looping through thousands of files takes a loooooong time
# for the debug case, specify small subset of magnetometer files to use
if debug: mag_files = [f'./{args.magdir}/mag_grid_e20170906-180250.out',
                       f'./{args.magdir}/mag_grid_e20170907-210350.out',
                       f'./{args.magdir}/mag_grid_e20170908-170530.out']

# create dict with empty arrays for calculated values and time
ae_dict = {'epochs':[], 
           'al': [], 
           'au': [], 
           'ae': [], 
           'ao': []}

# loop through all mag files and calculate AL, AU, AE, and AO
for mag_file in mag_files:
    # use spacepy to open mag file
    mag = pbs.MagGridFile(mag_file)
    # get file time from attributes
    epoch =  mag.attrs['time']
    # more debugging print statements
    if debug: 
        print(epoch)
        print(mag['Lat'][0], mag['Lat'][-1])
    # get dBn array for selected latitudes only
    dBn = mag['dBn'][:,lower_lat:upper_lat+1]
    # resample data to specific number of magnetometers
    dBn = resample(dBn, resample_rate)
    total_mags = resample_rate*(upper_lat - lower_lat+1)
    if debug:
        print(f'resample rate = {resample_rate}')
        print(f'total mags = {total_mags}')
    # more debugging print statements
    if debug: print(np.shape(dBn))
    # set AL to be min of resampled array
    # np.amin flattens a 2-D array to take the min
    al = np.amin(dBn)
    # set AU to max of resampled array
    # np.amax flattens a 2-D array to take the max
    au = np.amax(dBn)
    # calculate ae as the difference between AU and AL
    ae = au - al
    # (AU+AL)/2 defines the AO index
    ao = (au + al)/2
    # more debugging print statements
    if debug:
        print(f'epoch = {epoch}')
        print(f'al = {al}')
        print(f'au = {au}')
        print(f'ae = {ae}')
        print(f'ao = {ao}')
    # add all calculated values to respective arrays in ea_dict
    ae_dict['epochs'].append(epoch)
    ae_dict['al'].append(al)
    ae_dict['au'].append(au)
    ae_dict['ae'].append(ae)
    ae_dict['ao'].append(ao)

# more debugging print statements
if debug: print(ae_dict)

# save ae_dict to pkl, different filenames/locations for debug version
if debug:
    # use resample rate in filename to distinguish it from others
    with open(f'./{output_folder}/ae_dict{total_mags:04}_debug.pkl', 'wb') as f: dump(ae_dict, f)
else:
    with open(f'./{output_folder}/ae_dict{total_mags:04}.pkl', 'wb') as f: dump(ae_dict, f)
