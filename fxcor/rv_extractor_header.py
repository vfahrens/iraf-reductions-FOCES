import os
import astropy.io.fits as fits
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

###############################
# User definitions
path = 'output/ID2864/'
path_to_outfiles = 'output/ID2864/'
filename_fxcortxt = 'out_allRVs_200311.txt'
filename_all_single_orders = 'RVs_all_single_orders.txt'
filename_weighted = 'RVs_time_weighted.txt'
###############################

# check if the output directory exists, create if it does not
if not os.path.exists(path_to_outfiles):
    os.makedirs(path_to_outfiles)

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

    open_filepath = os.path.join(pathin, fname)
    with fits.open(open_filepath) as datei:
        header = datei[0].header
        if 'HJD' in header:
            date = header['HJD']
            rv_value = header['VHELIO']*1000.0
        phys_ord = fname[34:37]

    with open(fxcor_output, 'r') as fxfile:
        for line in fxfile:
            line = line.split()
            if fname in line and line[-1] != 'INDEF':
                rv_err = float(line[-1]) * 1000.0

    with open(out1_filepath, 'a') as outfile:
        if 'HJD' in header:
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
        v_err = []
        for line in infile:
            line = line.split()
            if line[0] == i:
                if int(line[3]) > 104 and int(line[3]) < 137 and int(line[3]) != 115:
                    vel_corroff = float(line[1]) - 5990.0
                    vels_onedate.append(vel_corroff)
                    vel_err = float(line[2])
                    v_err.append(vel_err)

        print(len(vels_onedate))
        if len(vels_onedate) > 0:
            vels_onedate_np = np.array(vels_onedate).astype(np.float)
            v_err_np = np.array(v_err).astype(np.float)
            rv_weightmean = np.average(vels_onedate_np, weights=(1/np.abs(v_err_np)))
            rv_std = np.std(vels_onedate_np) * np.sqrt(2) / np.sqrt(len(vels_onedate))

            if rv_std < 29.0:
                with open(out2_filepath, 'a') as out2file:
                    results = str(i) + ' ' + str(rv_weightmean) + ' ' + str(rv_std) + '\n'
                    out2file.write(results)
