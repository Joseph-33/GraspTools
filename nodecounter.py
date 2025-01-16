#########################################################
#                                                       #
#  WARNING: DEPRECATED!                                 #
#                                                       #
#  DEPRECATED! Functions moved to waveanalysis.py       #
#                                                       #
#  Welcome to node Counter!                             #
#                                                       #
#########################################################



import re
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from numpy import trapz
import pdb
from os import listdir
import pandas as pd
from fnmatch import filter as fnfilter
bp = breakpoint

def expand_filter_pattern(pattern):
    match = re.match(r'(\d*)>', pattern)
    if match:
        numeric_part = match.group(1)
        if numeric_part:
            return [str(i) + '*' for i in range(1, int(numeric_part) + 1)]
    return [pattern]

def filter_atomic_orbitals(custom_orbitals, filter_list):
    expanded_filter_list = []
    for pattern in filter_list:
        expanded_filter_list.extend(expand_filter_pattern(pattern))

    filtered_orbitals = []

    for pattern in expanded_filter_list:
        match = re.match(r'(\d*)(.*)', pattern)
        if match:
            numeric_part = match.group(1)
            non_numeric_part = match.group(2)

            if numeric_part:
                start_pattern = int(numeric_part)
                end_pattern = start_pattern + 1
            else:
                start_pattern = 1
                end_pattern = 10  # Assuming a default maximum pattern of 9

            for i in range(start_pattern, end_pattern):
                filtered_orbitals.extend(fnfilter(custom_orbitals, str(i) + non_numeric_part))
        else:
            filtered_orbitals.extend(fnfilter(custom_orbitals, pattern))

    return filtered_orbitals

plotmode = input("Enable Plot mode? (y/n)\n")
filter_list=[]
if plotmode == "y":
    custom_orbitals_selec = input("Selected orbitals only? (y/n)\n")

    if custom_orbitals_selec == "y":
        filter_list = input("input the selected orbitals seperated by a space, use wildcards such like 2* = 2s 2p 2p-, 2> = 1s, 2s 2p- 2p\n")
        filter_list = filter_list.split()
        filter_list = [i for i in filter_list if i]

file_names = [i for i in listdir() if ".agr" in i]
file_names = [i for i in file_names if i[0] != "."]
if len(file_names) == 1:
    file_name = file_names[0]
else:
    for num,val in enumerate(file_names):
        print("{}: {}".format(num+1,val))

    valuechoice = input("Choose a file: \n")
    file_name = file_names[int(valuechoice)-1]
print(file_name)
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

allowed_orbitals = filter_atomic_orbitals(orbitals,filter_list)
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
    print("{:4s}: {} nodes {} away from the correct node of {}".format(orbitals[i], len(new_z_vals), diff_from_correct, correct_node))


    if plotmode == "y":
        if orbitals[i] not in allowed_orbitals:
            continue
        print(orbitals[i])
        end_value = get_end(gr,k)
        plt.plot(k[0],k[1], label="{}: {} nodes {} away".format(orbitals[i], len(new_z_vals), diff_from_correct))
        plt.xlim(0,end_value)
        plt.legend()
        plt.show()
