#!/usr/bin/env python3

import pathlib
import sys

cores = int(sys.argv[1])

def func(st):   
    return "'" + str(st) + "'\n"

scr_path = pathlib.Path("script.sh").parent.resolve()
mpi_path = pathlib.Path("tmp_mpi").resolve()


str_path = func(scr_path) + func(mpi_path) * cores


with open("disks",'w') as f:
    f.write(str_path)


