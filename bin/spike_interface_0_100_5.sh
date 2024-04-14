# Turning on Conda
module load conda

# Creating a new environment
mamba create -p ./spike_interface_0_100_5 python=3.10 --yes
# Turning on created environment
conda activate ./spike_interface_0_100_5

# Installing the necessary packages

### To use GPU
mamba install cudatoolkit=11.3 pytorch=1.12.1=gpu_cuda* -c pytorch --yes

### To use Jupyterlab
mamba install jupyterlab -c conda-forge --yes

### To use spikeinterface
pip install spikeinterface[full,widgets]==0.100.5
pip install --upgrade mountainsort5==0.5.6

### To calculate spectral metrics
mamba install -c edeno spectral_connectivity --yes

### To calculate power with CWT
pip install fCWT==0.1.18

### To make statistical models
mamba install -c conda-forge statsmodels --yes

### To calculate Spike-LFP Coupling
mamba install -c conda-forge astropy --yes

### To do GPU calculations with Numpy
mamba install -c conda-forge cupy --yes

### For better quality plots
mamba install seaborn -c conda-forge --yes

### To get the Git repo root directory
mamba install -c conda-forge gitpython --yes

### To read and write Excel files
mamba install -c conda-forge openpyxl --yes

