import os
import datetime as dt
import shutil
import astropy.io.fits as fits
import numpy as np
from operator import itemgetter
import julian
import matplotlib.pyplot as plt

# import statements for other python scripts
import paths_and_files as pf


# distinguish between logfile and comment file paths, filenames and years
def get_category():
    now = dt.datetime.now()
    # create a list with all years from when FOCES data exist
    years_log = list(range(2016, now.year + 1))
    years_comm = list(range(2018, now.year + 1))

    dif_files = ['log', 'comments']
    years_list = []
    directory = []
    file1 = []
    for cat in dif_files:
        # check whether to use the log or comments year list
        if cat == 'log':
            years_list.append(years_log)
            directory.append('log')
            file1.append('logfile')
        if cat == 'comments':
            years_list.append(years_comm)
            directory.append('comments')
            file1.append('comments')

    return years_list, directory, file1


# extract all nights with observation data for a specific redmine project and write the dates to a file
def get_obsnights(redmine_id):
    dates_for_red = []
    # extract all observation night dates for this project
    with open(pf.grep_redID_out.format(redmine_id), 'r') as grepfile:
        with open(pf.out_gamse_sorted.format(redmine_id), 'w') as datefile:
            for line in grepfile:
                # remove whitespaces in the beginning and end of the string
                line = line.strip()
                # remove whitespaces inside the string
                line = line.replace(' ', '')
                # split the string into its single entries
                line = line.split('|')
                if line[0][0] != '#':
                    # extract the individual observation dates from the grep results
                    file_time = dt.datetime.strptime(line[0][4:18], '%Y%m%d%H%M%S')
                    folder_date = dt.datetime.strftime(file_time, '%Y%m%d')
                    day_before = file_time - dt.timedelta(days=1)
                    str_day_before = dt.datetime.strftime(day_before, '%Y%m%d')
                    if file_time.hour > 12 and folder_date not in dates_for_red:
                        dates_for_red.append(folder_date)
                        datefile.write(folder_date + '\n')
                    elif file_time.hour <= 12 and str_day_before not in dates_for_red:
                        dates_for_red.append(str_day_before)
                        datefile.write(str_day_before + '\n')
    return


# read the dates that should be used in GAMSE from a file
def get_reductiondates(redmine_id):
    red_dates = []
    for line in open(pf.out_gamse_copy.format(redmine_id), 'r'):
        line = line.strip()
        red_dates.append(line)
    return red_dates


# automatically copy the (sorted) wavelength calibrated data to the IRAF folder
def script_copy_reduced_data(redmine_id):
    total_files_copied = 0
    # check if a folder with this redmine ID exists already in IRAF data input
    if not os.path.exists(pf.iraf_data_folder.format(redmine_id)):
        os.makedirs(pf.iraf_data_folder.format(redmine_id))

    with open(pf.frames_list.format(redmine_id), 'w') as framelist:
        # read the results from the grep command
        with open(pf.grep_redID_out.format(redmine_id), 'r') as grepfile:
            for line in grepfile:
                filename_used = []
                # remove whitespaces in the beginning and end of the string
                line = line.strip()
                # remove whitespaces inside the string
                line = line.replace(' ', '')
                # split the string into its single entries
                line = line.split('|')
                if line[0][0] != '#':
                    # extract the name of each file from the grep results
                    file_name = line[0]
                    filename_used.append(file_name)
                    file_time = dt.datetime.strptime(line[0][4:18], '%Y%m%d%H%M%S')

                    # get the correct date for the night of observation
                    folder_date = dt.datetime.strftime(file_time, '%Y%m%d')
                    if file_time.hour <= 12:
                        day_before = file_time - dt.timedelta(days=1)
                        str_day_before = dt.datetime.strftime(day_before, '%Y%m%d')
                        folder_date = str_day_before
                    # get the path of the .tab file corresponding to the .fits file
                    data_folder_path = os.path.join(pf.abs_path_data, folder_date)
                    tab_file_path = os.path.join(data_folder_path, file_name + '.tab')

                    # from the .tab file extract the correct link name of the raw frame
                    with open(tab_file_path, 'r') as tabfile:
                        for linex in tabfile:
                            if 'LINKNAME' in linex:
                                linex = linex.strip()
                                linex = linex.split('=')
                                raw_name = linex[1]
                                filename_used.append(raw_name)

                    # generate the file name for the reduced frame and copy it
                    red_name = raw_name[:-5] + '_ods.fits'
                    result_file_path = os.path.join(pf.gamse_results_folder.format(folder_date), red_name)
                    shutil.copy(result_file_path, pf.iraf_data_folder.format(redmine_id))
                    total_files_copied += 1
                    framelist.write(str(filename_used[0]) + ' ' + str(filename_used[1]) + '\n')
        print('Successfully copied {} files!'.format(total_files_copied))

    return


# get the RVs (VHELIO, VREL) and RVerrs from the image header and fxcor result file
def get_rvs(redmine_id, fxcor_outname):
    fname_lst = sorted(os.listdir(pf.iraf_output_folder.format(redmine_id)))

    with open(pf.out_RVs_single.format(redmine_id), 'w') as outfile:
        for fname in fname_lst:
            # only use the science fiber frames
            if fname[-16:] != '_A_lin_IRAF.fits':
                continue

            # get the RV (converted to m/s) and the physical order number from the header
            open_filepath = os.path.join(pf.iraf_output_folder.format(redmine_id), fname)
            with fits.open(open_filepath) as datei:
                header = datei[0].header
                if 'VHELIO' in header:
                    date_str = header['UTMID']
                    if len(date_str) == 19:
                        date_dt = dt.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                    elif len(date_str) > 19:
                        date_dt = dt.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
                    else:
                        print('Warning: Date {} has unexpected format.'.format(date_str))
                    date = julian.to_jd(date_dt, fmt='jd')
                    rv_value = header['VHELIO'] * 1000.0
                phys_ord = fname[34:37]

            # get the corresponding RV error (converted to m/s) and VREL from the fxcor result file
            fxcor_output = os.path.join(pf.iraf_output_folder.format(redmine_id), fxcor_outname + '.txt')
            with open(fxcor_output, 'r') as fxfile:
                for line in fxfile:
                    line = line.split()
                    if fname in line and line[-1] != 'INDEF':
                        rv_err = float(line[-1]) * 1000.0
                        rv_rel = float(line[-3]) * 1000.0

            # save all the results for the single orders to a file
            if 'HJD' in header:
                output_singleorders = str(date) + ' ' + str(rv_value) + ' ' + str(rv_err) + ' ' + \
                                      str(rv_rel) + ' ' + str(phys_ord) + '\n'
                # print(output_singleorders)
                outfile.write(output_singleorders)

    return


# get the radial velocities as object and telluric velocities
def split_rvs_tel(redmine_id):
    # read all RV results for a specific observation date (= 1 frame) from the single order file
    bad_orders = []
    rvs_fromfile = []
    tellurics_fromfile = []

    with open(pf.input_tel_orders, 'r') as telluric_file:
        for linet in telluric_file:
            linet = linet.strip()
            bad_orders.append(int(linet))
    # order_limits = input('Please give the range of orders where you want RVs extracted: (e.g.: 105-136) ')
    # order_limits = order_limits.strip()
    # order_limits = order_limits.split('-')
    with open(pf.out_RVs_single.format(redmine_id), 'r') as infile:
        for line in infile:
            line = line.split()
            # only use physical orders between the given limits and not 115, because that is bad
            # if int(line[-1]) in range(int(order_limits[0]), int(order_limits[1]) + 1) and int(line[-1]) != 115:
            if int(line[-1]) not in bad_orders:
                # save the whole line in a larger array with all observation dates
                rvs_fromfile.append(line)
            if int(line[-1]) == 69 or int(line[-1]) == 70 or int(line[-1]) == 75 or int(line[-1]) == 83:
                tellurics_fromfile.append(line)

    rvs_single_array = make_rv_array(rvs_fromfile)
    tels_single_array = make_rv_array(tellurics_fromfile)
    return rvs_single_array, tels_single_array


# sort, transpose and format RVs for further use
def make_rv_array(rv_list):
    # sort all RV results by date and order
    rvs_eachdate = sorted(rv_list, key=itemgetter(0))
    # convert that array to a useful format for numpy
    rvs_eachdate = np.transpose(rvs_eachdate)
    rvs_eachdate = np.asarray(rvs_eachdate).astype(np.float)
    return rvs_eachdate


# compute the median of the measured single-order RVs and RV errors
def rv_and_err_median(rvs_array, rv_type):
    # for normal RVs, use RV with heliocentric correction
    if rv_type != 'tel':
        med_rv = np.median(rvs_array[1])
    # for tellurics, use relative velocity without heliocentric correction
    else:
        med_rv = np.median(rvs_array[3])
    # for both cases use the fxcor error to get a median error of all RV values
    med_err = np.median(rvs_array[2])
    return med_rv, med_err


# get the data for one specific observation date and compute the weighted mean of the RV and the RV error
def rv_weightedmean(redmine_id, rvs_array, med_rv, med_err, rv_type):
    all_stds = []
    error_limit = input('Please give a limit for the max. allowed RV error in m/s: (e.g.: 29.0) ')

    if rv_type != 'tel':
        output_file = pf.out_RVs_weighted.format(redmine_id)
    else:
        output_file = pf.out_tels_weighted.format(redmine_id)
    with open(output_file, 'w') as out2file:
        for date in set(rvs_array[0]):
            vels_onedate = []
            v_err = []
            for j in range(len(rvs_array[0])):
                # only use the rows of the array that contain RV data from one observation date
                if rvs_array[0, j] == date:
                    if rv_type != 'tel':
                        vels_onedate.append(rvs_array[1, j])
                    else:
                        # for tellurics, use the relative RV without heliocentric correction
                        vels_onedate.append(rvs_array[3, j])

                    # if the RV error given by fxcor is zero, use the median RV error instead
                    if rvs_array[2, j] != 0.0:
                        v_err.append(rvs_array[2, j])
                    else:
                        v_err.append(med_err)

            # compute the weighted average for that date and use the median RV as zero-point correction
            rv_weightmean = np.average(vels_onedate, weights=(1/np.abs(v_err)))  # - med_rv
            if rv_type != 'tel':
                rv_weightmean = rv_weightmean - med_rv
            # compute the RV error across the orders and put it in a list of RV errors
            rv_std = np.std(vels_onedate) * np.sqrt(2) / np.sqrt(len(vels_onedate))
            all_stds.append(rv_std)

            # write the results to a file, if the data point is good,
            # which means that the error is below a certain limit
            if rv_std < float(error_limit):
                results = str(date) + ' ' + str(rv_weightmean) + ' ' + str(rv_std) + '\n'
                out2file.write(results)
            else:
                date_norm = julian.from_jd(date, fmt='jd')
                print('WARNING: Date {} has larger errors than {} m/s.'.format(date_norm, error_limit))

    return all_stds


# read the weighted RV results from the file again to fix missing RV error values
def fix_missing_errors(redmine_id, rv_type, all_stds):
    rv_results = []
    if rv_type != 'tel':
        input_file = pf.out_RVs_weighted.format(redmine_id)
    else:
        input_file = pf.out_tels_weighted.format(redmine_id)

    with open(input_file, 'r') as in2file:
        for line2 in in2file:
            line2 = line2.split()
            # check if the cross-order RV error has a reasonable value, this is not the case e.g. for the template
            # a value of 0.1 m/s cross-order RV error is probably never possible with FOCES
            # replace bad RV errors with the median of all other RV errors
            if float(line2[2]) < 0.1:
                line2[2] = str(np.median(all_stds))
                rv_results.append(line2)
            else:
                rv_results.append(line2)

    rv_tofile = sorted(rv_results, key=itemgetter(0))
    # save all RV results with the now corrected error to the file again
    rv_tofile = np.transpose(rv_tofile)

    if rv_type != 'tel':
        out2_filepath = pf.out_RVs_weighted.format(redmine_id)
    else:
        out2_filepath = pf.out_tels_weighted.format(redmine_id)
    with open(out2_filepath, 'w') as out2file_corr:
        for m in range(len(rv_tofile[0])):
            results_corr = str(rv_tofile[0, m]) + ' ' + str(rv_tofile[1, m]) + ' ' + str(rv_tofile[2, m]) + '\n'
            out2file_corr.write(results_corr)

    return rv_tofile


# save the RV results corrected with the telluric shift to a file
def get_tel_correction(redmine_id, rvs_fixerr, tel_fixerr):
    with open(pf.out_RVs_telcorr.format(redmine_id), 'w') as out4file_corr:
        for m in range(len(tel_fixerr[0])):
            results_corr = str(tel_fixerr[0, m]) + ' ' + str(
                np.float(rvs_fixerr[1, m]) - np.float(tel_fixerr[1, m])) + ' ' + str(tel_fixerr[2, m]) + '\n'
            out4file_corr.write(results_corr)

    return


# plot the RV results for all orders for each frame
def plot_single_orders(redmine_id):
    dates_rv_array = []
    # read the single order RVs from the file
    with open(pf.out_RVs_single.format(redmine_id), 'r') as singleorderfile:
        for line in singleorderfile:
            line = line.split()
            dates_rv_array.append(line)

    # convert that array to a useful format
    dates_rv_array = make_rv_array(dates_rv_array)
    print(dates_rv_array[0])

    # make a plot for each different date in the array
    for onedate in set(dates_rv_array[0]):
        order_list = []
        rv_list = []
        err_list = []
        for g in range(len(dates_rv_array[0])):
            if dates_rv_array[0, g] == onedate:
                order_list.append(dates_rv_array[-1, g])
                rv_list.append(dates_rv_array[1, g])
                err_list.append(dates_rv_array[2, g])

        onedate_norm = julian.from_jd(onedate, fmt='jd')
        date_out = dt.datetime.strftime(onedate_norm, '%m.%d_%H:%M:%S')
        # plot the whole thing
        fig = plt.figure()
        plt.errorbar(order_list, rv_list, yerr=err_list, fmt='o', label=date_out, alpha=0.5)
        plt.hlines(np.median(rv_list), min(order_list), max(order_list), lw=2)
        plt.xlabel('# of physical order')
        plt.ylabel('RV in m/s')
        plt.legend()
        plt.show()

    return


# make a plot of the data, phase-folded with the literature orbit

# plot_single_orders(2864)

# def plot_single_RVs():
#
#     return
