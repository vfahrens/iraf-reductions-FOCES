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
filename_all_single_orders = 'RVs_all_single_orders_oldscatred.txt'
filename_weighted = 'RVs_time_weighted_oldscatred.txt'
filename_weighted_tels = 'RVs_time_weighted_tels_oldscatred.txt'
filename_weighted_corrtels = 'RVs_time_weighted_corrtels_oldscatred.txt'
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
out3_filepath = os.path.join(pathout, filename_weighted_tels)
out4_filepath = os.path.join(pathout, filename_weighted_corrtels)


# # get the RVs and RVerrs from the image header and fxcor result file, respectively
# fname_lst = sorted(os.listdir(path))
# prev_frameid = 0
# with open(out1_filepath, 'w') as outfile:
#     for fname in fname_lst:
#         # only use the science fiber frames
#         if fname[-16:] != '_A_lin_IRAF.fits':
#             continue
#
#         # get the RV (converted to m/s) and the physical order number from the header
#         open_filepath = os.path.join(pathin, fname)
#         with fits.open(open_filepath) as datei:
#             header = datei[0].header
#             if 'HJD' in header:
#                 date = header['HJD']
#                 rv_value = header['VHELIO']*1000.0
#             phys_ord = fname[34:37]
#
#         # get the corresponding RV error (converted to m/s) from the fxcor result file
#         with open(fxcor_output, 'r') as fxfile:
#             for line in fxfile:
#                 line = line.split()
#                 if fname in line and line[-1] != 'INDEF':
#                     rv_err = float(line[-1]) * 1000.0
#
#         # save all the results for the single orders to a file
#         if 'HJD' in header:
#             output_singleorders = str(date) + ' ' + str(rv_value) + ' ' + str(rv_err) + ' ' + str(phys_ord) + '\n'
#             print(output_singleorders)
#             outfile.write(output_singleorders)
#
# # read the list of observation dates from the file containing the single order RV results
# alldates = []
# with open(out1_filepath, 'r') as infile:
#     for line in infile:
#         line = line.split()
#         alldates.append(line[0])
# # remove any duplicates from the dates list
# dates_list = set(alldates)
#
# # read all RV results for a specific observation date (= 1 frame) from the single order file
# RVs_fromfile = []
# tellurics_fromfile = []
# with open(out1_filepath, 'r') as infile:
#     for line in infile:
#         line = line.split()
#         # only use physical orders 105-136 and not 115, because the rest is bad
#         if 104 < int(line[3]) < 137 and int(line[3]) != 115:
#             # save the whole line in a larger array with all observation dates
#             RVs_fromfile.append(line)
#         if int(line[3]) == 75 or int(line[3]) == 83:
#             tellurics_fromfile.append(line)
#
# # sort all RV results by date and order
# RVs_eachdate = sorted(RVs_fromfile, key=itemgetter(0))
# tellurics_eachdate = sorted(tellurics_fromfile, key=itemgetter(0))
# # convert that array to a useful format for numpy
# RVs_eachdate = np.transpose(RVs_eachdate)
# RVs_eachdate = np.asarray(RVs_eachdate).astype(np.float)
# tellurics_eachdate = np.transpose(tellurics_eachdate)
# tellurics_eachdate = np.asarray(tellurics_eachdate).astype(np.float)
# # print(tellurics_eachdate)
#
# # compute the median of all measured RVs and RV errors
# med_RV = np.median(RVs_eachdate[1])
# med_err = np.median(RVs_eachdate[2])
# med_RV_tels = np.median(tellurics_eachdate[1])
# med_err_tels = np.median(tellurics_eachdate[2])
#
# # get the data for one specific observation date again and compute the weighted mean of the RV and the RV error
# all_stds = []
# with open(out2_filepath, 'w') as out2file:
#     for date in set(RVs_eachdate[0]):
#         vels_onedate = []
#         v_err = []
#         for j in range(len(RVs_eachdate[0])):
#             # only use the rows of the array that contain RV data from one observation date
#             if RVs_eachdate[0, j] == date:
#                 vels_onedate.append(RVs_eachdate[1, j])
#                 # if the RV error given by fxcor is zero, use the median RV error instead
#                 if RVs_eachdate[2, j] != 0.0:
#                     v_err.append(RVs_eachdate[2, j])
#                 else:
#                     v_err.append(med_err)
#         # compute the weighted average for that date and use the median RV as zero-point correction
#         rv_weightmean = np.average(vels_onedate, weights=(1/np.abs(v_err))) - med_RV
#         # compute the RV error across the orders and put it in a list of RV errors
#         rv_std = np.std(vels_onedate) * np.sqrt(2) / np.sqrt(len(vels_onedate))
#         all_stds.append(rv_std)
#
#         # write the results to a file, if the data point is good, which means that the error is below a certain limit
#         if rv_std < 29.0:
#             results = str(date) + ' ' + str(rv_weightmean) + ' ' + str(rv_std) + '\n'
#             out2file.write(results)
#
# # read the results from the file again to fix missing RV error values
# RV_results = []
# with open(out2_filepath, 'r') as in2file:
#     for line2 in in2file:
#         line2 = line2.split()
#         # check if the cross-order RV error has a reasonable value, this is not the case e.g. for the template
#         # a value of 0.1 m/s cross-order RV error is probably never possible with FOCES
#         # replace bad RV errors with the median of all other RV errors
#         if float(line2[2]) < 0.1:
#             line2[2] = str(np.median(all_stds))
#             RV_results.append(line2)
#         else:
#             RV_results.append(line2)
#
# RV_tofile = sorted(RV_results, key=itemgetter(0))
# # save all RV results with the now corrected error to the file again
# RV_tofile = np.transpose(RV_tofile)
# with open(out2_filepath, 'w') as out2file_corr:
#     for m in range(len(RV_tofile[0])):
#         results_corr = str(RV_tofile[0, m]) + ' ' + str(RV_tofile[1, m]) + ' ' + str(RV_tofile[2, m]) + '\n'
#         out2file_corr.write(results_corr)
#
#
# # get the telluric line RVs for one specific observation date and compute the weighted mean of the RV and the RV error
# all_stds_tels = []
# with open(out3_filepath, 'w') as out3file:
#     for date in set(tellurics_eachdate[0]):
#         vels_onedate_tels = []
#         v_err_tels = []
#         for j in range(len(tellurics_eachdate[0])):
#             # only use the rows of the array that contain RV data from one observation date
#             if tellurics_eachdate[0, j] == date:
#                 vels_onedate_tels.append(tellurics_eachdate[1, j])
#                 # if the RV error given by fxcor is zero, use the median RV error instead
#                 if tellurics_eachdate[2, j] != 0.0:
#                     v_err_tels.append(tellurics_eachdate[2, j])
#                 else:
#                     v_err_tels.append(med_err_tels)
#         # compute the weighted average for that date and use the median RV as zero-point correction
#         rv_weightmean_tels = np.average(vels_onedate_tels, weights=(1/np.abs(v_err_tels))) - med_RV_tels
#         # compute the RV error across the orders and put it in a list of RV errors
#         rv_std_tels = np.std(vels_onedate_tels) * np.sqrt(2) / np.sqrt(len(vels_onedate_tels))
#         all_stds_tels.append(rv_std_tels)
#
#         # write the results to a file, if the data point is good, which means that the error is below a certain limit
#         if rv_std_tels < 150.0:
#             results = str(date) + ' ' + str(rv_weightmean_tels) + ' ' + str(rv_std_tels) + '\n'
#             out3file.write(results)
#
# # read the results from the file again to fix missing RV error values
# RV_results_tels = []
# with open(out3_filepath, 'r') as in3file:
#     for line2 in in3file:
#         line2 = line2.split()
#         # check if the cross-order RV error has a reasonable value, this is not the case e.g. for the template
#         # a value of 0.1 m/s cross-order RV error is probably never possible with FOCES
#         # replace bad RV errors with the median of all other RV errors
#         if float(line2[2]) < 0.1:
#             line2[2] = str(np.median(all_stds_tels))
#             RV_results_tels.append(line2)
#         else:
#             RV_results_tels.append(line2)
#
# RV_tofile_tels = sorted(RV_results_tels, key=itemgetter(0))
# # save all RV results with the now corrected error to the file again
# RV_tofile_tels = np.transpose(RV_tofile_tels)
# with open(out3_filepath, 'w') as out3file_corr:
#     for m in range(len(RV_tofile_tels[0])):
#         results_corr = str(RV_tofile_tels[0, m]) + ' ' + str(RV_tofile_tels[1, m]) + ' ' + str(RV_tofile_tels[2, m]) + '\n'
#         out3file_corr.write(results_corr)
#
# # save the RV results corrected with the telluric shift to a file
# with open(out4_filepath, 'w') as out4file_corr:
#     for m in range(len(RV_tofile_tels[0])):
#         results_corr = str(RV_tofile_tels[0, m]) + ' ' + str(np.float(RV_tofile[1, m]) - np.float(RV_tofile_tels[1, m])) + ' ' + str(RV_tofile_tels[2, m]) + '\n'
#         out4file_corr.write(results_corr)
