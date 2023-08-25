import argparse
import pathlib

filename = "rcsfmr.inp"

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", default=filename, type=pathlib.Path)
parsed_args = parser.parse_args()

print("Installing to", parsed_args.filename.resolve())

fil = parsed_args.filename.resolve()



with open(fil,'r') as f:
    lines = f.readlines()


lsgen = lines[3].split()

with open("clist.ref",'w') as f:
    for i in lsgen:
        f.write(i + "\n")


