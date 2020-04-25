# Purose: Find files based on filename.

import re

import numpy as np
import pandas as pd

def get_filenames(df, save_ouput_path):
    """Checks for files that match required filename format."""
    # Get list of files
    filenames = df['File'].tolist()
    files_matched = []
    files_project = []
    files_type = []
    
    # For format: Demo of files starting with three numbers
    p1 = re.compile(r"""
        [0-9]           # Starts with a number
        {3,3}           # Has three of above at start
        """, re.VERBOSE | re.IGNORECASE)

    # Search for the strings
    for file in filenames:
        if len(str(file)) > 16:          # don't consider long filenames
            continue                      
        m1 = p1.match(str(file))
        if m1:
            # Append filename
            files_matched.append(file.lower())

    # Return the list that matched and save to .csv
    df_out = pd.DataFrame({'File': files_matched, 'Project': files_project, 'File type': files_type})
    df_out.to_csv(save_ouput_path + r'\files-names-matched.csv')
    print('Saved data to \\files-names-matched.csv.')

    # Save list of unique doc types
    doc_types = list(set(files_type))
    df_out1 = pd.DataFrame({'Doc-types': doc_types})
    df_out1.to_csv(save_ouput_path + r'\doc-types.csv')

    # Print num (%) of files that matched
    percent = 100 * len(files_matched) / len(filenames)
    print('{:.1f} % ({} of {}) of filenames matched structure.'.format(percent, len(files_matched), len(filenames)))