#!/bin/bash 
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --time=45:50:00
#SBATCH --partition=p_fast
#SBATCH --mem=7520M
#SBATCH --hint=nomultithread
#SBATCH --workdir=.

input="MgO_deform_hydro_5"
output="output"
files="MgO_deform_hydro_5.in ../../../pseudo-potentials/Mg.upf ../../../pseudo-potentials/O.upf"
command="pw.x -ndiag 1 < MgO_deform_hydro_5.in > MgO_deform_hydro_5.out"


## Do not change below this line

. /home/users/slurm/etc/slurm_func.sh

HOST=$(hostname)
echo Job runing on $HOST

chooseScr

LDIR=$(pwd)
export LDIR

echo "cp ${files} to  $scr/."
cp  ${files} $0 ${scr}/.

cd $scr

# LOAD NOW REQUIERED MODULES
module load QuantumESPRESSO/6.6-intel-2020a

# CALL EXECUTABLE with SRUN
echo "Running: /usr/bin/time -p srun $command"
eval /usr/bin/time -p srun $command

rm -rf tmp/

recover
rm -r $scr
