#!/usr/bin/env python3
"""Elo Rating Dataframe Helper Functions
"""
import re
from pyparsing import col

def get_all_animal_ids(animal_string):
    """
    Converts a string that contains the ID of animals, and only gets the IDs. 
    This usually removes extra characters that were added. (i.e. "1.1 v 2.2" to ("1.1", "2.2"))

    Args:
        animal_string(str): This is the first param.

    Returns:
        tuple: Of IDs of animals as strings
    """
    # Splitting by space so that we have a list of just the words
    all_words = animal_string.split()
    # Removing all words that are not numbers
    all_numbers = [num for num in all_words if re.match(r'^-?\d+(?:\.\d+)$', num)]
    return tuple(all_numbers)

def add_session_number_column(dataframe, indexes, session_number_column="session_number"):
    """
    Add a column to Pandas DataFrame that contains the session number. 
    This will only add session numbers to the rows specified by indexes. 
    You can fill in the empty cells with method: DataFrame.fillna(method='ffill')
    
    Args:
        dataframe(Pandas DataFrame): The DataFrame to add the session number column
        indexes(list): List of indexes for which rows to add the session numbers
        session_number_column(str): Name of the column to add
        
    Returns:
        Pandas DataFrame: DataFrame with the session numbers added
    """
    # Using a copy so that original is not changed
    copy_dataframe = dataframe.copy()
    session_number = 1
    for index in indexes:
        # Changing the session number one cell at a time where the index is
        copy_dataframe.at[index, session_number_column] = session_number
        session_number += 1
    return copy_dataframe
