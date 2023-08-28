import re
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from numpy import trapz
import pdb
import os
import pandas as pd
bp = breakpoint

plotmode = input("Enable Plot mode? (y/n)")

file_names = [i for i in os.listdir() if ".agr" in i]
file_names = [i for i in file_names if i[0] != "."]
if len(file_names) == 1:
    file_name = file_names[0]
else:
    for num,val in enumerate(file_names):
        print("{}: {}".format(num+1,val))

    valuechoice = input("Choose a file: \n")
    file_name = file_names[int(valuechoice)+0]

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

def get_end(gr,k):
    x = k[1]
    graddf = pd.DataFrame(np.array(np.array([x,gr]).T))
    graddf_redone = graddf[(np.abs(graddf[0]) > 1e-4) & (np.abs(graddf[1]) > 1e-4)]
    
    index = graddf_redone[0].index[-1]
    x_val = k[0][index]
    return x_val

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


    if plotmode == "y":
        end_value = get_end(gr,k)
        plt.plot(k[0],k[1], label="{}: {} nodes {} away".format(orbitals[i], len(new_z_vals), diff_from_correct))
        plt.xlim(0,end_value)
        plt.legend()
        plt.show()
