#!/usr/bin/env python3
"""
Docstring
"""

# handle args first, import argparse
from argparse import ArgumentParser

# create parser object, set docstring as help
parser = ArgumentParser(description=__doc__)

# add all arguments, descriptions and defaults.
# magdir () is a required arg
parser.add_argument('magdir', help='File directory where mag files are.',
                    type=str)
# 
parser.add_argument('outdir', help='File directory for pkl output files.'+
                    'Defaults to /ae_pkls.', type=str,  default='ae_pkls_debug/')
parser.add_argument('-u', '--u', help='Value of upper latitude limit. '+
                    'Defaults to 70 degrees.', type=int, default=70)
parser.add_argument('-l', '--l', help='Value of lower latitude limit. '+
                    'Defaults to 65 degrees.', type=int, default=65)
parser.add_argument('-r', '--r', help='Value of magnetometer resample rate.'+
                    'Defaults to 360 (no resample).', type=int, default=360)
parser.add_argument('-o', '--o', help='File directory for pkl output files.'+
                    'Defaults to /ae_pkls.', type=str, default='ae_pkls/')

# Get args from caller, collect arguments into a convenient object:
args = parser.parse_args()

import spacepy.pybats.bats as pbs
import spacepy.pybats as pb
import numpy as np
import os
from glob import glob
from pickle import load, dump
from scipy.signal import resample

debug = True

output_folder = args.outdir
upper_lat = args.u
lower_lat = args.l
resample_rate = args.r

if debug: print(upper_lat, lower_lat)

if not os.path.exists(output_folder): os.makedirs(output_folder)

mag_files = sorted(glob(f'./{args.magdir}/mag*.out'))

if debug: mag_files = [f'./{args.magdir}/mag_grid_e20170906-180250.out',
                       f'./{args.magdir}/mag_grid_e20170907-210350.out',
                       f'./{args.magdir}/mag_grid_e20170908-170530.out']

ae_dict = {'epochs':[], 
           'al': [], 
           'au': [], 
           'ae': [], 
           'ao': []}

for mag_file in mag_files:
    epoch = pb.parse_filename_time(mag_file)[2]
    if debug: print(epoch)
    mag = pbs.MagGridFile(mag_file)
    dBn = mag['dBn'][:,lower_lat:upper_lat+1]
    dBn = resample(dBn, resample_rate)
    if debug: print(np.shape(dBn))
    dBn_min = np.amin(dBn)
    dBn_max = np.amax(dBn)
    al = dBn_min
    au = dBn_max
    ae = au - al
    # (AU+AL)/2 defines the AO index
    ao = (au + al)/2
    if debug:
        print(f'epoch = {epoch}')
        print(f'al = {al}')
        print(f'au = {au}')
        print(f'ae = {ae}')
        print(f'ao = {ao}')
    ae_dict['epochs'].append(epoch)
    ae_dict['al'].append(al)
    ae_dict['au'].append(au)
    ae_dict['ae'].append(ae)
    ae_dict['ao'].append(ao)

if debug: print(ae_dict)

if debug:
    with open(f'./{output_folder}/ae_dict{resample_rate:03}_debug.pkl', 'wb') as f: dump(ae_dict, f)
else:
    with open(f'./{output_folder}/ae_dict{resample_rate:03}.pkl', 'wb') as f: dump(ae_dict, f)
