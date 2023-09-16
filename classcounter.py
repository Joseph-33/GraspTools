import re
import numpy as np
from scipy.signal import savgol_filter
from collections import defaultdict
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
    """
    Filters the wavefunction orbitals into the user-selected orbitals.
    The code allows for regex rules specified by the user.
    """
    if not filter_list:
        return custom_orbitals
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

def check_filterlist():
    """
    Asks the user if they want to enable plot mode and filter list
    """
    filter_list=[]
    custom_orbitals_selec = input("Selected orbitals only? (y/n)\n")

    if custom_orbitals_selec == "y":
        filter_list = input("input the selected orbitals seperated by a space, use wildcards such like 2* = 2s 2p 2p-, 2> = 1s, 2s 2p- 2p\n")
        filter_list = filter_list.split()
        filter_list = [i for i in filter_list if i]
        return filter_list

def get_filename():
    """
    Asks for the input filenames
    """
    filter_list = check_filterlist()

    file_names = [i for i in listdir() if ".agr" in i]
    file_names = [i for i in file_names if i[0] != "."]
    if len(file_names) == 1:
        file_name = file_names[0]
    else:
        for num,val in enumerate(file_names):
            print("{}: {}".format(num+1,val))

        valuechoice = input("Choose a file: \n")
        file_name = file_names[int(valuechoice)-1]
    return file_name, filter_list



def to_numeric_func(x):
    """
    Converts to pd.numeric, otherwise NaN
    """
    try:
        return pd.to_numeric(x)
    except ValueError as e:
        return np.nan


def node_corr(a):
    dic = {"s":0, "p":1, "d":2, "f":3,"g":4,"h":5}
    princ = int(re.search("\d+",a).group())
    ell = re.search("\D",a).group()
    return princ - dic[ell] - 1

def get_end(gr,k):
    """
    Get r value at which the wavefunction has settled and no longer oscillates
    """

    x = k[1]
    # Index 0 is value, index 1 is the gradient
    graddf = pd.DataFrame(np.array(np.array([x,gr]).T))
    graddf_redone = graddf[(np.abs(graddf[0]) > 1e-4) & (np.abs(graddf[1]) > 1e-3)]
    
    index = graddf_redone[0].index[-1]
    x_val = k[0][index]
    return x_val

def file_to_dataset(file_name):
    """
    Read the filename given and return a line by line dataset
    """
    with open(file_name,'r') as f:
        readall = f.read()

    readall = readall.replace("D","E")
    datasets = readall.split("\n\n")[:-1]
    first = datasets[0].split("\n") 
    datasets[0] = "\n".join(first[3:])
    return datasets

def datasets_to_numpy(datasets):
    """
    Transforms the datasets by using a combination of numpy and pandas
    """
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
    return datasets, orbitals

def remove_unused_datasets(datasets, orbitals, allowed_orbitals):
    """
    Removes entries to the datasets variable and orbitals which were not chosen by the user
    """
    new_datasets = []
    new_orbitals = []
    for i in range(len(datasets)):
        if orbitals[i] not in allowed_orbitals:
            continue
        new_datasets.append(datasets[i])
        new_orbitals.append(orbitals[i])

    return new_datasets, new_orbitals

def flip_combined_plots(datasets, orbitals):
    from scipy.interpolate import interp1d
    from skimage.metrics import mean_squared_error

    """
    If two plots have the same orbitals, but one is flipped, this function will flip the graph
    """

    D = defaultdict(list) # Gets the duplicates of orbitals
    for i, item in enumerate(orbitals):
        D[item].append(i)
    D = {k:v for k,v in D.items() if len(v)>1}

    for i in D:

        df_1 = datasets[D[i][0]]
        y1 = df_1[1]

        df_2 = datasets[D[i][1]]
        y2 = df_2[1]

        maxy1 = max(y1, key=abs)
        maxy2 = max(y2, key=abs)
        if maxy1 * maxy2 < 0:
            datasets[D[i][0]][1]  = - datasets[D[i][0]][1]

    return datasets


def node_print(datasets, orbitals):
    """
    Allows the user to print orbitals onto the screen
    """
    min_cutoff = 0.01 # x coordinate before which all nodes are ignored
    min_gradient = 1e-4 # Gradient at which nodes are ignored.
    for i in range(len(datasets)):

        df_i = datasets[i]
        z = np.where(np.diff(np.signbit(df_i[1])))[0] # Find where the wavefunction has crossed the x axis.

        z_vals = [df_i[0][j] for j in z] # Get the coordinates of these index points

        df_grad = np.gradient(df_i[1]) # Get the gradient function

        gr_vals = [abs(df_grad[j]) for j in z] # Get the gradient at where the wavefunction crosses the x axis.

        new_z_vals = []
        for vals in range(len(z_vals)):
            if z_vals[vals] < min_cutoff: # If the coordinates too small, then ignore
                continue
    #        elif z_vals[i] > 0.95 * df_i[0][-1]:
    #            continue
            elif gr_vals[vals] < min_gradient: # If the gradient is too small, then ignore
                continue

            new_z_vals.append(z_vals[vals]) # Since all criteria met, then node successfully measured

        correct_node = node_corr(orbitals[i])
        diff_from_correct = abs(correct_node - len(new_z_vals))
        print("{:4s}: {} nodes {} away from the correct node of {}".format(orbitals[i], len(new_z_vals), diff_from_correct, correct_node))

def plotmode(datasets, orbitals, plottogether, indexer = False, restrict_orbitals = []):
    """
    Allows the user to plot orbitals
    """
    end_list = []
    for i in range(len(datasets)):
        if orbitals[i] not in restrict_orbitals:
            continue

        df_i = datasets[i]
        df_grad = np.gradient(df_i[1])
        
        if indexer: # So if multiple files, one can see which orbital is from which file
            my_label = "{}: {}".format(indexer[i], orbitals[i])
        else:
            my_label = "{}".format(orbitals[i])
        end_list.append(get_end(df_grad,df_i)) # Append all of the final ends together
        plt.plot(df_i[0],df_i[1], label=my_label)
        plt.legend()
        if not plottogether:
            plt.xlim(0,end_list[-1]) # Use the most recent end value
            plt.show()


    if plottogether:
        plt.xlim(0,max(end_list)) # Use the largest end value
        plt.show()

#file_name, filter_list = get_filename()
##print(file_name)
n_cols = 3

class Wave:
    def __init__(self):
        return None


    def from_file(self):
        self.filename, self.filter_list = get_filename()
        self.datasets = file_to_dataset(self.filename)
        self.datasets, self.orbitals = datasets_to_numpy(self.datasets)
        self.allowed_orbitals = filter_atomic_orbitals(self.orbitals,self.filter_list) # Collects the nessicary datasets
        self.datasets, self.orbitals = remove_unused_datasets(self.datasets, self.orbitals, self.allowed_orbitals)
        self.indexer = False

    def flip(self):
        """
        If there are identical orbitals with identical plots but flipped, this function will match these plots
        """
        self.datasets = flip_combined_plots(self.datasets, self.orbitals)

    def printnodes(self):
        """
        Prints the number of nodes of each orbital, alongside the correct number of nodes
        This method is very sensitive and picks up very small oscillations GRASP usually would not
        """
        node_print(self.datasets, self.orbitals)

    def plot(self, plottogether=True, restrict_orb = []):
        """
        Plots the selected orbitals of the wavefunction
        plottogether - Boolean operator, either plots the orbitals together or seperately
        restrict_orb - Uses regex to restrict number of orbitals plotted
        """
        restrict_orbitals = filter_atomic_orbitals(self.orbitals, restrict_orb) # Collects the nessicary datasets
        plotmode(self.datasets, self.orbitals, plottogether, indexer = self.indexer, restrict_orbitals = restrict_orbitals)

    def __add__(self, wave2):
        """
        Allows one to add two different wavefunctions together
        """
        result = Wave()

        result.allowed_orbitals = self.allowed_orbitals + wave2.allowed_orbitals
        result.orbitals = self.orbitals + wave2.orbitals
        result.datasets = self.datasets + wave2.datasets
        result.indexer = [self.filename] * len(self.orbitals) + [wave2.filename] * len(wave2.orbitals)
        return result

lays = Wave()
lays.from_file()
dbsr = Wave()
dbsr.from_file()
both = lays + dbsr

#for i in dbsr.orbitals:
#    both.plot(restrict_orb =["{}".format(i)])

#datasets = file_to_dataset(file_name) # Uses the file_name to obtain the dataset
#datasets, orbitals = datasets_to_numpy(datasets) # Call datasets_to_numpy

#allowed_orbitals = filter_atomic_orbitals(orbitals,filter_list) # Collects the nessicary datasets
#
#if input("Enable node printing? (y/n)\n").lower() == "y":
#    node_print(datasets, allowed_orbitals, orbitals)
#
#if input("Enable Plot mode? (y/n)\n").lower() == "y":
#    plotmode(datasets, orbitals)
#
#
