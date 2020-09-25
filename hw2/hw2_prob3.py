#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 13:07:11 2020
@author: exv3640

Code to parse ASCII files with DST index data from Kyoto World Data Center, 
display statistics for hourly- and daily-averaged DST values, 
and make a simple timeseries plot of DST for the data in the given file.

"""

import numpy as np
import datetime as dt
import re
import pandas as pd
import matplotlib.pyplot as plt
	
def kyoto_ascii_parser(infile, timescale='hourly', debug=False):
    '''
    Function to parse ASCII file with DST index data from Kyoto World Data Center
    
    If the timescale is set to hourly, this function returns an array with a datetime 
    for every hour, and an array with DST index value for every hour.
    
    If the timescale is set to daily, this function returns an array with a datetime 
    for every day, and an array with DST index value for every day.

    Parameters
    ----------
    infile : string
        filename of the file you wish to parse
    timescale : string, optional
        Allows you to specify whether you want to receive hourly averaged 
        or daily-averaged DST index data. The default is 'hourly'.
    debug : bool, optional
        Just in case things go wrong. The default is False.

    Returns
    -------
    lists
        If timescale is set to hourly, returns an array with a datetime 
    for every hour, and an array with DST index value for every hour.
    lists
        If the timescale is set to daily, this function returns an array with a datetime 
    for every day, and an array with DST index value for every day.

    '''
    if timescale not in ['hourly', 'daily']:
        raise(ValueError('Timescale must be daily or hourly. Default is hourly.'))
    f = open(infile, 'r')
    lines = f.readlines()
    dateTimes = []
    dateTimesHourly = []
    dstDaily = []
    dstHourly = []
    for line in lines:
        timeStr = line[14:16] + line[3:7] + line[8:10]
        date = dt.datetime.strptime(timeStr, '%Y%m%d')
        dateTimes.append(date)
        times = pd.date_range(date, periods=24, freq='1H').to_pydatetime()
        dateTimesHourly.extend(times)
        allInts = [int(d) for d in re.findall(r'-?\d+', line)]
        hourlyDst = allInts[4:-1]
        dstHourly.extend(hourlyDst)
        dailyDst = allInts[-1]
        dstDaily.append(dailyDst)
    f.close()
    if debug:
        print(dateTimes)
        print(dateTimesHourly)
        print(dstDaily)
        print(dstHourly)
    if timescale == 'hourly':
        return dateTimesHourly, dstHourly
    if timescale == 'daily':
        return dateTimes, dstDaily




dateTimesHourly, dstHourly = kyoto_ascii_parser('Dst_July2000.dat')
# data stats
minHourly = np.min(dstHourly)
maxHourly = np.max(dstHourly)
meanHourly = np.mean(dstHourly)
medianHourly = np.median(dstHourly)
stdHourly = np.std(dstHourly)

print(f'The min of the hourly-averaged DST index is: {minHourly}')
print(f'The max of the hourly-averaged DST index is: {maxHourly}')
print(f'The mean of the hourly-averaged DST index is: {meanHourly:.1f}')
print(f'The median of the hourly-averaged DST index is: {medianHourly}')
print(f'The standard deviation of the hourly-averaged DST index is: {stdHourly:.1f}')


# print data stats to screen

dateTimes, dstDaily = kyoto_ascii_parser('Dst_July2000.dat', timescale='daily')
 
minDaily = np.min(dstDaily)
maxDaily = np.max(dstDaily)
meanDaily = np.mean(dstDaily)
medianDaily = np.median(dstDaily)
stdDaily = np.std(dstDaily)

print(f'The min of the daily-averaged DST index is: {minDaily}')
print(f'The max of the daily-averaged DST index is: {maxDaily}')
print(f'The mean of the daily-averaged DST index is: {meanDaily:.1f}')
print(f'The median of the daily-averaged DST index is: {medianDaily}')
print(f'The standard deviation of the daily-averaged DST index is: {stdDaily:.1f}')



plt.figure(figsize=(11,5))
ax = plt.subplot(111)
ax.plot(dateTimes, dstDaily, label='Daily-averaged')
ax.plot(dateTimesHourly, dstHourly, label='Hourly-averaged')
ax.set_title('Dst_July2000.dat')
ax.set_ylabel('DST Index Value')
ax.set_xlim(dateTimesHourly[0], dateTimesHourly[-1])
plt.legend()
plt.show()



# TO PRINT OUT THE DAILY AND HOURLY DATETIME ARRAYS, UNCOMMENT THE FOLLOWING LINES
#print(dateTimesHourly)
#print(dateTimes)