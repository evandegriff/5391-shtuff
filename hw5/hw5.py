#!/usr/bin/env python3

'''Script to download 2003 imf data from the Internet'''

import urllib.request
import datetime
import os

# specify where files should be downloaded
download_dir = 'dat_files/'
# create download dir, if it doesn't already exist
if not os.path.exists(download_dir): os.makedirs(download_dir)

# set time range start for files
base = datetime.datetime(2003,1,1)
# create years worth of datetimes
date_list = [base + datetime.timedelta(days=x) for x in range(365)]

# loop through datetimes to get imf file for each one
for each in date_list:
    # string version of datetime in format of imf file
    date = datetime.datetime.strftime(each, '%Y%m%d')
    # webpage to pull data from 
    url = f'http://www-personal.umich.edu/~dwelling/imf_2003/imf{date}.dat'
    # download data, put into local folder
    urllib.request.urlretrieve(url, f'./dat_files/imf{date}.dat')