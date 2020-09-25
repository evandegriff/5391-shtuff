#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 00:19:23 2020

@author: exv3640
"""


import sciprog as sp
import numpy as np


allData = sp.read_imf('imf_aug2005.dat')

absB = np.sqrt(allData['bx']**2 + allData['by']**2 + allData['bz']**2)
allB = np.array(list(zip(allData['bx'], allData['by'], allData['bz'], absB)))

absV = np.sqrt(allData['vx']**2 + allData['vy']**2 + allData['vz']**2)
allV = np.array(list(zip(allData['vx'], allData['vy'], allData['vz'], absV)))


f = open('b_out.txt', 'w')
f.write(f'{"Bx":<10} {"By":<10} {"Bz":<10} |B|\n')
for each in allB:
    f.write(f'{each[0]:<+10} {each[1]:<+10} {each[2]:<+10} {each[3]:<+10.2f}\n')
f.close()

f2 = open('v_out.txt', 'w')
f2.write(f'{"Vx":<10} {"Vy":<10} {"Vz":<10} |V|\n')
for each1 in allV:
    f2.write(f'{each1[0]:<+10} {each1[1]:<+10} {each1[2]:<+10} {each1[3]:<+10.2f}\n')
f2.close()


print(f'The mean value of |B| is {np.mean(absB):+.2f}')
print(f'The mean value of |V| is {np.mean(absV):+.2f}')