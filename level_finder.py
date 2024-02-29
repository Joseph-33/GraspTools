import sys

filename = sys.argv[1]
if len(sys.argv) == 3:
    selecter = sys.argv[2]
else:
    selecter = ""

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

if selecter:
    select_parted = selecter.strip().split()
    if len(select_parted) > 1:
        J_sel = select_parted[0]
        P_sel = select_parted[1]
    else:
        J_sel = select_parted
        P_sel = ""

for massive in blockmerge:
    items = massive[0].split()
    block = int(items[0]) - 1
    level = int(items[1])
    J = items[2]
    parity = items[3]
    contribs = items[4:]

    csfnumbs = massive[1].split()
    csfnumbs = [ int(i) for i in csfnumbs]

    if selecter:
        if J != J_sel:
            continue
        if P_sel:
            if parity != P_sel:
                continue
    print("\n",J,parity,level, csfnumbs)

    for csfnumb in range(len(csfnumbs[:3])):
        csf = allcsfs[block][csfnumbs[csfnumb]-1]
        print("{:7s}".format(contribs[csfnumb]), csf)



