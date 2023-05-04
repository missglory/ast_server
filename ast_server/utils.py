import os
import re

def find_files_with_regex(root_dir, regex):
    """
    Recursively finds files in a directory that match a regular expression.

    Args:
        root_dir (str): The root directory to start the search from.
        regex (str): The regular expression to match against file paths.

    Returns:
        A list of file paths that match the regular expression.
    """
    # Split the regular expression into path components
    path_components = regex.split('/')

    # Build a regular expression for the final path component
    final_regex = path_components.pop()

    # Build a regular expression for the intermediate path components
    intermediate_regex = ''
    for component in path_components:
        intermediate_regex += component + '[/\\\\]'

    # Compile the regular expressions
    intermediate_pattern = re.compile(intermediate_regex)
    final_pattern = re.compile(final_regex)

    # Recursively search for files
    matching_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if intermediate_pattern.search(dirpath):
            for filename in filenames:
                if final_pattern.match(filename):
                    matching_files.append(os.path.join(dirpath, filename))

    return matching_files


def find_files_with_name(root_dir, filename):
    """
    Recursively finds files in a directory with a specific filename.

    Args:
        root_dir (str): The root directory to start the search from.
        filename (str): The filename to search for.

    Returns:
        A list of file paths with the specified filename.
    """
    matching_files = []
    print(root_dir)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if file == filename:
                matching_files.append(os.path.join(dirpath, file))

    return matching_files
