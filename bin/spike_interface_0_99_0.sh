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

# Statistics
conda install -c conda-forge statsmodels --yes

# Hi-performance Pandas
conda install dask -c conda-forge --yes


conda install -c ejolly -c conda-forge -c defaults pymer4

# To get the Git repo root directory
conda install -c conda-forge gitpython --yes
