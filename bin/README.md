# Conda Environment Installation Commands

## Spike Interface Environment with Pip from Conda
```
# https://github.com/SpikeInterface/spikeinterface 
conda create -n spike_interface_0_97_1 python=3.9 --yes
conda activate spike_interface_0_97_1
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

# Installing Jupyter Notebook
conda install -c conda-forge notebook --yes

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

```

# Stellargraph Enviornment
conda create -n stellar_graph python=3.6 --yes
conda activate stellar_graph
conda install -c conda-forge jupyterlab --yes
conda install -c stellargraph stellargraph --yes



# SLEAP Environment
conda create -y -n sleap_1_3_0 -c sleap -c nvidia -c conda-forge sleap=1.3.0 

# Phy Environment
conda create -n phy2 -y cython dask h5py joblib matplotlib numpy pillow pip pyopengl pyqt pyqtwebengine pytest python qtconsole requests responses scikit-learn scipy traitlets -y

