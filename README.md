# GraspTools
A collection of tools that can provide assistance for the program GRASP.

## Node counter and python plotter (nodecounter.py)

May count the total number of nodes of any octave output file in the current directory. Also supports plotting and manually specifying orbitals to plot and count using wildcards.

## Electronic configurations from rcsf.out (conf_from_rcsf.py)

Prints and outputs a list of configuration files from an rcsf.out file.
Each configuration list is sorted to ensure the same order of configurations will appear for slightly different CSF files for easy comparison.

## DF orbital optimisation assistant (orbital_reoptimisation.sh)

A bash script that automates much of the DF layer optimisation for you, with many functions such as nuclear charge decrease mode and creating screened hydrogenic functions to reestimate orbitals.

## Clist generator (clistgen.py)

Creates a clist.ref file from the rcsfmr.inp multireference file provided

## Configuration CSF counter (conf_collector.sh)

Uses the rcsfpreview program developed in https://github.com/Joseph-33/Grasp that will estimate the number of CSFs by generating CSFs but not saving them to file. Useful for rough estimates of extremely large expansions.

