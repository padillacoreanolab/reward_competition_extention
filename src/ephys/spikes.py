#!/usr/bin/env python3
"""
"""

import numpy as np


def calculate_rolling_avg_firing_rate(firing_times, window_size=2000, slide=2000, stop_time=None):
    """
    Calculates the rolling average firing rate of a neuron.

    Parameters:
    - firing_times (numpy.ndarray): An array of firing times of a neuron.
    - window_size (int or float): The size of the window for calculating the average firing rate.
    - slide (int or float): The amount to slide the window for each calculation.
    - stop_time (int or float, optional): The timestamp to stop the calculation at. If None, the calculation goes until the end of the firing times.

    Returns:
    - tuple: Two numpy.ndarrays, the rolling average firing rates and the starting timestamps of each window.
    """
    # Convert firing_times to a numpy array if it's not already
    firing_times = np.array(firing_times)

    # Initialize lists to store the results
    avg_firing_rates = []
    window_starts = []

    # If no stop_time is provided, use the last firing time
    if stop_time is None:
        stop_time = firing_times[-1]

    # Calculate the number of windows
    num_windows = int((stop_time - window_size) / slide) + 1

    # Loop over each window
    for i in range(num_windows):
        # Calculate the start and end of the window
        start = i * slide
        end = start + window_size

        # Calculate the average firing rate for this window
        firing_rate = np.sum((firing_times >= start) & (firing_times < end)) / window_size

        # Store the results
        avg_firing_rates.append(firing_rate)
        window_starts.append(start)

    return np.array(avg_firing_rates), np.array(window_starts)

def filter_outlier_timestamps(lfp_zscores, lfp_timestamps, event_timestamps, max_zscore=3):
    """
    Filter and return the indices of events based on LFP data that exceed a specified z-score threshold.

    This function identifies outlier data points in LFP traces based on their z-scores, 
    determines the corresponding event timestamps that these outliers fall into, and 
    returns the indices of these events, excluding any that precede the first event.

    Parameters:
    - lfp_zscores (numpy.array): Array of z-scores for LFP data points.
    - lfp_timestamps (numpy.array): Array of timestamps corresponding to the LFP data points.
    - event_timestamps (numpy.array): Array of timestamps marking specific events or intervals.
    - max_zscore (float): The z-score threshold used to classify data points as outliers. 
      Data points with a z-score magnitude greater or equal to this threshold are considered outliers.

    Returns:
    - numpy.array: An array of indices for the events that contain outlier LFP data points, 
      adjusted to ensure no indices precede the first event.
    """
    # Identify indices of LFP data points considered as outliers based on the z-score threshold
    outlier_indices = np.where(np.abs(lfp_zscores) >= max_zscore)[0]

    # Map the outlier LFP timestamps to their corresponding event timestamps
    outlier_timestamps = lfp_timestamps[outlier_indices]

    # Determine the event bin indices for each outlier timestamp
    event_bin_indices = np.digitize(outlier_timestamps, event_timestamps, right=True) - 1

    # Exclude outlier events occurring before the first event timestamp
    valid_event_indices = event_bin_indices[event_bin_indices >= 0]

    return valid_event_indices

def main():
    """
    Main function that runs when the script is run
    """


if __name__ == '__main__': 
    main()
