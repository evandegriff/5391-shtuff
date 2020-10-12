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
import matplotlib.pyplot as plt
import os


outputPath = './plots'
if not os.path.exists(outputPath):
    os.makedirs(outputPath)



dstTime, dstData = rdst.kyoto_ascii_parser('Dst_July2000.dat')
imfData = sp.read_imf('imf_jul2000.dat')
imfTime = imfData['time']
startTime = datetime.datetime(2000, 7, 15, 6)
endTime = datetime.datetime(2000, 7, 16)

for each in imfData.keys():
    if each != 'time':
        fig = plt.figure(figsize=(15,5))
        ax1 = plt.subplot(111)
        
        color = 'tab:red'
        ax1.set_ylabel(each, color=color)
        ax1.plot(imfTime, imfData[each], label=f'{each}', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        
        color = 'tab:blue'
        ax2.set_ylabel('DST', color=color)  # we already handled the x-label with ax1
        ax2.plot(dstTime, dstData, label='DST Index', color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        fig.autofmt_xdate()
        ax1.set_xlim([startTime, endTime])
        plt.legend()
        ax1.set_title(f'DST and {each} plotted over July 15th, 2000 storm')
        outFileName = outputPath + f'/{each}_and_DST.png'
        plt.savefig(outFileName)
        plt.close()




