setupATLAS
lsetup "scikit 5.0.0-x86_64-centos7"

source myvenv/bin/activate

# YOU NEED TO RUN THIS IN BASH SHELL , ZSH DOES NOT WORK !!!!!!
source /cvmfs/sft.cern.ch/lcg/views/LCG_103swan/x86_64-centos7-gcc11-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/etc/hadoop-confext/hadoop-swan-setconf.sh analytix 3.2 spark3

