#!/usr/bin/env python3

# this script is for renaming the files with simulated poissonian noise to a format similar to the FOCES name pattern

import os
import sys
import shutil

path_in = '/mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/IDtest/'

# make a list of all files in the input folder
fname_lst = sorted(os.listdir(path_in))
for fname in fname_lst:

    # if the file does not end with '.fits', skip it and continue with the next file in the list
    if fname[-5:] != '.fits':
        continue
    else:
        file_in = os.path.join(path_in, fname)

        if len(fname) == 54:
            id_num = fname[21:22]
        if len(fname) == 55:
            id_num = fname[21:23]
        else:
            print('Something is wrong with the file name length.')

        fname_out = '20201006_{:0>4}_{}_ods_fred.fits'.format(id_num, fname[17:20])
        file_out = os.path.join(path_in, fname_out)

        shutil.copy(file_in, file_out)
