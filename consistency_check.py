import numpy as np
import os
import pdb
import re
import pandas as pd
from collections import defaultdict
bp = breakpoint
sumnm = ["oddvsml_sci_layer8.sum"]


def fsumlog(sumnm):
    """ Opens the sum file and reads it"""
    with open(sumnm, 'r') as fil:
        smrd = fil.read()

    a=smrd.rfind("Self")
    b = smrd[a:]
    c = b.split("\n\n")[1]
    d = c.split("\n")

    dicsm = {}
    for i in d:
        spl = i.split()
        dicsm[spl[0]] = float(spl[1].replace("D","e"))
    return dicsm

def frmcdhf(rlog):
    """ Opens the rmcdhf log file and reads the last data section"""

    logpth = os.path.join(lognm,rlog)
    with open(logpth,'r') as fil:
        rd = fil.read()

    a = rd.rfind("Self")
    b = rd[a:].find("Average")

    c = rd[a:][:b].split("\n\n")[1]

    d = c.split("\n")

    dic = {}
    for i in d:
        i = i.split()
        dic[i[0]] = float(i[1].replace("D","e"))

    return dic

cwd = os.getcwd()

lognm = "logs"
logs = os.listdir(lognm)

rmcdhf_logs = [ i for i in logs if "rmcdhf" in i and i[0] != "."]

srt = defaultdict(list)
srt2 = defaultdict(list)

rgx = "(.*layer)(\d.*)"
rgxd = []
rgx2 = "((.*layer)\d+)_?(\d+)?"
rgxd2 = []

for rlog in rmcdhf_logs:

    rtn2 = re.search(rgx2,rlog)
    srt2[rtn2[1]].append(rtn2[3])

finals = [] # Builds finals, which is an unsorted list of the log files we want (not log2_1 when log2_3 exists)
for key, value in list(srt2.items()):
    try:
        integ = max([int(i) for i in value if i is not None])
        mrlog = "_" + str(integ)
    except:
        mrlog = ""
    finals.append(key + mrlog) 

for rlog in finals:
    
    rtn = re.search(rgx,rlog)
    srt[rtn[1]].append(rtn[0]) # Srt is a sorted dictionary of final
    
allvs = {}
allvstmp = {}
for rlog_gr in list(srt.items()):
    for rlog in rlog_gr[1]:
        allvstmp = {**allvstmp, **frmcdhf(rlog)}
    allvs = { **allvs, rlog_gr[0] : {**allvstmp} }

def sumlogmatch(sumnm, allvs, key):
    """ Match the energies of the sumd to the log files """
    sumd = fsumlog(sumnm)
    onevs = allvs[key]
    notsum = set(onevs) - set(sumd)
    if notsum:
        print("Values not in sumd, skipping: {}".format(notsum))
    notvs = set(sumd) - set(onevs)
    if notvs:
        print("Values not in onevs, skipping: {}".format(np.sort(list(notvs))))
    input("Press enter to continue\n")
    for orb in ( onevs.keys() ):

        if orb in notsum or orb in notvs:
            continue

        tr = np.round(onevs[orb],6) == np.round(sumd[orb],6)
        print(tr, orb)
        if tr == False:
            print(np.round(onevs[orb],6), np.round(sumd[orb],6), orb)
     

for key, sumnam in zip(allvs.keys(), sumnm):
    print("Matching {} with {}".format(key, sumnam))

    sumlogmatch(sumnam, allvs, key) # Run the match program

