import numpy as np
import collections
import os.path
import re
import pdb

print("""
########################################
#  Welcome to Duplicate CSF remover!   #
#                                      #
#  Removes CSFs that are duplicate     #
#  Very useful for custom made         #
#  or combined CSF lists               #
#                                      #
#  Orders of magnitude faster than     #
#  Standard GRASP version              #
#                                      #
#  INPUTS:                             #
#         Input CSF list               #
#                                      #
#  OUTPUTS:                            #
#         List without duplicates      #
#                                      #
#                                      #
########################################
""")


infile = "rcsf.inp"
outfile = "rcsf.out"

print("Warning: This removes the block markers, run rcsfblock afterwards")

filans = input("The input and output files are:\nInput: {}\nOutput: {}\nWould you like to change them? (y/n)\n".format(file_name,out_name))
if filans.lower() == 'y':
    file_name = input("Type input name: \n")
    out_name = input("Type output name: \n")

def star_remover(csf,starindex=False):
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
    stars_n = [1 for i in sti if elem > i]
    stars = sum(stars_n)
    #print(stars,sti, stars_n, elem)
    return 3 + (elem + 1) * 3 + stars

with open(infile,'r') as fil:
    lines = fil.readlines()

csf_raw1 = lines[5:]
csf1, sti1 = star_remover(csf_raw1, starindex=True)
#group1 = [csf1[i:i+3] for i in range(0, len(csf1), 3)]

group1 = ["".join(csf1[i:i+3]) for i in range(0, len(csf1), 3)]
srt2 = list(collections.OrderedDict.fromkeys(group1))


print("Before:",len(group1))
print("After:",len(srt2))
with open(outfile,'w') as fil:
    fil.write("".join(lines[:5]))
    for i in srt2:
        fil.write(i)



