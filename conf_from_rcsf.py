import numpy as np
import os.path
import re
import pdb
bp = breakpoint


infile = "rcsf.out"
outfile = "out.out"

def order(a):
    dic = {"s":0, "p":1, "d":2, "f":3,"g":4}
    a_separated = re.split("(\d+)",a)[1:]
    returned = int(a_separated[0]) * 10 + dic[a_separated[1]]
    return returned

def order_gen(a):
    nl = []
    for i in a:
        i = re.split("(\d+\D\(.*?\))", i)
        i = [j for j in i if j]
        i = sorted(i, key=lambda x:order(x.split('(')[0]))
        nl.append("".join(i))
    return nl


def mr_confs_gen(confs):
    with open("mr_confs","r") as fil:
        mr_vals = fil.readlines()

    mr_vals = [i.strip() for i in mr_vals]

    confs_list = list(confs)
    confs_list_ord = order_gen(confs_list)
    mr_vals_ord = order_gen(mr_vals)


    diffs = [x for x in confs_list_ord if x not in mr_vals_ord]
    return diffs

ans = input("Using '{}' as output file, change settings? (y/n) (Leave blank to continue)\n".format(outfile))
if ans.lower() == "y":
    numbers = input("Remove numbers from list?\n")
    if numbers.lower() == "y":
        numb = True
    else:
        numb = False
    outquestion = input("Should the filename be changed?\n")
    if outquestion.lower() == "y":
        outfile = input("What should the output name be?\n")
    else:
        outfile = ""
else:
    numb = ""

with open(infile,'r') as fil:
    lines = fil.readlines()

mr_confs = os.path.isfile("mr_confs")
if mr_confs:
    print("mr_confs file found")
else:
    print("mr_confs file not found")

nl = []
for i in lines[5:]:
    i=i.strip()
    if "*" in i:
        continue
    if "/" in i:
        continue
    i = i.replace("-"," ")
    nl.append(i)

sl = sorted(set(nl), key=lambda x: nl.index(x))
configurations = []
for i in range(len(sl)):
    sl[i] = sl[i].replace(" ","")
    sl[i] = re.split("(\d+\D\(\d+\))", sl[i])
    sl[i] = list(filter(None, sl[i])) # Remove empty values

    my_dict = {}
    for j in range(len(sl[i])):
        
        orbital = re.split("(\d+\D)\(\d+\)", sl[i][j])
        occupation = re.split("\d+\D\((\d+)\)", sl[i][j])
        occupation = list(filter(None, occupation))[0]
        orbital = list(filter(None, orbital))[0]
        my_dict[orbital] = my_dict.get(orbital, 0) + int(occupation)

    configuration_list = ["{}({})".format(orb, occ) for orb, occ in zip(my_dict.keys(), my_dict.values())]

    configurations.append("".join(configuration_list))
configurations = set(configurations)

configurations = sorted(configurations)
string_out = "\n".join(configurations)
print("All configurations:\n")
if numb:
    print(string_out)
else:
    for i in range(len(configurations)):
        print("{:3s} {}".format(str(i+1) + ":",configurations[i]))


if mr_confs:
    diff_list = mr_confs_gen(configurations)
    diff_list = sorted(diff_list)
    print("\nConfs not in mr list:\n")
    diffs = "\n".join(diff_list)
    if numb:
        print(diffs)
    else:
        for i in range(len(diff_list)):
            print("{:3s} {}".format(str(i+1) + ":",diff_list[i]))

    if outfile:
        with open(outfile,"w") as f:
            f.write(string_out)
            f.write("\n")


elif outfile:
    with open(outfile,"w") as f:
        f.write(string_out)
        f.write("\n")





