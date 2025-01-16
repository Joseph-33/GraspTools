print("""
######################################################
#                                                    #
#  Welcome to RCSFZEROFIRST Python Edition!          #
#                                                    #
#  Similar to rcsfzerofirst, but faster by factors   #
#  of 480!                                           #
#                                                    #
#  INPUT:                                            #
#        Zero-order space CSF list                   #
#        List to partition into first and zero space #
#                                                    #
#  Output:                                           #
#        rcsf.out                                    #
#                                                    #
######################################################
""")

import numpy as np
import pdb
bp = breakpoint

filename2 = "rcsf.inp"
filename3 = "rcsfmr_4n_z39rdl2_l2.inp"

filename3 = input("Please give the zero order space:\n")
filename2 = input("Please give the list you want to partition\n")

def blocklessreader(filename):
    """
    Reads the CSF lists, does not consider block information

    INPUTS:
        filename

    OUTPUTS:
        CSF list
        Header information
    """
    print("Reading: ", filename)
    with open(filename,'r') as csffil:
        rawlines = csffil.readlines()
    lines = rawlines[5:]
    initlines = rawlines[:5]
    fulllines = []
    for i in range(0,len(lines),3):
        fulllines.append("".join(lines[i:i+3]))

    return fulllines, initlines

# Load the CSFs into memory and transform into sets for time and space efficiency
allcsfs2, initlines2 = blocklessreader(filename2)
allcsfs3, initlines3 = blocklessreader(filename3)
setmr = set(allcsfs3) #
lenbig = len(allcsfs2)
lensmall = len(allcsfs3)
lendiff = lenbig - lensmall
string_array = np.empty(lendiff, dtype='<U1024')
final = []

print("Zerospace: ", lensmall)
print("Partition list", lenbig)

j=0
thresholds = {i: (i * lenbig) // 10 for i in range(1, 11)} # Every 10% will print to screen of partially complete
for i in range(len(allcsfs2)):
    if i in thresholds.values():
        print(i, "{:.4f}".format(i/lenbig * 100))
    if allcsfs2[i] in setmr:
        continue
    string_array[j] = allcsfs2[i] # Removes zerospace CSFs from main list
    j += 1
with open("rcsf.out",'w') as fil:
    fil.write("".join(initlines2)) # Save header
    fil.write("".join(allcsfs3))   # Save zerospace CSFs
    fil.write("".join(string_array.tolist())) # Save remaining CSFs

