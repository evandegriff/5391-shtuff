#!/usr/bin/env python3
"""
Simple script for looping through 'calc_ae.py' to create pkls for a range of 
station values.
Output folder will have start, stop, and step values in folder name.
"""

# only need to import one thing!
import os

# still need to set ae_calc.py to debug if you want any printed statements
debug = True

# define the start, astop, and step integers to loop through
start = 12
stop = 361
step = 36

# separate script runs for debug and full versions
if debug:
    # loop through from start to stop ints, by step, and run calc_ae.py
    for rate in range(start, stop, step):
        # use os. system to run the string below in the command line
        os.system(f'python calc_ae.py mag_files_debug/ ae_pkls_debug_{start}_{stop}_{step}/ -r {rate}' )
else:
    # loop through from start to stop ints, by step, and run calc_ae.py
    for rate in range(start, stop, step):
        # use os. system to run the string below in the command line
        os.system(f'python calc_ae.py mag_files/ ae_pkls_{start}_{stop}_{step}/ -r {rate}')