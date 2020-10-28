#!/usr/bin/env python3
# file to explore my weasel program in various ways

import weasels as ws
import numpy as np
import matplotlib.pyplot as plt
import os

out_dir = './plots/'

if not os.path.exists(out_dir):
    # make output dir if it doesn't exist
    os.makedirs(out_dir)

target_phrase = 'METHINKS IT IS LIKE A WEASEL'
fixed_gen = 100
fixed_mut_rate = 4
# define function(variable range start and stop, plotting specifications):
#def explore_var(var_name, range_start, range_stop, units):
# define empty dict for all values
all_values = {}
# define empty dict for mean values
mean_values = {}
# loop through range of variable from start to stop range:
for x in range(1,100):
    print(f'Mutation rate = {x}')
    # in all values dict, save key=variable and value=empty list
    all_values[x] = []
    for y in range(1000):
        # run weasel program, append num_gen to dict[variable]
        gens = ws.weasel_program(fixed_gen, x, target_phrase)
        all_values[x].append(gens)
    # in mean values dict, save key=variable and value=mean of all values dict[variable]
    mean_values[x] = np.mean(all_values[x])

print(mean_values)
    
# plot that shit - num of gen to reach target as a fn of variable
# define a figure
fig = plt.figure(figsize=(15,5))
# specify axis
ax = plt.subplot(111)
# set y-axis label
ax.set_ylabel('Mean Num of Generations')
ax.set_xlabel('Mutation rate (%)')
# plot dst
ax.plot(mean_values.keys(), mean_values.values())
# set the x-axis limits
#ax.set_xlim([startTime, endTime])
# set plot title
ax.set_title('Number of Gens to Reach Target Phrase as Fn of Mutation Rate')
# create file output name
outfile_name = out_dir + 'gens_mutation_rate_mean_1000.png'
# save the plot
plt.savefig(outfile_name)
#close the plot; eh close them all, just to be safe
plt.close('all')