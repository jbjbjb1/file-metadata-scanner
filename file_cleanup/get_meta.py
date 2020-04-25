# Purpose: Get data about documents, save in feather (for fast read/write for much data)

import csv
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import tika
tika.initVM()
from tika import parser


def file_action(path, file, top_folder, file_meta_data):
    """Action for each file in os.walk."""
    # Save metadata of files provided by tika
    parsed = parser.from_file(path + '/' + file)
    try:
        # Conditions for file
        file = file.lower()
        # Conditions for 'Author'
        if type(parsed["metadata"]['Author']) == list:
            author = ', '.join( parsed["metadata"]['Author'][:3] )         # just join first 3 authors
            author = author.title()
        else:
            author = parsed["metadata"]['Author']
            author = author.title()
        # Conditions for 'meta:creation-date'
        if type(parsed["metadata"]['meta:creation-date']) == list:
            creationdate = parsed["metadata"]['meta:creation-date'][0]      # only take the first date'
        else:
            creationdate = parsed["metadata"]['meta:creation-date']
        # Conditions for 'dc:title'
        if type(parsed["metadata"]['dc:title']) == list:
            title = ', '.join( parsed["metadata"]['dc:title'] )
            title = title.title()
        else:
            title = parsed["metadata"]['dc:title']
            title = str(title.title())
            
        # Save to dictionary
        parsed_structure = {'Author': author, 'Top-folder': top_folder, 'Creation-date': creationdate, 'Path': path, 'File': file, 'Title':title}
    
    except (KeyError, TypeError):
        """KeyError; does not have this key, TypeError; no metadata."""
        parsed_structure = {'Author': '', 'Top-folder': top_folder, 'Creation-date': '', 'Path': path, 'File': file, 'Title':''}
    file_meta_data.append(parsed_structure)
    
    return file_meta_data

def get_data(root):
    """Get list of all directories and corresponding sub-directories."""

    file_meta_data = []     # For tika file metadata
    for path, subdirs, files in os.walk(root):
        for file in files:
            top_folder = ''
            file_meta_data = file_action(path, file, top_folder, file_meta_data)
           
    
    # Convert to dataframe
    df = pd.DataFrame(file_meta_data)

    # Save data
    df.to_feather(root + r'/meta_data.feather')
    df.to_csv(root + r'/meta_data.csv')

    return len(df)