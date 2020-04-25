import time

import pandas as pd

from file_cleanup import get_meta, filename_match, visualise_doc

########################
# Program controls & Steps
########################

root = input(r'Enter root directory:    ')
root = root.strip('"')
run_steps = [0, 1, 2]        # runs these steps below, separate by comma


# 1. Get metadata from walk.root
if 1 in run_steps:
    start2 = time.time()
    num = get_meta.get_data(root)
    end2 = time.time()
    print('Step 1 complete. Metadata from {} files took {:.1f} sec.'.format(num, end2 - start2))

# 2. From walk.root files, get list of filenames that match requirement
if 2 in run_steps:
    file_meta = pd.read_feather(root + r'/meta_data.feather')
    filename_match.get_filenames(file_meta, root)
    print('Step 2 complete.')

# 3. Visualise & operate on data
if 3 in run_steps:
    # Create instance of class
    GlobalFolder = visualise_doc.Files(root)

    # Visualise
    #GlobalFolder.visualise('Title')
    #GlobalFolder.visualise('Author')

    # Operate on data
    GlobalFolder.compile_file_keep()
    print('Step 3 complete.')