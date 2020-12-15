#!/usr/bin/env python3
"""
Simple script for 
"""

import os

debug = True

start = 10
stop = 361
step = 36

if debug:
    for rate in range(start, stop, step): 
        os.system(f'python calc_ae.py mag_files_debug/ ae_pkls_debug_{start}_{stop}_{step}/ -r {rate}' )
else:
    for rate in range(start, stop, step): 
        os.system(f'python calc_ae.py mag_files/ ae_pkls_{start}_{stop}_{step}/ -r {rate}')