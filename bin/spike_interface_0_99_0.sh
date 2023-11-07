conda create -n spike_interface_0_99_0 python=3.10 --yes
conda activate spike_interface_0_99_0
conda install -c conda-forge jupyterlab --yes

# https://pypi.org/project/spikeinterface/0.99.0/
# Ephys processing tools
pip install spikeinterface[full,widgets]==0.99.0
conda install -c conda-forge openpyxl --yes

# For better quality plots
conda install seaborn -c conda-forge --yes
# For power calculations
conda install -c edeno spectral_connectivity --yes
# For using the GPU
conda install -c conda-forge cupy --yes

# Spike-LFP Coupling
conda install astropy --yes

################## OLD CODE BELOW ################################
# Pandas
conda install -c conda-forge pandas

# Installing Spikeinterface
pip install spikeinterface[full,widgets]==0.97.1
# Installing Spike sorters
# pip install mountainsort4
pip install --upgrade mountainsort5
# Installing Spectral Connectivty
conda install -c edeno spectral_connectivity --yes

# Installing Medpc library
pip install medpc2excel
conda install -c anaconda openpyxl -y

# Installing Git Library to get root directory of repo
conda install -c conda-forge gitpython
# To use GPU for spectral connectivity
# NOTE: Change Cuda version based on your local Cuda
conda install -c conda-forge cupy cudatoolkit=11.0

# To label inlines and other plots
pip install matplotlib-label-lines
conda install -c conda-forge seaborn -y

# To look at videos
# NOTE: This may take a long time to install
# NOTE: Not installed on spike_interface_0_97_1 because it was taking forever
# conda install -c conda-forge opencv
conda install -c conda-forge moviepy -y

# Refactoring
conda install flake8 -y
pip install jupyterlab_flake8

# GPFA
conda install -c conda-forge tqdm --yes
pip install elephant

# For Grainger Causality
conda install -c anaconda statsmodels --yes

# For checking if phase locking values have uniform distribution
conda install astropy

# For graphical neural networks
conda install -c pytorch pytorch --yes
conda install -c stellargraph stellargraph --yes
conda install -c conda-forge tensorflow --yes
conda install -c conda-forge tensorflow=2.13.1
conda install -c anaconda chardet --yes
