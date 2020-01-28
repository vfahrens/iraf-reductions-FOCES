import os
import astropy.io.fits as fits
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

###############################
# User definitions
path = 'data/51Peg_lin/'
path_to_outfiles = 'output/51Peg_lin/'
filename_fxcortxt = 'out_all_200124.txt'
filename_all_single_orders = 'RVs_all_single_orders.txt'
filename_weighted = 'RVs_lin_weighted.txt'
###############################

location = Path(__file__).parent
pathin = (location / path).resolve()
pathout = (location / path_to_outfiles).resolve()
fxcor_output = os.path.join(path, filename_fxcortxt)
out1_filepath = os.path.join(pathout, filename_all_single_orders)
out2_filepath = os.path.join(pathout, filename_weighted)

#
# outname_lst = []
#
# with os.scandir(path) as it:
#     for entry in it:
#         # if the file name contains fxcor_result
#         if entry.name.rfind('_A_lin_IRAF.fits') != -1 and entry.is_file():
#             with open(path + entry.name) as file:
#                 with open(path + '{}_rv_allorders.txt'.format(entry.name[:13]), 'w') as outfile:
#                     print("test")



alldates = []


fname_lst = sorted(os.listdir(path))
prev_frameid = 0
for fname in fname_lst:
    if fname[-16:] != '_A_lin_IRAF.fits':
        continue
    #else:
        #print(fname)

    open_filepath = os.path.join(pathin, fname)
    with fits.open(open_filepath) as datei:
        header = datei[0].header
        date = header['HJD']
        rv_value = header['VHELIO']*1000.0
        phys_ord = fname[34:37]

    with open(fxcor_output, 'r') as fxfile:
        for line in fxfile:
            line = line.split()
            if fname in line:
                rv_err = floatline[-1] * 1000.0

    with open(out1_filepath, 'a') as outfile:
        output_singleorders = str(date) + ' ' + str(rv_value) + ' ' + str(rv_err) + ' ' + str(phys_ord) + '\n'
        print(output_singleorders)
        outfile.write(output_singleorders)

with open(out1_filepath, 'r') as infile:
    for line in infile:
        line = line.split()
        alldates.append(line[0])
dates_list = set(alldates)

for i in dates_list:
    with open(out1_filepath, 'r') as infile:
        vels_onedate = []
        for line in infile:
            line = line.split()
            if line[0] == i:
                if int(line[3]) > 104 and int(line[3]) < 137 and int(line[3]) != 115:
                    vel_corroff = float(line[1]) - 5990.0
                    vels_onedate.append(vel_corroff)

        print(len(vels_onedate))
        if len(vels_onedate) > 0:
            vels_onedate_np = np.array(vels_onedate).astype(np.float)
            rv_weightmean = np.average(vels_onedate_np)  #, weights=(1/np.abs(v_err)))
            rv_std = np.std(vels_onedate_np)

            if rv_std < 100.0:
                with open(out2_filepath, 'a') as out2file:
                    results = str(i) + ' ' + str(rv_weightmean) + ' ' + str(rv_std) + '\n'
                    out2file.write(results)

        vels_onedate = []
        vels_onedate_np = np.array(vels_onedate).astype(np.float)





