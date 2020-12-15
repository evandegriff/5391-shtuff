#!/usr/bin/env python3
"""
File docs
"""


from pickle import load, dump
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime as dt

debug = False

input_dir = 'ae_pkls'
output_dir = './ae_plots'
if not os.path.exists(output_dir): os.makedirs(output_dir)

with open(f'./{input_dir}/ae_dict180.pkl', 'rb') as f: ae_pkl = load(f)
