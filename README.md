# MCeleM6


### General Info
***

MCeleM6 is a MonteCarlo tool developed to reproduce the dynamics of protein gradient formation in the C. elegans embryo.
In particular, it focuses on PLK-1 and MEX proteins.

## Requirements
***

* cmake: version > 3.1
* make
* gcc
* Python
* Matplotlib
* numpy
* scipy
* CERN ROOT
* Boost C++ libraries - including boost.python module

## System/Package versions tested on HPC UNIGE Cluster
***

* OS: Ubuntu18 - Fedora33
* Tool-chain: foss/2019b
* cmake: 3.17.4
* make: 4.2.1 
* gcc: 8.3.0
* Python: 3.7.4
* Matplotlib: 3.1.1
* numpy: 1.16.6
* scipy: 1.2.3
* CERN ROOT: 6.20.04 
* Boost C++ libraries - including boost.python module: 1.71
***
The software may run with other versions. Python2 is NOT supported.


## Installation
***
To install, please follow the instructions below:
- first loading the correct modules to build with
```
$ module load foss/2019b ROOT Boost/1.71.0 Boost.Python/1.71.0 matplotlib/3.1.1-Python-3.7.4 CMake

```
- Cloning and making the files
```
$ git clone https://github.com/Ratpenk40/MCeleM6.git

$ mkdir install
$ mkdir build
$ cd build
$ cmake ../
$ make
$ make install
$ cd ../install
```
Installation takes 1-2 minutes.

## Run instruction
***
To run the code, ! always inside a sbatch file, to avoid running on the login node
```
$ python main.py 
```
Several parameters are expected:
```
-p (--particles) <number> : number of particles to create
-b (--bound) : enable rebound at embryo's boundaries
--plk1 : enable plk1
--threeD : enable 3D 
--drawMovie : make GIF of protein dynamics
--settings <filename> : settings filename
-f (--slice) : enable slice
```
Example:
```
python main.py -p 1000000 --bound --plk1 --threeD --slice --settings settingsTemplate 
```
As a title of example a run as the example before (10^6 paricles for both MEXs and plk1) has a memory footprint of about 1000 MB.
A sbatch shell script, called 'one-node.sh' for running on the cluster is provided, see HPC doc for instruction on how to modify: https://doc.eresearch.unige.ch/hpc/slurm

## Output
***
The simulation output is saved in the ./logs/X directory where X is the date and time at the beginning of the run.
Several variables and information are reported, refer to the Supplementary material to know more.
In case several runs with same settings are launched (as for example, by using the runner.sh script), results can be summaryzed by using the analyze.py script, which produces mean and std dev over the runs.
```
python  analyze.py -f log_k_MEXp.txt -o MEXp.txt
```
where -f is the filename to parse and average over the runs, and -o is the output file to generate.
***
Average running time on normal desktop machine is of the order of few hours per run.

## Sample data
***
A sample output data is available in the logs directory, as well as a setting file ready to be used.
## Output data description
***
Conc_idY_XXX: 2D distribution of the protein XXX (Y component) as a function of time  (rows) and space along the embryo axis (columns) within the volume slice
log_k_XXX: extrapolated gradient value from the linear fit for the protein XXX
log_MEXp_ratio_slow_fast: ratio between slow and fast component for MEXp protein along the embryo axis as a function of time within the volume slice
log_profileAP_XXX: normalized particle concentration for protein XXX along the line ROI within the volume slice
log_v_XXX: average velocity for particle XXX along the embryo axis as a function of time within the volume slice
summary_parameter: summary of the input parameters used for the simulation run.
***
## Data analysis script provided
***
For averaging results over multiple runs launched with same input parameters, run, in the shell, in the logs package directory (or in output directory), the Python macro: analyzer.py:
```
python analyzer.py -f log_k_MEXp.txt -o MEXp.txt
```
this provides the output file (e.g.) MEXp.txt with a column for the average values and a column for standard deviations (STDEV) for each timeframe, of the parameters in the input files (e.g.) log_k_MEXp.txt
To analyze results that have a distribution in time ans space (2D matrices), run the Python macro analyzerConc.py, in the output folder
```
 python  analyzerConc.py -f log_v_plk1.txt -o v_plk1
```
this provides the output files (e.g.) v_plk1_MEAN.txt and (e.g.) v_plk1_STDDEV.txt (extensions ias added by the macro), respectively containing the matrix of the mean values and the STDEV over the runs of the values from the input files (e.g.) log_v_plk1.txt.
3D plots of the output files can be otained by running:
```
python plotter_3D_t_X.py -i v_plk1_MEAN.txt
```
this provides the distribution as a function of time and space of the parameter in the input file, along with the 2D distributions.

