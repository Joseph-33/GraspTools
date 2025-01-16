print("""
########################################################
#  Welcome to CLISTGEN generator!                      #
#                                                      # 
#  This file will generate a clist.ref file, based     #
#  upon your rcsfmr.inp file.                          #
#                                                      #
#  INPUTS:                                             #
#         rcsfmr.inp                                   #
#                                                      #
#  OUTPUTS:                                            #
#         clist.ref                                    #
#                                                      #
#                                                      #
########################################################
""")



import argparse
import pathlib

filename = "rcsfmr.inp"

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", default=filename, type=pathlib.Path)
parsed_args = parser.parse_args() # If argument, then use this as alternative to rcsfmr.inp

print("Installing to", parsed_args.filename.resolve())

fil = parsed_args.filename.resolve()



with open(fil,'r') as f:
    lines = f.readlines()


lsgen = lines[3].split()

with open("clist.ref",'w') as f: # Save to clist.ref
    for i in lsgen:
        f.write(i + "\n")


