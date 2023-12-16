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

def main():
    """
    Main function that runs when the script is run
    """

if __name__ == '__main__': 
    main()
