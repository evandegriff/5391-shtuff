#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to plot imf variables alongside DST values for a specific time range. 
Uses a dst .dat file and an imf .dat file, creates a directory of plots with
one for each imf variable, plus one plot with DST alone.
"""
import sciprog as sp # import the file-parser from class
import read_dst as rdst # import my kyoto data format file-parser *MAKE SURE read_dst IS IN YOUR PYTHON PATH
import datetime # need to manipulate datetimes
import matplotlib.pyplot as plt # here's our plotting tool!
import os # need to create a folder to put plots in, use os module to do this


# set output path where plots will go
outputPath = './plots'
# check if output path exists
if not os.path.exists(outputPath):
    # make output dir if it doesn't exist
    os.makedirs(outputPath)

# create dict for units of each var
units = {'bx':'nT', 'by':'nT', 'bz':'nT', 'vx':'km/s', 'vy':'km/s', 'vz':'km/s', 'rho':'$n/cm^3$', 'temp':'K'}
# create dict of plot labels for each var (more descriptive than just using the variable name)
titles = {'bx':'$B_{x}$', 'by':'$B_{y}$', 'bz':'$B_{z}$', 'vx':'$V_{x}$', 'vy':'$V_{y}$', 'vz':'$V_{z}$', 
          'rho':'Number Density', 'temp':'Temperature'}

# parse the dst file using my script, get arrays of time and dst
dstTime, dstData = rdst.kyoto_ascii_parser('Dst_July2000.dat')
# parse the imf file using our script from class
imfData = sp.read_imf('imf_jul2000.dat')
# set the imf time array
imfTime = imfData['time']
# set start time for plot
startTime = datetime.datetime(2000, 7, 15, 12)
# set end time for plot
endTime = datetime.datetime(2000, 7, 16)

# loop through each variable in imf file
for each in imfData.keys():
    # exclude time, we don't need to plot that
    if each != 'time':
        # define a figure
        fig = plt.figure(figsize=(15,5))
        # specify axis
        ax1 = plt.subplot(111)
        # set color for this data series
        color = 'tab:red'
        # set the y-axis label and color for first axis
        ax1.set_ylabel(f'{titles[each]} ({units[each]})', color=color)
        # plot whichever imf variable our loop is on
        ax1.plot(imfTime, imfData[each], color=color)
        # set the color of the y-axis ticks
        ax1.tick_params(axis='y', labelcolor=color)        
        # make a second set of axes with same x-axis
        ax2 = ax1.twinx()
        # set a new color for this data series
        color = 'tab:blue'
        # set the y-axis label and color for second axis
        ax2.set_ylabel('$D_{{ST}}$ (nT)', color=color)
        # plot dst data
        ax2.plot(dstTime, dstData, color=color)
        # set the color of the y-axis ticks
        ax2.tick_params(axis='y', labelcolor=color)
        # set the x-axis limits as the start and stop datetimes 
        ax1.set_xlim([startTime, endTime])
        # set the plot title
        # NOTE: double brackets allow you to use LaTeX notation inside fstring notation
        ax1.set_title(f'$D_{{ST}}$ and {titles[each]} for July 15th, 2000 storm')
        # create name of plot to save
        outFileName = outputPath + f'/{each}_and_DST.png'
        # save plot
        plt.savefig(outFileName)
        # close the current figure
        plt.close()


# Make a separate plot with ONLY dst:

# define a figure
fig = plt.figure(figsize=(15,5))
# specify axis
ax = plt.subplot(111)
# set color
color = 'tab:blue'
# set y-axis label and color
ax.set_ylabel('$D_{{ST}}$ (nT)', color=color)
# plot dst
ax.plot(dstTime, dstData, color=color)
# set the color of the y-axis ticks
ax.tick_params(axis='y', labelcolor=color)
# set the x-axis limits as the start and stop datetimes
ax.set_xlim([startTime, endTime])
# set plot title
ax.set_title(f'$D_{{ST}}$ for July 15th, 2000 storm')
# create file output name
outFileName = outputPath + f'/DST.png'
# save the plot
plt.savefig(outFileName)
#close the plot; eh close them all, just to be safe
plt.close('all')

