#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 12:56:15 2020

@author: exv3640
"""

import sciprog as sp # import the file-parser from class
import numpy as np #yay numpy
import read_dst as rdst
import datetime
import pandas as pd

imfData = sp.read_imf('imf_jul2000.dat')
dstData = kyoto_ascii_parser('Dst_July2000.dat')
startTime = datetime.datetime()
print(imfData.keys())
