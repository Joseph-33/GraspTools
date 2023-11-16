import sys

filename = sys.argv[1]

def allcsfsgen():
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

allcsfs = allcsfsgen()

#filename = "rmcdhf_log.log"
with open(filename,'r') as fil:
    read = fil.read()

tex = "Weights of major contributors to ASF"

ind = read.rfind(tex)
blocks = read[ind:].split("\n\n")[2]
blockspl = blocks.split("\n")

blockmerge = [ list(x) for x in zip(blockspl[0::2], blockspl[1::2]) ]

for massive in blockmerge:
    items = massive[0].split()
    block = int(items[0]) - 1
    level = int(items[1])
    J = items[2]
    parity = items[3]
    contribs = items[4:]

    csfnumbs = massive[1].split()
    csfnumbs = [ int(i) for i in csfnumbs]

    print("\n",J,level, csfnumbs)

    for csfnumb in range(len(csfnumbs[:3])):
        csf = allcsfs[block][csfnumbs[csfnumb]-1]
        print("{:7s}".format(contribs[csfnumb]), csf)



