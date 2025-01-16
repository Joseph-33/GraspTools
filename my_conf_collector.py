################################################
#                                              #
#  Welcome to configuration collector!         #
#                                              #
#  A script that reads the logs in rcsfpreview #
#  and obtains the number of CSFs generated.   #
#  Best runs with conf_collector.sh            #
#                                              #
#  Can run 23x faster than standard generate   #
#                                              #
#  INPUTS:                                     #
#        ARG 1: rcsfpreview logfile path       #
#        ARG 2: rcsfpreview input file path    #
#                                              #
#  OUTPUTS:                                    #
#        CSF info print to screen              #
#                                              #
################################################

import numpy as np
import sys
import pdb
bp = breakpoint

logfile = sys.argv[1] 
inp_file = sys.argv[2]

with open(logfile,"r") as f: # Read logfile
    lines = f.readlines()

with open(inp_file,'r') as fil: # Read input file
    lines_inp1 = fil.readlines()

#lines_inp = "".join(lines_inp[2:]).split("\n\n")[0].split("\n")
lines_inp = []
for i in lines_inp1:
    if "(" in i: # Get CSF info
        lines_inp.append(i.strip())
print(lines_inp1[-4].strip())

num = 0
value = []
for i in range(len(lines)): # Extracts the number of CSFs generated from the large logs
    if "been generated" in lines[i]:
        value_temp = lines[i].strip().split(" ")[0]
        if value_temp == "One":
            value_temp = 1
        value.append(int(value_temp))
        
        
        value[num] = str(value[num])
        #value[num] = int(value[num])
        print("{:2s}    {:11s}   ".format(str(num+1),value[num]) + lines_inp[num])
        num += 1

value_int = [int(i) for i in value]
print("cumsum: {:.2e}".format(sum(value_int)))
print("cumsum even with 4f for largest block of {:.2e}".format(sum(value_int) * .21544 )) # Prints the value with the estimated reduction after running rcsfinteract.
