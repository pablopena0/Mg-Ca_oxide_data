#!/bin/bash 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --time=45:50:00
#SBATCH --partition=p_fast
#SBATCH --mem=7520M
#SBATCH --hint=nomultithread
#SBATCH --workdir=.

input="MgO"
output="output"
files="MgO.in ../../pseudo-potentials/Mg.upf ../../pseudo-potentials/O.upf"
command="pw.x -ndiag 1 < MgO.in > MgO.out"

## Do not change below this line

. /home/users/slurm/etc/slurm_func.sh

HOST=$(hostname)
echo Job running on $HOST

chooseScr

LDIR=$(pwd)
export LDIR

echo "Copying files to $scr:"
echo "Files: ${files}"
cp ${files} $0 ${scr}/.

cd $scr

# LOAD NOW REQUIRED MODULES
module load QuantumESPRESSO/6.6-intel-2020a

# CALL EXECUTABLE with SRUN
echo "Running: /usr/bin/time -p srun $command"
eval /usr/bin/time -p srun $command

# List the contents of the scratch directory for debugging
echo "Contents of scratch directory after execution:"
ls -l $scr

recover

# List the contents of the working directory for debugging
echo "Contents of working directory after recovery:"
ls -l $LDIR

rm -r $scr
