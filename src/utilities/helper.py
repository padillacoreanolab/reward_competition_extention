#!/usr/bin/env python3
"""
"""
from collections import defaultdict
import numpy as np


def create_recursive_dict():
    """
    Creates a recursive dictionary using defaultdict.

    This function returns a defaultdict that defaults to itself. This allows for the creation of 
    dictionaries of arbitrary depth without having to manually check if a key exists before adding 
    to it.

    Returns:
    - defaultdict: A defaultdict that defaults to itself, allowing for the creation of dictionaries 
                   of arbitrary depth.
    """
    return defaultdict(create_recursive_dict)


def compute_sorted_index(group, value_column='Value', index_column='SortedIndex'):
    """ 
    Computes the index of each row's value within its sorted group.

    Parameters:
    - group (pd.DataFrame): A group of data.
    - value_column (str): Name of the column containing the values to be sorted.
    - index_column (str): Name of the new column that will contain the indices.

    Returns:
    - pd.DataFrame: The group with an additional column containing the indices.
    """
    sorted_values = sorted(list(set(group[value_column].tolist())))
    group[index_column] = group[value_column].apply(lambda x: sorted_values.index(x))
    return group


def find_nearest_index(sorted_list=None, target=0):
    """
    Returns the index of the number in the sorted list that is nearest to the target.

    This function performs a binary search on a sorted list to find the nearest number to 
    a given target. If the target exists in the list, its index is returned. If not, the 
    function will return the index of the number that's nearest to the target.

    Parameters:
    - sorted_list (list[int or float]): A sorted list of numbers.
    - target (int or float): The target number to find the nearest value to.

    Returns:
    - int: The index of the nearest number in the sorted list to the target. 
           If the sorted list is empty, returns None.

    Example:
    >>> sorted_nums = [1, 3, 5, 8, 10, 15, 18, 20, 24, 27, 30]
    >>> find_nearest_index(sorted_nums, 6)
    2

    Note:
    The list should be sorted in ascending order.
    """
    
    if sorted_list is None:
        return None
    if target <= sorted_list[0]:
        return 0
    if target >= sorted_list[-1]:
        return len(sorted_list) - 1

    # Binary search
    left, right = 0, len(sorted_list) - 1
    while left <= right:
        mid = (left + right) // 2

        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # After binary search, the target will be between sorted_list[right] and sorted_list[left]
    # We compare the two to see which one is closer to the target and return its index
    if abs(sorted_list[left] - target) < abs(sorted_list[right] - target):
        return left
    else:
        return right


def find_nearest_indices(array1, array2):
    """
    Finds the indices of the elements in array2 that are nearest to the elements in array1.

    This function flattens array1 and for each number in the flattened array, finds the index of the 
    number in array2 that is nearest to it. The indices are then reshaped to match the shape of array1.

    Parameters:
    - array1 (numpy.ndarray): The array to find the nearest numbers to.
    - array2 (numpy.ndarray): The array to find the nearest numbers in.

    Returns:
    - numpy.ndarray: An array of the same shape as array1, containing the indices of the nearest numbers 
                     in array2 to the numbers in array1.
    """
    array1_flat = array1.flatten()
    indices = np.array([np.abs(array2 - num).argmin() for num in array1_flat])
    return indices.reshape(array1.shape)


def main():
    """
    Main function that runs when the script is run
    """


if __name__ == '__main__': 
    main()
