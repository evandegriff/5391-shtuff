#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code to parse ASCII files with DST index data from Kyoto World Data Center, 
display statistics for hourly- and daily-averaged DST values, 
and make a simple timeseries plot of DST for the data in the given file.

"""
# import all needed packages.
# re is to find the integers in the file using regular expressions
# pandas is to create a range of datetimes
import numpy as np
import datetime as dt
import re
import pandas as pd
import matplotlib.pyplot as plt

# defining a function that can read the file, in case we need to do it later
def kyoto_ascii_parser(infile, timescale='hourly', debug=False):
    '''
    Function to parse ASCII file with DST index data from Kyoto World Data 
    Center
    If the timescale is set to hourly, this function returns an array with 
    a datetime for every hour, and an array with DST index value for every hour.
    
    If the timescale is set to daily, this function returns an array with a 
    datetime for every day, and an array with DST index value for every day.

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
        If the timescale is set to daily, this function returns an array with a 
    datetime for every day, and an array with DST index value for every day.

    '''
    if timescale not in ['hourly', 'daily']:
        raise(ValueError('Timescale must be daily or hourly. Default is hourly.'))
    # open the file
    f = open(infile, 'r')
    # get an array of all the lines
    lines = f.readlines()
    # close the file, we already have the lines from it
    f.close()
    # create empty lists to put data in, depending on whether hourly or daily
    if timescale == 'daily':
        dateTimes = []
        dstDaily = []
    if timescale == 'hourly':
        dateTimesHourly = []
        dstHourly = []
    # loop through array of lines to parse each one
    for line in lines:
        # construct the date using the specified file format info given
        # first two numbers of the year and the last two are scattered around
        #  month and day are similarly...dispersed
        # final product is a string, e.g. '20000701'
        timeStr = line[14:16] + line[3:7] + line[8:10]
        # use datetime to convert string into usable datetime format
        date = dt.datetime.strptime(timeStr, '%Y%m%d')
        # use regex to extract all integers in the current line, make a list
        # taking negative sign into account
        # note that the first few integers are NOT data and will be removed
        allInts = [int(d) for d in re.findall(r'-?\d+', line)]
        if timescale == 'daily':
            # for the daily timescale, we only need the single datetime
            # add it into the pre-made daily array
            dateTimes.append(date)
            # daily average is the very last integer in each row of the file
            dailyDst = allInts[-1]
            # for daily, we have only one DST value to append to daily DST array
            dstDaily.append(dailyDst)
        if timescale == 'hourly':
            # for the hourly timescale, we  need to create a datetime for each
            # hour of the day, and we can easily do this with pandas
            # .to_pydatetime() at the end of the line converts the list of times
            # back into datetimes rather than the pandas format
            times = pd.date_range(date, periods=24, freq='1H').to_pydatetime()
            # add the list of times into our existing DST array,
            # extend list rather than append so the final array is 1-D
            dateTimesHourly.extend(times)
            # get list of hourly dst values
            # entries 0-3 are part of the date or file format, so we exclude
            # last entry is the daily average DST, so also excluded
            hourlyDst = allInts[4:-1]
            # again, extending, not appending
            dstHourly.extend(hourlyDst)

    # printing out the data can be useful when debugging, but not otherwise
    if debug:
        print(dateTimes)
        print(dateTimesHourly)
        print(dstDaily)
        print(dstHourly)

    # return either hourly datetime and dst arrays, or daily
    if timescale == 'hourly':
        return dateTimesHourly, dstHourly
    if timescale == 'daily':
        return dateTimes, dstDaily



# time to use my new function! let's start with getting the hourly data
dateTimesHourly, dstHourly = kyoto_ascii_parser('Dst_July2000.dat')

# print some stats of the data to screen
print(f'The min of the hourly-averaged DST index is: {np.min(dstHourly)}')
print(f'The max of the hourly-averaged DST index is: {np.max(dstHourly)}')
print(f'The mean of the hourly-averaged DST index is: {np.mean(dstHourly):.1f}')
print(f'The median of the hourly-averaged DST index is: {np.median(dstHourly)}')
print(f'The standard deviation of the hourly-averaged DST index is: {np.std(dstHourly):.1f}')


# repeat for the daily-averaged data
dateTimes, dstDaily = kyoto_ascii_parser('Dst_July2000.dat', timescale='daily')

print(f'The min of the daily-averaged DST index is: {np.min(dstDaily)}')
print(f'The max of the daily-averaged DST index is: {np.max(dstDaily)}')
print(f'The mean of the daily-averaged DST index is: {np.mean(dstDaily):.1f}')
print(f'The median of the daily-averaged DST index is: {np.median(dstDaily)}')
print(f'The standard deviation of the daily-averaged DST index is: {np.std(dstDaily):.1f}')



# lets use our timeseries to plot
# create a figure
plt.figure(figsize=(11,5))
# specify axes
ax = plt.subplot(111)
# plot daily DST data
ax.plot(dateTimes, dstDaily, label='Daily-averaged')
# plot hourly DST data on the same axes
ax.plot(dateTimesHourly, dstHourly, label='Hourly-averaged')
# give plot a title
ax.set_title('Dst_July2000.dat')
# set the label for the y-axis (with units)
ax.set_ylabel('DST Index Value (nT)')
# start and end plot on first and last data points
ax.set_xlim(dateTimesHourly[0], dateTimesHourly[-1])
# add plot legend
plt.legend()
# voila
plt.show()



# TO PRINT OUT THE DAILY AND HOURLY DATETIME ARRAYS, UNCOMMENT THE FOLLOWING LINES
#print(dateTimesHourly)
#print(dateTimes)
