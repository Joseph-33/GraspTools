import numpy as np
import collections
import os.path
import re
import pdb
bp = breakpoint

nextlay = "rcsf.inp"
rmix_fil = "rcsfmix.out"
output = "rcsflastlay.out"

ansch = input("Choose an option: \n(1) orblays\n(2) remove full 4f\n")
if ansch == 1:
    orblays = ["13s","13p","13d","13f"]
    print("Using:"," ".join(orblays))
elif ansch == 2:
    str4f = "  5f-( 6)  5f ( 8)"
    print("Using:",str4f)
else:
    print("Choose either 1 or 2")
    exit()

ans = input("Add the files from {}? (y/n): ".format(rmix_fil))
if ans.lower() == "y":
    rmix_q = True
else:
    rmix_q = False

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

with open(nextlay,'r') as fil:
    lines = fil.readlines()


csf_raw1 = lines[5:]
csf1, sti1 = star_remover(csf_raw1, starindex=True)
group1 = [csf1[i:i+3] for i in range(0, len(csf1), 3)]

group1_mod = [] # First loop is orblays
#for csf in group1:
#    if any(orb in csf[0] for orb in orblays):
#        group1_mod.append(csf)
for csf in group1: # Here is the things for 4f full
    if str4f not in csf[0]:
        group1_mod.append(csf)

group1_modbigstr = ["".join(i) for i in group1_mod]
group1_modstr = "".join(group1_modbigstr)

with open(rmix_fil,'r') as fil:
    linesmix = fil.readlines()

csf_raw2 = linesmix[5:]
csf2, sti2 = star_remover(csf_raw2, starindex=True)
group2 = [csf2[i:i+3] for i in range(0, len(csf2), 3)]

group2_modbigstr = ["".join(i) for i in group2]
group2_modstr = "".join(group2_modbigstr)

with open(output,'w') as fil2:
    fil2.write("".join(lines[:5]))
    if rmix_q:
        fil2.write(group2_modstr)
    fil2.write(group1_modstr)
print("Previous: ",len(group1))
print("After + rmix:",len(group1_mod)," + ",len(group2))
print(len(group1_mod)+len(group2))

#with open(sec,'r') as fil:
#    lines2 = fil.readlines()
#
#csf_raw2 = lines2[5:]
#csf2, sti2 = star_remover(csf_raw2, starindex=True)
#group2 = [csf2[i:i+3] for i in range(0, len(csf2), 3)]
