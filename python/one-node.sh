#!/bin/sh
#SBATCH --job-name MC100k         # this is a parameter to help you sort your job when listing it
#SBATCH --ntasks 1                    # number of tasks in your job. One by default
#SBATCH --cpus-per-task 1             # number of cpus for each task. One by default
#SBATCH --partition public-cpu         # the partition to use. By default debug-cpu
#SBATCH --mem-per-cpu=2000             #in MB
#SBATCH --time 08:00:00                  # maximum run time.
 
module load foss/2019b ROOT Boost/1.71.0 Boost.Python/1.71.0 matplotlib/3.1.1-Python-3.7.4   # load a specific software using module, for example Python
 
srun python main.py -p 100000 --bound --plk1 --threeD --slice --settings settingsTemplate  # run your software 