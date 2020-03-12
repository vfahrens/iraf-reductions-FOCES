import os
import astropy.io.fits as fits
from pathlib import Path
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt

###############################
# User definitions
path = 'output/ID2864_oldscatred/'
path_to_outfiles = 'output/ID2864_oldscatred/'
filename_fxcortxt = 'out_allRVs_200311_oldscatred.txt'
filename_all_single_orders = 'test_RVs_all_single_orders.txt'
filename_weighted = 'test_RVs_time_weighted.txt'
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


alldates = []

# # get the RVs and RVerrs from the image header and fxcor result file, respectively
# fname_lst = sorted(os.listdir(path))
# prev_frameid = 0
# for fname in fname_lst:
#     # only use the science fiber frames
#     if fname[-16:] != '_A_lin_IRAF.fits':
#         continue
#
#     # get the RV (converted to m/s) and the physical order number from the header
#     open_filepath = os.path.join(pathin, fname)
#     with fits.open(open_filepath) as datei:
#         header = datei[0].header
#         if 'HJD' in header:
#             date = header['HJD']
#             rv_value = header['VHELIO']*1000.0
#         phys_ord = fname[34:37]
#
#     # get the corresponding RV error (converted to m/s) from the fxcor result file
#     with open(fxcor_output, 'r') as fxfile:
#         for line in fxfile:
#             line = line.split()
#             if fname in line and line[-1] != 'INDEF':
#                 rv_err = float(line[-1]) * 1000.0
#
#     # save all the results for the single orders to a file
#     with open(out1_filepath, 'w') as outfile:
#         if 'HJD' in header:
#             output_singleorders = str(date) + ' ' + str(rv_value) + ' ' + str(rv_err) + ' ' + str(phys_ord) + '\n'
#             print(output_singleorders)
#             outfile.write(output_singleorders)

# read the list of observation dates from the file containing the single order RV results
with open(out1_filepath, 'r') as infile:
    for line in infile:
        line = line.split()
        alldates.append(line[0])
# remove any duplicates from the dates list
dates_list = set(alldates)

# read all RV results for a specific observation date (= 1 frame) from the single order file
RVs_eachdate = []
with open(out1_filepath, 'r') as infile:
    for line in infile:
        line = line.split()
        # only use physical orders 105-136 and not 115, because the rest is bad
        if 104 < int(line[3]) < 137 and int(line[3]) != 115:
            # save the whole line in a larger array with all observation dates
            RVs_eachdate.append(line)

# convert that array to a useful format for numpy
RVs_eachdate = np.transpose(RVs_eachdate)
RVs_eachdate = np.asarray(RVs_eachdate).astype(np.float)

# compute the median of all measured RVs and RV errors
med_RV = np.median(RVs_eachdate[1])
med_err = np.median(RVs_eachdate[2])
print(med_RV, med_err)
# for k in range(np.shape(RVs_eachdate)[1]):
#     if k % 150 == 0:
#         print(RVs_eachdate[:,k])
# print(len(vels_onedate))

# get the data for one specific observation date again and compute the weighted mean of the RV and the RV error
all_stds = []
with open(out2_filepath, 'w') as out2file:
    for date in set(RVs_eachdate[0]):
        vels_onedate = []
        v_err = []
        for j in range(len(RVs_eachdate[0])):
            # only use the rows of the array that contain RV data from one observation date
            if RVs_eachdate[0, j] == date:
                vels_onedate.append(RVs_eachdate[1, j])
                # if the RV error given by fxcor is zero, use the median RV error instead
                if RVs_eachdate[2, j] != 0.0:
                    v_err.append(RVs_eachdate[2, j])
                else:
                    v_err.append(med_err)
        # compute the weighted average for that date and use the median RV as zero-point correction
        rv_weightmean = np.average(vels_onedate, weights=(1/np.abs(v_err))) - med_RV
        # compute the RV error across the orders and put it in a list of RV errors
        rv_std = np.std(vels_onedate) * np.sqrt(2) / np.sqrt(len(vels_onedate))
        all_stds.append(rv_std)

        # write the results to a file, if the data point is good, which means that the error is below a certain limit
        if rv_std < 29.0:
            results = str(date) + ' ' + str(rv_weightmean) + ' ' + str(rv_std) + '\n'
            out2file.write(results)

# read the results from the file again to fix missing RV error values
RV_results = []
with open(out2_filepath, 'r') as in2file:
    for line2 in in2file:
        line2 = line2.split()
        # check if the cross-order RV error has a reasonable value, this is not the case e.g. for the template
        # a value of 0.1 m/s cross-order RV error is probably never possible with FOCES
        # replace bad RV errors with the median of all other RV errors
        if float(line2[2]) < 0.1:
            line2[2] = str(np.median(all_stds))
            RV_results.append(line2)
        else:
            RV_results.append(line2)

# save all RV results with the now corrected error to the file again
RV_results = np.transpose(RV_results)
with open(out2_filepath, 'w') as out2file_corr:
    for m in range(len(RV_results[0])):
        results_corr = str(RV_results[0,m]) + ' ' + str(RV_results[1,m]) + ' ' + str(RV_results[2,m]) + '\n'
        out2file_corr.write(results_corr)
# # I think I need to read in the whole file again and overwrite the old one after changing the value...
