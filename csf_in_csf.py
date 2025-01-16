print("""
############################################################
#  Welcome to the CSF in CSF verifier!                     #
#                                                          #
#  Checks whether a set of CSFs exist in another CSF list  #
#  Code also includes some consistency verification        #
#                                                          #
#  INPUTS:                                                 #
#        - Target CSF List                                 #
#        - Large CSF list to check                         #
#                                                          #
#  OUTPUTS:                                                #
#        - List of CSFs found with line numbers            #
#                                                          #
############################################################
""")

import numpy as np
import collections
import os.path
import re
import pdb

infile = "tmp"
sec = "rcsf.out"
filans = input("The large CSF list and CSFs to check are:\nInput: {}\nOutput: {}\nWould you like to change them? (y/n)\n".format(sec,infile))
if filans.lower() == 'y':
    infile = input("Type filename of CSFs to check: \n")
    sec = input("Type file name of large CSF list: \n")

def star_remover(csf,starindex=False):
    """ Removes block information from the CSF list
        Obtains the line numbers of CSFs in each block
        """
    nl = []
    sti = []
    for j,i in enumerate( csf ):
        if "*" in i:
            sti.append(int(j/3))
            continue
        nl.append(i)
    if not starindex:
        return nl
    else:
        return nl, sti

def linenum(elem,sti):
    """ 
     Obtains the line number of the particular CSF in the file, given the block number (number of stars) and number in the list.
    INPUTS:
        Element number
        Star information, sti

    OUTPUTS:
        Line number
    """

    stars_n = [1 for i in sti if elem > i]
    stars = sum(stars_n)
    #print(stars,sti, stars_n, elem)
    return 3 + (elem + 1) * 3 + stars

with open(infile,'r') as fil:  # Reads CSF file
    lines = fil.readlines()

csf_raw1 = lines[5:] # Remove header
csf1, sti1 = star_remover(csf_raw1, starindex=True) # Get block information
group1 = [csf1[i:i+3] for i in range(0, len(csf1), 3)]

with open(sec,'r') as fil: # Read second file
    lines2 = fil.readlines()

csf_raw2 = lines2[5:] # Remove header
csf2, sti2 = star_remover(csf_raw2, starindex=True) # Get block information
group2 = [csf2[i:i+3] for i in range(0, len(csf2), 3)]


# Flag initialization

# Using Counter
for ind1, gr1 in enumerate(group1): # Loop around the first file, for each of these CSFs
    flag = 0
    for ind2, elem in enumerate(group2): # Check each CSF to find line number
        if collections.Counter(elem) == collections.Counter(gr1) : # If found
            if gr1 == elem: # Use two separate methods to verify same string
                flag = 1
                break
            else:
                print("ERROR!!!") # Consistency verification failed

    if flag == 0: # CSF not found
        print("False")
        print(gr1)
    else:

        #print("True")
        print(linenum(ind1,sti1),linenum(ind2,sti2)) # CSF Found
        #print(gr1,elem)
print("done")
