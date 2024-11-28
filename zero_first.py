import numpy as np
import sys
import pdb
bp = breakpoint

filename2 = "rcsf.inp"
filename3 = "rcsfmr_4n_z39rdl2_l2.inp"
filename2 = sys.argv[1]
filename3 = sys.argv[2]

print("#"*41)
print("##### RCSFZEROFIRST Python Edition ######")
print("#"*41)
print("Welcome to zerofirst, but faster by factors of 480!")
print("Input:\n\t Zerospace\n\t List to Partition\nOutput:\n\t rcsf.out\n")
filename3 = input("Please give the zero order space:\n")
filename2 = input("Please give the list you want to partition\n")

def blocklessreader(filename):
    print("Reading: ", filename)
    with open(filename,'r') as csffil:
        rawlines = csffil.readlines()
    lines = rawlines[5:]
    initlines = rawlines[:5]
    fulllines = []
    for i in range(0,len(lines),3):
        fulllines.append("".join(lines[i:i+3]))

    return fulllines, initlines

# def reader(filename):
#     with open(filename,'r') as csffil:
#         rawlines = csffil.readlines()
#     lines = rawlines[5:]
#     total = "".join(lines)
#     
#     blockspl = total.split("*") 
#     allcsfs = []
#     Js = []
# 
#     Ps = []
#     for i in range(len(blockspl)):
#         block = blockspl[i].split("\n")
#         block = [ "\n".join(block[j:j+3]) for j in range(0,len(block),3) if block[j].strip()]
#     return block
allcsfs2, initlines = blocklessreader(filename2)
allcsfs3, initlines = blocklessreader(filename3)
setmr = set(allcsfs3)
lenbig = len(allcsfs2)
lensmall = len(allcsfs3)
lendiff = lenbig - lensmall
string_array = np.empty(lendiff, dtype='<U1024')
final = []

j=0
thresholds = {i: (i * lenbig) // 10 for i in range(1, 11)}
for i in range(len(allcsfs2)):
    if i in thresholds.values():
        print(i, "{:.4f}".format(i/lenbig * 100))
    if allcsfs2[i] in setmr:
        continue
    string_array[j] = allcsfs2[i]
    j += 1
with open("rcsf.out",'w') as fil:
    fil.write("".join(initlines))
    fil.write("".join(allcsfs3))
    fil.write("".join(string_array.tolist()))

