#!/usr/bin/env python3
"""
Function to converge on a phrase using generations of random characters that can mutate, etc.
"""
import random
import string
    

def weasel_program(gen_size, mutation_rate, target_phrase):
    '''
    yeaaaaah boiiiiiiii

    Parameters
    ----------
    gen_size : TYPE
        DESCRIPTION.
    mutation_rate : TYPE
        DESCRIPTION.
    target_phrase : TYPE
        DESCRIPTION.

    Returns
    -------
    gen_num : TYPE
        DESCRIPTION.

    '''
    # define array of allowed characters
    alph_string = string.ascii_uppercase
    allowed = list(alph_string)
    allowed.append(' ')
    # define starting string of random chars, same len as target phrase
    start_string = ''
    for i in range(len(target_phrase)):
        start_string += random.choice(allowed)
    gen_num = 1
    while start_string != target_phrase:
        # print(gen_num)
        gen_num += 1
        # create empty list of strings
        offspring_list = []
        for x in range(gen_size):
            # create empty string
            offspring = ''
            for char in start_string:
                newchar = char
                if random.randrange(0, 100) <= 4:
                    while newchar == char:
                        newchar = random.choice(allowed)
                # append char to string
                offspring += newchar
            # append string to list
            offspring_list.append(offspring)
        # create empty dict
        offspring_dict = {}
        # loop through list of strings, add each to dict: key is phrase
        # value is score of how close it is to target phrase
        for each_offspring in offspring_list:
            score = 0
            for j in range(len(target_phrase)):
                if each_offspring[j] == target_phrase[j]:
                    score += 1
            offspring_dict[each_offspring] = score
        # get string with max score, define as new starting string
        start_string = max(offspring_dict, key=offspring_dict.get)
        # print(start_string)
    #print(f'{gen_num} generations Needed to reach target phrase.')
    return gen_num


if __name__ == '__main__':
    # define target phrase
    target_phr = 'METHINKS IT IS LIKE A WEASEL'
    # define mutation rate as an integer percentage
    mut_rate = 4
    print(f'Mutation rate is: {mut_rate}')
    # define generation size
    gens = 100
    print(f'Generation size is: {gens}')
    weasel_program(gens, mut_rate, target_phr)