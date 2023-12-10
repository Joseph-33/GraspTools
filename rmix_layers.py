import numpy as np
import collections
import os.path
import re
import pdb
bp = breakpoint

# Input files
nextlay = "rcsf.inp"
rmix_fil = "rcsfmix.out"
output = "rcsflastlay.out"

# Functions
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

def file_process(lines):
    csf_raw = lines[5:]
    csf, sti = star_remover(csf_raw, starindex=True)
    group = [csf[i:i+3] for i in range(0, len(csf), 3)]

    return group

# Questions
ansch = int(input("Choose an option: \n(1) orblays\n(2) remove full 4f\n(3) Some combination of both"))
if ansch == 1:
    orblays = ["13s","13p","13d","13f"]
    print("Using:"," ".join(orblays))
elif ansch == 2:
    str4f = "  5f-( 6)  5f ( 8)"
    print("Using:",str4f)
elif ansch == 3:
    orblays = ["11s","11p","10d","8f","8g","7g"]
    str4f = "  5f-( 6)  5f ( 8)"
    print("Using:",str4f)
else:
    print("Choose either 1, 2 or 3")
    exit()

ans = input("Add the files from {}? (y/n): ".format(rmix_fil))
if ans.lower() == "y":
    rmix_q = True
else:
    rmix_q = False

# Open
with open(nextlay,'r') as fil:
    lines = fil.readlines()

with open(rmix_fil,'r') as fil:
    linesmix = fil.readlines()

# Process the files
group1 = file_process(lines)
group2 = file_process(linesmix)

def modstr(group_mod):
    """ Formats the csfs from lists into strings ready to save to file"""
    group_modbigstr = ["".join(i) for i in group_mod]
    group_modstr = "".join(group_modbigstr)
    return group_modstr

def option1(group1, group2_mod):
    """ Removes csf from rcsfint if they do not contain an orbital in orblays """
    group1_mod = [csf for csf in group1 if any(orb in csf[0] for orb in orblays)]
    return group1_mod, group2_mod

def option2(group1, group2_mod):
    """ Remove csf if it contains full 5f core """
    group1_mod = [i for i in group1 if str4f not in i[0]]
    return group1_mod, group2_mod

def option3(group1, group2_mod):
    """ Remove csf if it contains full 5f core or does not contain orbital in orblays """
    group1_mod = [] # First loop is orblays
    for csf in group1: # Here is the things for 4f full
        if str4f not in csf[0] and any(orb in csf[0] for orb in orblays):
            group1_mod.append(csf)
    return group1_mod, group2_mod
def option4(group1, group2):
    """ Removes csf if contains full 5f core or does not contain orbital in orblays, but keeps all 1/2- csfs
    Also remove all 1/2- csfs from the rmix file to avoid duplicates"""
    group1_mod = [] # First loop is orblays
    for csf in group1: # Here is the things for 4f full
        trth1 = "1/2-" in csf[-1]
        trth2 = str4f not in csf[0] and any(orb in csf[0] for orb in orblays)
        if trth1 or trth2:
            group1_mod.append(csf)
    group2_mod = [csf2 for csf2 in group2 if "1/2-" not in csf2[-1]]

    return group1_mod, group2_mod


        

if ansch == 1:
    group1_mod, group2_mod = option1(group1, group2)
elif ansch == 2:
    group1_mod, group2_mod = option2(group1, group2)
elif ansch == 3:
    group1_mod, group2_mod = option3(group1, group2)
elif ansch == 4:
    group1_mod, group2_mod = option4(group1, group2)

group1_modstr = modstr(group1_mod)
group2_modstr = modstr(group2_mod)

print("Previous: ",len(group1))
with open(output,'w') as fil2:
    fil2.write("".join(lines[:5]))
    if rmix_q:
        fil2.write(group2_modstr)
        print("After + rmix:",len(group1_mod)," + ",len(group2))
    else:
        fil2.write(group1_modstr)
print(len(group1_mod)+len(group2))

