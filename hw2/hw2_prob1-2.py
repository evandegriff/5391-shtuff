#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File designed to calculate total B and V at each timestep for a given data file, save B and V data to files and print the mean values of B and V to screen.
"""


import sciprog as sp # import the file-parser from class
import numpy as np #yay numpy

# read in the data
allData = sp.read_imf('imf_aug2005.dat')

# take the square root of the squares to determine total absolute value of B
absB = np.sqrt(allData['bx']**2 + allData['by']**2 + allData['bz']**2)

# zip together values of Bx, By, Bz, and B for each timestep
allB = np.array(list(zip(allData['bx'], allData['by'], allData['bz'], absB)))

# take the square root of the squares to determine total absolute value of V
absV = np.sqrt(allData['vx']**2 + allData['vy']**2 + allData['vz']**2)

# zip together values of Vx, Vy, Vz, and V for each timestep
allV = np.array(list(zip(allData['vx'], allData['vy'], allData['vz'], absV)))

# open a new file to save th B values
f = open('b_out.txt', 'w')
# write the header line
f.write(f'{"Bx":<10} {"By":<10} {"Bz":<10} |B|\n')
# loop through each list in the array of B values
for each in allB:
    # write to file
    f.write(f'{each[0]:<+10} {each[1]:<+10} {each[2]:<+10} {each[3]:<+10.2f}\n')
# close the file!
f.close()

# open a new file to save th B values
f2 = open('v_out.txt', 'w')
# write the header line
f2.write(f'{"Vx":<10} {"Vy":<10} {"Vz":<10} |V|\n')
for each1 in allV:
    # write to file
    f2.write(f'{each1[0]:<+10} {each1[1]:<+10} {each1[2]:<+10} {each1[3]:<+10.2f}\n')
# close the second file!
f2.close()


# print statements to make calculations easier to read
print(f'The mean value of |B| is {np.mean(absB):+.2f}')
print(f'The mean value of |V| is {np.mean(absV):+.2f}')
