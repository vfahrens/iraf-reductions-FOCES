import os
import numpy as np
import matplotlib.pyplot as plt

###############################
# User definitions
path = "51Peg_lin/"
###############################

outname_lst = []

with os.scandir(path) as it:
    for entry in it:
        # if the file name contains fxcor_result
        if entry.name.rfind('_A_lin_IRAF.fits') != -1 and entry.is_file():
            with open(path + entry.name) as file:
                with open(path + '{}_rv_allorders.txt'.format(entry.name[:13]), 'w') as outfile:
                    print("test")



fname_lst = sorted(os.listdir(path))
prev_frameid = 0
for fname in fname_lst:
    if fname[-5:] != '_A_lin_IRAF.fits':
        continue
    else:
        print(fname)

    with fits.open((path / fname).resolve()) as datei:
        headyyy = datei[0].header