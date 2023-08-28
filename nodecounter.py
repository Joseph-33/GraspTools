import re
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from numpy import trapz
import pdb
import os
import pandas as pd
bp = breakpoint

#file_name = "xmgrace_odd_SD_sm1.agr"
file_name = [i for i in os.listdir() if "xmgrace" in i][0]
n_cols = 3

def to_numeric_func(x):
    try:
        return pd.to_numeric(x)
    except ValueError as e:
        return np.nan


def node_corr(a):
    dic = {"s":0, "p":1, "d":2, "f":3,"g":4,"h":5}
    princ = int(re.search("\d+",a).group())
    ell = re.search("\D",a).group()
    return princ - dic[ell] - 1

with open(file_name,'r') as f:
    readall = f.read()

readall = readall.replace("D","E")
datasets = readall.split("\n\n")[:-1]

first = datasets[0].split("\n") 
datasets[0] = "\n".join(first[3:])

orbitals = []
for i in range(len(datasets)):
    dataset = datasets[i].split("\n") [1:]
    orbitals.append(dataset[0].replace("#","").replace(" ",""))
    dataset = " ".join(dataset[1:])
    dataset = dataset.split()
    array = np.array(dataset).reshape(( int(len(dataset)/3), 3))

    newdf = pd.DataFrame(array)
    newdf = newdf.apply(pd.to_numeric, errors='coerce')
    newdf = newdf.dropna()
    df = newdf.to_numpy().T
    datasets[i] = df


for i in range(len(datasets)):
    k = datasets[i]
    z = np.where(np.diff(np.signbit(k[1])))[0]

    z_vals = [k[0][j] for j in z]

    gr = np.gradient(k[1])

    gr_vals = [abs(gr[j]) for j in z]

    new_z_vals = []
    for vals in range(len(z_vals)):
        if z_vals[vals] < 0.01:
            continue
#        elif z_vals[i] > 0.95 * k[0][-1]:
#            continue
        elif gr_vals[vals] < 1e-4:
            continue

        new_z_vals.append(z_vals[vals])

    correct_node = node_corr(orbitals[i])
    diff_from_correct = abs(correct_node - len(new_z_vals))
    print("{:3s}: {} nodes {} away from the correct node of {}".format(orbitals[i], len(new_z_vals), diff_from_correct, correct_node))
