# Purpose: Visualise data about documents


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Files():
    def __init__(self, root):
        # Load data       
        # Filename register
        self.file_register = pd.read_csv(root + r'\pd_doc_register.csv')
        self.file_register.rename(columns={"Document No.": "File"}, inplace=True)
        self.file_register['File'] = self.file_register['File'].str.lower()
        self.file_register.set_index(['File'], inplace=True)
        del self.file_register['Unnamed: 0']
        # Metadata
        self.file_meta = pd.read_feather(root + r'\meta_data.feather')
        self.file_meta.set_index(['File'], inplace=True)                     # set index to unique identifier
        print('{} files scanned.'.format(len(self.file_meta)))
        # Files to transfer
        self.file_transfer = pd.read_csv(root + r'\files-names-matched.csv')
        self.file_transfer.set_index(['File'], inplace=True)                 # set index to unique identifier
        del self.file_transfer['Unnamed: 0']                                 # required when importing back in csv
        
        self.root = root


    def visualise(self, key, num_categories=10):
        """Visualise the string sent (which is the key)."""
        print('>>>>>>>>>>> Key to visualise:', key)

        # Plot file author numbers
        df = self.file_meta
        df[key].value_counts().head(num_categories).plot(kind='barh', align='center', figsize=(6.4*2, 4.8))
        print('>>>>>>>>>>> Describe:')
        print(df[key].describe())
        print('>>>>>>>>>>> Unique (first 100):')
        print(df[key].unique()[0:100])
        plt.title('Count of files by ' + key)
        plt.tight_layout()
        plt.show()

    
    def compile_file_keep(self):
        """Add metadata to files-names-matched.csv list."""
        # Add data from metadata gathered
        df = self.file_transfer.join(self.file_meta, how='left')
        # Drop 'Top-folder' column
        del df['Top-folder']

        # Count common files
        files_to_keep = self.file_transfer.index.tolist()
        files_in_register = self.file_register.index.tolist()
        count = 0
        for a_file in files_to_keep:
            if a_file in files_in_register:
                count += 1
        print('Of {} files to keep, {} of {} files in PD Doc register match.'.format(len(files_to_keep), count, len(files_in_register)))

        # Save to csv
        df.to_csv(self.root + r'\files_to_keep.csv')