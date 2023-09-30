import os

def read_key_value_file(file_name):
    """
    Reads a text file with key=value pairs on each line and returns a dictionary.

    Parameters:
    file_path (str): The path to the text file.

    Returns:
    dict: A dictionary with keys and values from the file.
    """
    # Get the current file's directory
    current_dir = os.path.dirname(__file__)

    # Construct the file path
    file_path = os.path.join(current_dir, file_name)

    # Create an empty dictionary to store key-value pairs
    data = {}

    # Open and read the file
    with open(file_path, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Split the line at the '=' character to get the key and value
            key, value = line.strip().split('=')
            # Add the key-value pair to the dictionary
            data[key] = value

    return data