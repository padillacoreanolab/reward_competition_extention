#!/usr/bin/env python
# coding: utf-8

# In[1]:


# get_ipython().run_line_magic('matplotlib', 'inline')


# # Preprocessing and Spike Sorting Tutorial

# - In this introductory example, you will see how to use the :code:`spikeinterface` to perform a full electrophysiology analysis.
# - We will first create some simulated data, and we will then perform some pre-processing, run a couple of spike sorting algorithms, inspect and validate the results, export to Phy, and compare spike sorters.
# 

# In[2]:


import os
import pickle
import _pickle as cPickle
import glob
import warnings
import git
import imp


# In[3]:


from collections import defaultdict
import time
import json
from datetime import datetime


# In[4]:


import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import pandas as pd
import scipy.signal


# In[5]:


# Changing the figure size
from matplotlib.pyplot import figure
figure(figsize=(8, 6), dpi=80)


# The spikeinterface module by itself import only the spikeinterface.core submodule
# which is not useful for end user
# 
# 

# In[6]:


import spikeinterface


# We need to import one by one different submodules separately (preferred).
# There are 5 modules:
# 
# - :code:`extractors` : file IO
# - :code:`toolkit` : processing toolkit for pre-, post-processing, validation, and automatic curation
# - :code:`sorters` : Python wrappers of spike sorters
# - :code:`comparison` : comparison of spike sorting output
# - :code:`widgets` : visualization
# 
# 

# In[7]:


import spikeinterface as si  # import core only
import spikeinterface.extractors as se
import spikeinterface.sorters as ss
import spikeinterface.comparison as sc
import spikeinterface.widgets as sw
from spikeinterface.exporters import export_to_phy


# In[8]:


import spikeinterface.core


# In[9]:


from probeinterface import get_probe
from probeinterface.plotting import plot_probe, plot_probe_group
from probeinterface import write_prb, read_prb


# In[ ]:





# We can also import all submodules at once with this
#   this internally import core+extractors+toolkit+sorters+comparison+widgets+exporters
# 
# This is useful for notebooks but this is a more heavy import because internally many more dependency
# are imported (scipy/sklearn/networkx/matplotlib/h5py...)
# 
# 

# In[10]:


import spikeinterface.full as si


# In[11]:


# Increase size of plot in jupyter

plt.rcParams["figure.figsize"] = (10,6)


# - Getting the root directory of the Github Repo to base the files off of

# In[12]:


git_repo = git.Repo(".", search_parent_directories=True)
git_root = git_repo.git.rev_parse("--show-toplevel")


# In[13]:


git_root


# # Part 0: Loading in the Probe

# In[14]:


probe_filepath_glob = "data/*.prb"


# In[15]:


probe_absolultepath_glob = os.path.join(git_root, probe_filepath_glob)


# In[16]:


# Getting all the file paths of the recording parameter files(that happen to all end in `.prm`)
all_probe_files = glob.glob(probe_absolultepath_glob, recursive=True)


# In[17]:


all_probe_files


# - If you have more than one metadata file, then you must either:
#     - A. Put the index of the file in `all_parameter_files[0]` below. You would replace the `0` with the correct index. (Remember, Python is zero indexed so the first file in the list is 0. Second is 1, and so forth.
#     - B. Add a absolute or relative path to `open({./path/to/recording_file.rec})` below. You would replace `{./path/to/recording_file.rec}` with the path of the file for the metadata.

# In[18]:


if len(all_probe_files) < 1:
    warnings.warn("There are no parameter files in the directory that you specified. Please add a file, or correct the directory path")
else:
    probe_parameters = imp.load_source("probe_parameters", all_probe_files[0])
    with open(all_probe_files[0]) as info_file:
        lines = info_file.readlines()
        for line in lines:
            print(line)


# - Reading in the probe information into Spike interface and plotting the probe

# In[19]:


if len(all_probe_files) < 1:
    warnings.warn("There are no parameter files in the directory that you specified. Please add a file, or correct the directory path")
else:
    # Reading in the probe data
    probe_object = read_prb(all_probe_files[0])


# In[20]:


probe_object.to_dataframe()


# In[21]:


probe_object.get_global_contact_ids()


# In[22]:


probe_object.get_global_device_channel_indices()


# - Creating a dictionary of all the variables in the probe file

# In[23]:


if 'probe_parameters' in locals():
    probe_dict = defaultdict(dict)
    for attribute in dir(probe_parameters):
        # Removing built in attributes
        if not attribute.startswith("__"): 
            probe_dict[attribute] = getattr(probe_parameters, attribute)


# In[24]:


if "probe_dict" in locals():
    for key, value in probe_dict.items():
        print("{}: {}".format(key, value))


# In[ ]:





# # Part 1: Importing Data

# ## Loading in the Electrophysiology Recording

# - We are inputting the electrophsiology recording data with probe information. This should have been created in the prevous notebook in a directory created by Spike Interface. If you had already read in your own electrophsiology recording data with probe information with a different way, then follow these instructions.
#     - If you want to use a different directory, then you must either:
#         - Change `glob.glob({./path/to/with/*/recording_raw})` to the directory that you have the directories created from Spikeinterface. You can use a wildcard if you have multiple folders. You would replace `{./path/to/with/*/recording_raw}` with the path to either the parent directory or the actual directory containing the electrophsiology recording data read into Spikeinterface.
#         - Or change `(file_or_folder_or_dict={./path/to/recording_raw})`. You would replace `{./path/to/recording_raw}` with the path to either the parent directory or the actual directory containing the electrophsiology recording data read into Spikeinterface.

# In[25]:


all_recording_preprocessing_directories = glob.glob("./proc/*/*preprocessing*", recursive=True)


# In[26]:


all_recording_preprocessing_directories


# - If you have more than one recording directory, then you must either:
#     - A. Put the index of the file in `all_recording_directories[0]` below. You would replace the `0` with the correct index. (Remember, Python is zero indexed so the first file in the list is 0. Second is 1, and so forth.
#     - B. Add a absolute or relative path to `(file_or_folder_or_dict={./path/to/recording_file.rec}`) below. You would replace `{./path/to/recording_file.rec}` with the path of the file for the metadata.

# In[27]:


all_recording_preprocessing_directories[0]


# In[28]:


os.listdir(all_recording_preprocessing_directories[0])


# In[29]:


# To be used for all steps
recording_preprocessed = spikeinterface.core.load_extractor(file_or_folder_or_dict=all_recording_preprocessing_directories[1])


# In[30]:


type(recording_preprocessed)


# ## Metadata from the recording file

# - This is how you retrieve info from a :code:`RecordingExtractor`...
# 
# 

# In[31]:


channel_ids = recording_preprocessed.get_channel_ids()
fs = recording_preprocessed.get_sampling_frequency()
num_chan = recording_preprocessed.get_num_channels()
num_seg = recording_preprocessed.get_num_segments()
duration = recording_preprocessed.get_num_frames()

print('Channel ids:', channel_ids)
print('Sampling frequency:', fs)
print('Number of channels:', num_chan)
print('Number of segments:', num_seg)
print('Duration:', duration)
print('Number of hours:', duration/fs/3600)


# - Looking over the recording file

# In[32]:


sw.plot_timeseries(recording_preprocessed, time_range=(800,805), show_channel_ids=True)
plt.title("Timeseries for Traces for Preprocessed Recording")
plt.ylabel("Channels")


# In[33]:


channel_ids = ["13", "14", "15", "16", "21"]


# In[34]:


channel_ids = sorted(channel_ids, key=lambda x: float(x))


# In[35]:


sw.plot_timeseries(recording_preprocessed, channel_ids=channel_ids, show_channel_ids=True)
plt.title("Timeseries for Traces for Preprocessed Recording")
plt.ylabel("Channels")


# # Part 2: Sorting

# Now you are ready to spike sort using the :code:`sorters` module!
# Let's first check which sorters are implemented and which are installed
# 
# 

# In[36]:


print('Available sorters', ss.available_sorters())


# The :code:`ss.installed_sorters()` will list the sorters installed in the machine.
# We can see we have mountainsort4 and Tridesclous installed.
# Spike sorters come with a set of parameters that users can change.
# The available parameters are dictionaries and can be accessed with:
# 
# 

# In[37]:


sorter_name = 'mountainsort4'


# In[38]:


print(ss.get_default_sorter_params(sorter_name))


# Let's run a spike sorter and change one of the parameter, say, the detect_threshold:
# 
# 

# In[39]:


ss_params = ss.get_default_sorter_params(sorter_name).copy()


# - Changing the default parameters for these parameters
#     - These are the parameters changed in Maya's video

# In[40]:


# To only look for negative peaks
ss_params['detect_sign'] = 0
ss_params['detect_interval'] = 30
# So that each channel is sorted independently
ss_params['adjacency_radius'] = 700
# False because we have already filtered the recordings
ss_params['filter'] = False
ss_params['num_workers'] = 8
ss_params['whiten'] = False


# - Sorting usually takes at least a hour. Uncomment the code block below to run it. 

# In[41]:


all_sorter_methods = [sorter for sorter in dir(ss) if sorter_name in sorter and "run" in sorter]


# In[42]:


all_sorter_methods


# In[43]:


sorter_method_name = all_sorter_methods[0]


# In[44]:


sorter_method_name


# ## Creating a folder for Spike Sorting Output

# In[45]:


all_parent_recording_directories = glob.glob("./proc/*")


# In[46]:


all_parent_recording_directories


# In[ ]:





# In[ ]:


for preprocessing_directory in all_recording_preprocessing_directories:
    try:
        recording_preprocessed = spikeinterface.core.load_extractor(file_or_folder_or_dict=preprocessing_directory)
        recording_preprocessed = recording_preprocessed.set_probes(probe_object)
        recording_basename = os.path.basename(os.path.dirname(preprocessing_directory))
        
        parent_spikesorting_output_directory = os.path.dirname(preprocessing_directory)
        print("Output directory: {}".format(parent_spikesorting_output_directory))

        sorter_method_call = getattr(ss, sorter_method_name)
        child_spikesorting_output_directory = os.path.join(parent_spikesorting_output_directory,"ss_output")
        
        if not os.path.exists(child_spikesorting_output_directory):
            start = time.time()
            sorter_method_call(recording=recording_preprocessed,
                                          verbose=True,
                                           output_folder=child_spikesorting_output_directory ,
                                           **ss_params)
            print("Sorting finished in: ", time.time() - start)
        else:
            warnings.warn("""Directory already exists for: {}. 
            Either continue on if you are satisfied with the previous run 
            or delete the directory and run this cell again""".format(child_spikesorting_output_directory))
        spike_sorted_object = ss.read_sorter_folder(child_spikesorting_output_directory)
        sw.plot_rasters(spike_sorted_object)
        plt.title(recording_basename)
        plt.ylabel("Unit IDs")
        
        plt.savefig(os.path.join(parent_spikesorting_output_directory, "{}_raster_plot.png".format(recording_basename)))
        plt.close()
        
        waveform_output_directory = os.path.join(parent_spikesorting_output_directory, "waveforms")
        
        we_spike_sorted = si.extract_waveforms(recording=recording_preprocessed, 
                                       sorting=spike_sorted_object, folder=waveform_output_directory,
                                      ms_before=1, ms_after=1, progress_bar=True,
                                      n_jobs=8, total_memory="1G", overwrite=True,
                                       max_spikes_per_unit=2000)
        
        phy_output_directory = os.path.join(parent_spikesorting_output_directory, "phy")
        
        export_to_phy(we_spike_sorted, phy_output_directory,
              compute_pc_features=True, compute_amplitudes=True, remove_if_exists=False)
        
        
    except Exception as e: 
        print(e)


# In[ ]:


import os


# In[ ]:


for spike_output_dir in glob.glob("./proc/*/*/ss_output"):
    print(spike_output_dir)
    recording_basename = spike_output_dir.strip("/ss_output").strip("./proc/")
    spike_sorted_object = ss.read_sorter_folder(spike_output_dir)
    sw.plot_rasters(spike_sorted_object)
    plt.ylabel("Unit IDs")
    plt.title(recording_basename)
    raster_path = os.path.join(os.path.dirname(spike_output_dir), recording_basename + ".raster_plot.png")
    plt.savefig(raster_path)


# In[ ]:




