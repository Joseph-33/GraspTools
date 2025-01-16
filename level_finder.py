print("""
#################################################
#  Welcome to Level Finder!                     #
#                                               #
#  This program gives the configuration from    #
#  the logs in rmcdhf.                          #
#                                               #
#  INPUTS:                                      #
#        rcsf.inp file in cwd                   #
#        Argument 1: log path                   #
#                                               #
#        Argument 2: (optional) JP Selector     #
#        J Parity selector                      #
#        Format is JP, e.g. 5-                  #
#                                               #
#  OUTPUTS:                                     #
#        Configuration for each level           #
#                                               #
#################################################
""")

import sys

filename = sys.argv[1] # Get filename from first argument
if len(sys.argv) == 3:
    selector = sys.argv[2] # Get the file selector, if it exists
else:
    selector = ""

def allcsfsgen():
    """
    Get a list of all CSFs
    INPUTS:
        Filename: rcsf.inp

    OUTPUTS:
        A list of all CSFs by block

    """
    with open("rcsf.inp",'r') as csffil:
        rawlines = csffil.readlines()
    
    lines = rawlines[5:]
    
    total = "".join(lines)
    blockspl = total.split("*")
    
    allcsfs = []
    for i in range(len(blockspl)):
        block = blockspl[i].split("\n")
        block = [ i for i in block if i.strip()][::3]
        allcsfs.append(block)

    return allcsfs

allcsfs = allcsfsgen() # Get all the CSFs into a list

#filename = "rmcdhf_log.log"
with open(filename,'r') as fil:
    read = fil.read()

tex = "Weights of major contributors to ASF" # Use find function to search the logs text, extraxt the important text.

ind = read.rfind(tex)
blocks = read[ind:].split("\n\n")[2]
blockspl = blocks.split("\n")

blockmerge = [ list(x) for x in zip(blockspl[0::2], blockspl[1::2]) ]

if selector: # If selector is used, only print blocks with that J value.
    select_parted = selector.strip().split()
    if len(select_parted) > 1:
        J_sel = select_parted[0] # Select the J value
        P_sel = select_parted[1] # Select the Parity
    else:
        J_sel = select_parted
        P_sel = ""

for massive in blockmerge: # Loop around the blocks of J and P
    items = massive[0].split()
    block = int(items[0]) - 1
    level = int(items[1])
    J = items[2]
    parity = items[3]
    contribs = items[4:]

    csfnumbs = massive[1].split()
    csfnumbs = [ int(i) for i in csfnumbs]

    if selector:
        if J != J_sel:
            continue
        if P_sel:
            if parity != P_sel:
                continue
    print("\n",J,parity,level, csfnumbs) # Print level and block information

    for csfnumb in range(len(csfnumbs[:3])): # First three most important CSFs
        csf = allcsfs[block][csfnumbs[csfnumb]-1]
        print("{:7s}".format(contribs[csfnumb]), csf) 



