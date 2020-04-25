# Purpose: Simple demonstration using Tika

import os
import tika

tika.initVM()

from tika import parser

root = input(r'Enter root directory:    ')
system = input(int('Operating system: (1) Linux, (2) Windows'))
if system == 1:
    divider = '/'
elif system == 2:
    divider = '\\'
else:
    print('Error: incorrect selection.')
    

for path, subdirs, files in os.walk(root):
    file_list = files
    break

for file in file_list:
    get_path = root + '/' + file
    parsed = parser.from_file(get_path)

    for key, value in parsed["metadata"].items():
        if value == '':
            continue
        else:
            print('{:32s}: {}'.format(key, value))

    # Enable the below to see the content of each file
    #print('Content:')
    #print(parsed["content"])

    input('\nPress enter to continue...')