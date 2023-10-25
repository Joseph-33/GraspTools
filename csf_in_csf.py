import numpy as np
import collections
import os.path
import re
import pdb

infile = "tmp"
sec = "rcsf.out"

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
group1 = [csf1[i:i+3] for i in range(0, len(csf1), 3)]

with open(sec,'r') as fil:
    lines2 = fil.readlines()

csf_raw2 = lines2[5:]
csf2, sti2 = star_remover(csf_raw2, starindex=True)
group2 = [csf2[i:i+3] for i in range(0, len(csf2), 3)]


# Flag initialization

# Using Counter
for ind1, gr1 in enumerate(group1):
    flag = 0
    for ind2, elem in enumerate(group2):
        if collections.Counter(elem) == collections.Counter(gr1) :
            if gr1 == elem:
                flag = 1
                break
            else:
                print("ERROR!!!")

    if flag == 0:
        print("False")
        print(gr1)
    else:

        #print("True")
        print(linenum(ind1,sti1),linenum(ind2,sti2))
        #print(gr1,elem)
print("done")
