print("""
##############################################
#  Welcome to configuration from CSF!        #
#                                            #
#  Creates a list of configurations          #
#  from a CSF list.                          #
#  Can compare to a MR List                  #
#                                            #
#  INPUTS:                                   #
#        rcsf.out - CSF List                 #
#        mr_confs - MR List (optional)       #
#                                            #
#  OUTPUTS:                                  #
#       out.out - List of configurations     #
#       (optional)                           #
#                                            #
##############################################
""")


import numpy as np
import os.path
import re
import pdb
bp = breakpoint


infile = "rcsf.out"
outfile = "out.out"

def order(a):
    """ Order function, inputs an electronic orbital and returns a number
        allowing the orbitals to be sorted properly

        INPUTS:
            Electronic Orbital, e.g. 6p

        OUTPUTS:
            Integer
    """
    a_separated = re.split("(\d+)",a)[1:]
    returned = int(a_separated[0]) * 10 + dic[a_separated[1]]
    return returned

def order_gen(a):
    """ Order generating function, calls order function.

    Splits electronic configuration into a list, then sorted based upon a key from order.

    INPUTS:
        Electronic configuration

    OUTPUTS:
        Sorted Electronic Configuration

    """

    nl = []
    for i in a:
        i = re.split("(\d+\D\(.*?\))", i)
        i = [j for j in i if j]
        i = sorted(i, key=lambda x:order(x.split('(')[0]))
        nl.append("".join(i))
    return nl


def mr_confs_gen(confs):
    """ Loads the configurations and the MR configurations to take the difference 

        INPUTS:
            List of configurations

        Outputs:
            Ordered list of configurations not in the MR

    """
    with open("mr_confs","r") as fil:
        mr_vals = fil.readlines()

    mr_vals = [i.strip() for i in mr_vals]

    confs_list = list(confs)
    confs_list_ord = order_gen(confs_list) # Sorts the configuration list
    mr_vals_ord = order_gen(mr_vals)       # Sorts the MR list

    diffs = [x for x in confs_list_ord if x not in mr_vals_ord] # Takes the difference
    return diffs

# Asks the user questions
ans = input("Using '{}' as output file, change settings? (y/n) (Leave blank to continue)\n".format(outfile))
if ans.lower() == "y":
    numbers = input("Remove numbers from list?\n")
    if numbers.lower() == "y":
        numb = True
    else:
        numb = False
    outquestion = input("Should the filename be changed?\n")
    if outquestion.lower() == "y":
        outfile = input("What should the output name be?\n")
    else:
        outfile = ""
else:
    numb = ""

with open(infile,'r') as fil: # Loads the main CSF file
    lines = fil.readlines()

mr_confs = os.path.isfile("mr_confs") # Checks for mr_confs
if mr_confs:
    print("mr_confs file found")
else:
    print("mr_confs file not found")

nl = []
for i in lines[5:]: # Removes the header
    i=i.strip()
    if "*" in i: # Removes the blocks seperators
        continue
    if "(" not in i: # Removes angular momentum information
        continue
    i = i.replace("-"," ")
    nl.append(i)

# This block of code loads the list of configurations, and changes them into a suitable format. Including removing relativistic information, angular momentum, and sorting them.

sl = sorted(set(nl), key=lambda x: nl.index(x)) 
configurations = [] 
for i in range(len(sl)):
    sl[i] = sl[i].replace(" ","") # Remove space
    sl[i] = re.split("(\d+\D\(\d+\))", sl[i]) # Turn a configuration into a list of orbitals and occupation
    sl[i] = list(filter(None, sl[i])) # Remove empty values

    my_dict = {} 
    for j in range(len(sl[i])): # Place the orbitals into a dictionary for organisation.
        
        orbital = re.split("(\d+\D)\(\d+\)", sl[i][j])
        occupation = re.split("\d+\D\((\d+)\)", sl[i][j])
        occupation = list(filter(None, occupation))[0]
        orbital = list(filter(None, orbital))[0]
        my_dict[orbital] = my_dict.get(orbital, 0) + int(occupation)

    configuration_list = ["{}({})".format(orb, occ) for orb, occ in zip(my_dict.keys(), my_dict.values())] 
    # Put orbitals back into string format.
    configurations.append("".join(configuration_list))
configurations = set(configurations) # Remove duplicate configurations

configurations = sorted(configurations) # Sort
string_out = "\n".join(configurations)
print("All configurations:\n")
if numb:
    print(string_out)
else:
    for i in range(len(configurations)):
        print("{:3s} {}".format(str(i+1) + ":",configurations[i]))


if mr_confs: # If mr_confs file present
    diff_list = mr_confs_gen(configurations)
    diff_list = sorted(diff_list)
    print("\nConfs not in mr list:\n")
    diffs = "\n".join(diff_list)
    if numb:
        print(diffs)
    else:
        for i in range(len(diff_list)):
            print("{:3s} {}".format(str(i+1) + ":",diff_list[i]))

    if outfile:
        with open(outfile,"w") as f:
            f.write(string_out)
            f.write("\n")


elif outfile: # Print configurations
    with open(outfile,"w") as f:
        f.write(string_out)
        f.write("\n")
