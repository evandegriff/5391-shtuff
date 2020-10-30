#!/usr/bin/env python3

"""
Python file for Homework 4

Contains two functions: 
    weasel_program : does actual convergence to target phrase
    explore_var: creates plots for range of mutation rates or generation sizes
    
Short test cases showcase both functions at the bottom.
"""

import random # need for making mutations, generating starting string
import string # need to generate list of allowed chars
import numpy as np # yay numpy
import matplotlib.pyplot as plt # visualize that data
import os # make folders for plotting

# specify where plots end up
out_dir = './plots/'

# make output dir if it doesn't exist
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

def weasel_program(gen_size, mutation_rate, target_phrase, printout=False):
    '''
    Generates a random string of characters, then creates a "generation" of
    strings by changing the "parent" string at a certain "mutation rate."
    The "offspring" that is closest to the target phrase becomes the new
    parent, and the cycle continues until the target phrase is reached.

    Parameters
    ----------
    gen_size : int
        Specifies how many offspring in each generation.
    mutation_rate : int
        Percentage of how likely a letter is to change.
    target_phrase : str
        String of characters from the alphabet and the space character that
        the program will attempt to converge to.
    printout : boolean
        if True, prints generation size, mutation rate, and convergence to 
        screen

    Returns
    -------
    gen_num : int
        How many generations needed to reach target phrase.

    '''
    # printing starting info to screen
    if printout: print(f'Mutation rate is: {mutation_rate}')
    # printing starting info to screen
    if printout: print(f'Generation size is: {gen_size}')
    # define string of alphabet
    alph_string = string.ascii_uppercase
    # create array of alphabet
    allowed = list(alph_string)
    # add space to make a complete list of allowed chars
    allowed.append(' ')
    # prep an empty string
    start_string = ''
    # define starting string of random chars, same length as target phrase
    for i in range(len(target_phrase)):
        start_string += random.choice(allowed)
    # set starting generation
    # note: generation 0 is the starting string we just defined, start at 1
    gen_num = 1
    # loop through until start string has been transformed into target phrase
    while start_string != target_phrase:
        # increment generation
        gen_num += 1
        # create empty list of strings
        offspring_list = []
        #loop through to create offspring
        for x in range(gen_size):
            # create empty string
            offspring = ''
            # loop through parent string
            for char in start_string:
                # set the new character as the original one to start
                newchar = char
                # use mutation rate and random module to see if letter changes
                if random.randrange(0, 100) <= 4:
                    # make sure mutated char won't "mutate" to the same letter
                    while newchar == char:
                        newchar = random.choice(allowed)
                # append char to offspring string
                offspring += newchar
            # append offspring string to offspring list
            offspring_list.append(offspring)
        # create empty dict
        offspring_dict = {}
        # loop through offspring list
        for each_offspring in offspring_list:
            # start the offspring's score as 0
            score = 0
            # loop through chars of offspring
            for j in range(len(target_phrase)):
                # if any chars match target phrase, add one to offspring score
                if each_offspring[j] == target_phrase[j]:
                    score += 1
            # assign the total score to the offspring
            offspring_dict[each_offspring] = score
        # get offspring with max score, define as new starting string
        start_string = max(offspring_dict, key=offspring_dict.get)
        # print(start_string)
    if printout: print(f'{gen_num} generations Needed to reach target phrase.')
    # return the number of generations it took to reach target phrase
    return gen_num



def explore_var(var_name, var_start, var_stop, num_runs, fixed_var, target_phrase):
    '''
    Explores a parameter of weasel_program, either generation size or mutation
    rate, keeping the other fixed. Plots the average convergence over a 
    specified number of runs for each integer step of the variable value over
    a specified range.

    Parameters
    ----------
    var_name : str
        Variable to be explored: either "Generation Size" or "Mutation Rate".
    var_start : int
        Start value for relevant variable.
    var_stop : int
        Stop value for relevant variable.
    num_runs : int
        How many runs of weasel program to make before taking mean convergence.
    fixed_var : int
        Value for fixed variable that is not being explored.
    target_phrase : str
        String of characters from the alphabet and the space character that
        the program will attempt to converge to.

    Raises
    ------
    ValueError
        If var_name entered is neither "Generation Size" nor "Mutation Rate",
        throws an error.

    Returns
    -------
    None. Plots saved to specified directory

    '''
    # make sure correct variables are inputted
    if var_name != "Generation Size" and var_name != "Mutation Rate":
        raise ValueError("var name must be 'Generation Size' or 'Mutation Rate' ") 
    # define empty dict for all values
    all_values = {}
    # define empty dict for mean values
    mean_values = {}
    # loop through range of variable from start to stop range:
    for x in range(var_start,var_stop+1):
        # output to keep track of how far the program has gotten
        print(f'{var_name} = {x}')
        # in all values dict, save key=variable and value=empty list
        all_values[x] = []
        #time to run the weasel program num_runs times!
        for y in range(num_runs):
            # run weasel prog, for variable gen size and fixed mutation rate
            if var_name == "Generation Size":
                gens = weasel_program(x, fixed_var, target_phrase)
            # run weasel prog, for variable mutation rate and fixed gen size
            elif var_name == "Mutation Rate":
                gens = weasel_program(fixed_var, x, target_phrase)
            # add output of weasel program to list for given variable value
            all_values[x].append(gens)
        # take mean of all runs for each generation size/mutation rate
        # assign mean value to given variable value
        mean_values[x] = np.mean(all_values[x])
    # print the final mean values dict
    print(mean_values)        
    # plot the dependency of the variable in question
    # define a figure
    fig = plt.figure(figsize=(15,5))
    # specify axis
    ax = plt.subplot(111)
    # set y-axis label
    ax.set_ylabel('Mean Num of Generations')
    # set x-axis label
    ax.set_xlabel(var_name)
    # plot mean generations v. values
    ax.plot(mean_values.keys(), mean_values.values())
    # set plot title
    ax.set_title('Number of Gens to Reach Target Phrase as Fn of {var_name}')
    # create file output name
    outfile_name = out_dir + f'{var_name[:3]}_mean_{num_runs}_{var_start}_to_{var_stop}.png'
    # save the plot
    plt.savefig(outfile_name)
    #close all plots
    plt.close('all')





# specify target phrase
target_phrase = 'METHINKS IT IS LIKE A WEASEL'
# define mutation rate as an integer percentage
mut_rate = 4
# define generation size
gen_size = 100
# single run of the weasel program
weasel_program(gen_size, mut_rate, target_phrase, printout=True)

# average of a thousand runs, with fixed mutation rate and gen size
# NOTE: this part takes several minutes to run - you have been warned. uncomment at own risk
# all_runs = []
# for j in range(1000):
#     all_runs.append(weasel_program(gen_size, mut_rate, target_phrase))
# mean_conv = np.mean(all_runs)
# print(f'Mean convergence over 1000 runs = {mean_conv}')

#some very simple explore_var runs
explore_var("Generation Size", 100, 105, 10, mut_rate, target_phrase)
explore_var("Mutation Rate", 4, 10, 10, gen_size, target_phrase)