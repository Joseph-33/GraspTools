# MCDFTools
A collection of tools that can provide assistance for the program GRASP2018 (https://doi.org/10.1016/j.cpc.2018.10.032) and other MCDHF-based programs, please cite if used.

## Getting Started

Simply run 
```
git clone https://github.com/Joseph-33/GraspTools
```
on your command line, or download as a zip.

## Requirements
 - Python (For Python scripts)
 - Bash, Unix Shell (For Bash scripts) 

## Node counter and python plotter (waveanalysis.py)

A python code which reads the .xmgrace files outputted by grasp. Can be used to count the number of nodes in each orbital, which a sensitivity much higher than standard GRASP. Crucial for the heavy and super-heavy elements.

Multiple .xmgrace files can be combined into one Wave() object due to the object-oriented programming nature of the program to plot and compare two different calculations easily using `wave3 = wave1 + wave2`.

Start the analysis with
```
python -i waveanalysis.py
mywave = Wave()
mywave.from_file()
```
and use `help(mywave)` to learn more about the functions. Due to the modular nature of the program, more functions can easily be added.

## Duplicate CSF remover (duplicate_remover.py)

This tool will remove all duplicate CSFs in rcsf.inp while preservering the previous order of the CSFs much faster than rcsfblock. Run rcsfblock afterwards to rebuild the blocks

## Electronic configurations from rcsf.out (conf_from_rcsf.py)

Prints and outputs a list of configuration from an rcsf.out file.
Each configuration list is sorted to ensure the same order of configurations will appear for slightly different CSF files for easy comparison.

## Rmix layers
Will remove all csfs from the file rcsf.inp where a subshell in the list orblayers is not present. (Optional combine the list rcsfrmix.out with rcsf.inp) output is rcsflastlay.out. Remember to run rcsfblock afterwards.

## DF orbital optimisation assistant (orbital_reoptimisation.sh)

A bash script that automates much of the DF GRASP orbital optimisation for you, with many functions such as nuclear charge decrease mode and creating screened hydrogenic functions to reestimate orbitals.

## Clist generator (clistgen.py)

Creates a clist.ref file using the ordering of the rcsfmr.inp multireference file provided

## Configuration CSF counter (conf_collector.sh)

Uses the rcsfpreview program developed in https://github.com/Joseph-33/Grasp that will estimate the number of CSFs by generating CSFs but not combining or saving them to file. Useful for rough estimates of extremely large expansions.

## Principle Quantum Number n=4 Generator (4n_gen.py)

This code will add core subshells to a rcsf.inp file

## RMCDHF Level Finder (level_finder.py)

This code will link the rmcdhf CSF number in the log output to an elcetronic configuration in your rcsf.inp file.

## RCSF Zero First Order (zero_first.py)

This program is a replacement of the program rcsfzerofirst included in the GRASP suite of tools. Details on the program and background theory can be found here: https://doi.org/10.3390/atoms11040068.
This code was written to address speed issues, resulting in a speed increase over 480 for large CSFs lists.


