from os import listdir
import pdb
import re
bp = breakpoint

file_name = "rcsfmr_even_99_5d5f_PeelEdited.inp"
out_name = "rcsfmr_out.inp"

def file_selector():
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

with open(file_name,'r') as fil:
    lines = fil.readlines()

pattern_csf = r"^(\s\s6s\s\()"
replace_csf = r"  5d-( 4)  5d ( 6)  5f-( 6)  5f ( 8)"

pattern_ang = r"^(\s\s\s)"
replace_ang = " " * len(replace_csf)

result = []
for i in range(len(lines)):
    if i < 5:
        continue

    subs_csf = re.sub(pattern_csf, replace_csf + r"\1", lines[i])
    subs_ang = re.sub(pattern_ang, replace_ang + r"\1", subs_csf)

#    if subs == lines[i]:
#        subs = " " * repl_len + subs

    result.append(subs_ang)

out_str = "".join(result)
csf_str = "".join(lines[:5])

with open(out_name,"w") as fil:
    fil.write(csf_str)
    fil.write(out_str)
