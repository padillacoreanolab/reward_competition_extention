#!/usr/bin/env python3
"""
"""

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

def find_closest_index(sorted_list=None, target=0):
    """
    Returns the index of the number in the sorted list that is closest to the target.

    This function performs a binary search on a sorted list to find the closest number to 
    a given target. If the target exists in the list, its index is returned. If not, the 
    function will return the index of the number that's closest to the target.

    Parameters:
    - sorted_list (list[int or float]): A sorted list of numbers.
    - target (int or float): The target number to find the closest value to.

    Returns:
    - int: The index of the closest number in the sorted list to the target. 
           If the sorted list is empty, returns None.

    Example:
    >>> sorted_nums = [1, 3, 5, 8, 10, 15, 18, 20, 24, 27, 30]
    >>> find_closest_index(sorted_nums, 6)
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

def main():
    """
    Main function that runs when the script is run
    """

if __name__ == '__main__': 
    main()
