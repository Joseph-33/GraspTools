##########################################################
#  This is the Principle Quantum Number n=4 Generator    #
#                                                        #
#  This code will add core subshells to a rcsf.inp file  #
#                                                        #
#  Input:                                                #
#           Input CSF File Name                          #
#                                                        #
#  Output:                                               #
#           Output CSF File Name                         #
#                                                        #
##########################################################




from os import listdir
import pdb
import re
bp = breakpoint

file_name = "rcsfmr_99_evvsml.inp"
out_name = "rcsfmr_99_4d4f_evvsml.inp"

replace_csf = r"  4d-( 4)  4d ( 6)  4f-( 6)  4f ( 8)" # List of the core subshells to include

print("Welcome to the core subshell generator.\nThis program will add full core subshells to your csf file.")
print("The current csf to be added are '{}'".format(replace_csf))
filans = input("The input and output files are:\nInput: {}\nOutput: {}\nWould you like to change them? (y/n)\n".format(file_name,out_name))
if filans.lower() == 'y':
    file_name = input("Type input name: \n")
    out_name = input("Type output name: \n")
print("Method 1 is using regex with {} and method 2 uses simple replace method, considered to be more reliable")
ans = input("Would you like option 1 or option 2?: \n")

if not ans.isdigit():
    print("Choose an integer")
    exit()
elif int(ans) == 1:
    opt = 1
    print("Option 1 selected")
elif int(ans) == 2:
    opt = 2
    print("Option 2 selected")
else:
    print("Choose either 1 or 2")
    exit()



pattern_csf = r"^(\s\s5s\s\()"
pattern_ang = r"^(\s\s\s)"
replace_ang = " " * len(replace_csf)
patterns = [pattern_csf, replace_csf, pattern_ang, replace_ang]

def file_selector():
    """ REDUNDANT. The file selector function. """
    file_names = [i for i in listdir()]
    file_names = [i for i in file_names if i[0] != "."]
    if len(file_names) == 1:
        file_name = file_names[0]
    else:
        for num,val in enumerate(file_names):
            print("{}: {}".format(num+1,val))

        valuechoice = input("Choose a file: \n")
        file_name = file_names[int(valuechoice)-1]
    return file_name


def option1(lines, patterns):
    """ Option1:
                This function uses regex to add the core subshells to the basis set"""
    pattern_csf, replace_csf, pattern_ang, replace_ang = patterns
    result = []
    for i in range(len(lines)):
        if i < 5:
            continue

        subs_csf = re.sub(pattern_csf, replace_csf + r"\1", lines[i])
        subs_ang = re.sub(pattern_ang, replace_ang + r"\1", subs_csf)

        result.append(subs_ang)
    return result

def option2(lines, patterns):
    """ Option2:
            This function uses str.replace to add the core subshells to the basis set"""
    pattern_csf, replace_csf, pattern_ang, replace_ang = patterns
    result=[]
    for i in range(len(lines)):
        if i < 5:
            continue

        if "(" in lines[i]: # For the CSF part
            subs = replace_csf + lines[i]
        elif "*" not in lines[i]: # For the angular part
            subs = replace_ang + lines[i]
        else:
            subs = lines[i]

        result.append(subs)

    return result


with open(file_name,'r') as fil:
    lines = fil.readlines()

if opt == 1:
    result = option1(lines, patterns)
elif opt == 2:
    result = option2(lines, patterns)
out_str = "".join(result)
csf_str = "".join(lines[:5])

with open(out_name,"w") as fil:
    fil.write(csf_str)
    fil.write(out_str)
