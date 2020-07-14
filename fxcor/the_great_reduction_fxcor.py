#!/usr/bin/env python3
# makes file executable from shell without the "python3" command in front

import os
import subprocess
import re  # module for regular expressions
import datetime as dt
import shutil
import argparse

# import statements for other python scripts
import shell_script_maker as shesm
import paths_and_files as pf
import small_functions as sf
from gamse_convert import iraf_converter
from radvel_make_conffile import make_radvel_conffile


##################################################################
# general variables and option defaults

in_date = dt.datetime.strftime(dt.datetime.now(), '%Y%m%d')
in_opt1 = '-o'
in_opt2 = '-ld'

###################################################################
# argument parser definitions

# create command line argument parser
parser = argparse.ArgumentParser(description='RV calculation for FOCES with fxcor: This program takes raw frames for '
                                             'a certain object of the FOCES spectrograph, performs a wacelength '
                                             'calibration with the GAMSE software, converts the files to MEF files and '
                                             'computes radial velocities by using IRAF\'s fxcor package. There are '
                                             'different options to choose which parts of the program should be '
                                             'executed.')

# add optional command line arguments
parser.add_argument('-fu', '--fitsupdate', help='update the local raw FITS files', action='store_true')
parser.add_argument('-lu', '--logsupdate', help='update the local observation logfiles', action='store_true')
# create a group of options that exclude their simultaneous usage
processing_dates = parser.add_mutually_exclusive_group()
processing_dates.add_argument('-o', '--only', help='process data only for the date specified, date format: YYYYMMDD or '
                                                   '"today"', type=str)
processing_dates.add_argument('-a', '--after', help='process data for all dates starting with and after the one '
                                                    'specified, date format: YYYYMMDD', type=str)

# actually parse the arguments given in the command line in the current execution of this script
args = parser.parse_args()
print(args)

#####################################################################
# actual calls of functions

# Welcome message for the user
print('Hello! I see you want to reduce some data.')

# check whether an update of the data and logfiles is needed
if args.fitsupdate:
    sf.rsync_fits_update(args.only, args.after)


    # if update is needed, execute shell scripts

    # create a script for syncing the desired dates
    if re.search(r'-lo', date_restrict, re.I):
        file_script_USM, file_script_local = shesm.script_logs_update(in_date, in_opt1)
        subprocess.call(['dos2unix', str(pf.script_USM)])
        subprocess.call(['dos2unix', str(pf.script_local)])
        print('\n')
        print('Successfully created bash scripts. Starting to sync now...')
        subprocess.call(['bash', str(pf.script_local)])
    if re.search(r'-do', date_restrict, re.I):
        data_script_USM, data_script_local = shesm.script_data_update(in_date, in_opt1)
        subprocess.call(['dos2unix', str(pf.script2_USM)])
        subprocess.call(['dos2unix', str(pf.script2_local)])
        print('\n')
        print('Successfully created bash scripts. Starting to sync now...')
        subprocess.call(['bash', str(pf.script2_local)])
    if re.search(r'-ld', date_restrict, re.I):
        file_script_USM, file_script_local = shesm.script_logs_update(in_date, in_opt1)
        data_script_USM, data_script_local = shesm.script_data_update(in_date, in_opt1)
        subprocess.call(['dos2unix', str(pf.script_USM)])
        subprocess.call(['dos2unix', str(pf.script_local)])
        subprocess.call(['dos2unix', str(pf.script2_USM)])
        subprocess.call(['dos2unix', str(pf.script2_local)])
        print('\n')
        print('Successfully created bash scripts. Starting to sync now...')
        subprocess.call(['bash', str(pf.script_local)])
        subprocess.call(['bash', str(pf.script2_local)])

else:
    print('\n')
    print('No files were updated.')
    print('\n')


# check whether an update of the data file headers is needed
print('\n')
yn_header = input('Do you also want to update the data file headers? ')
if re.match(r'^y', yn_header, re.I) or re.match(r'^j', yn_header, re.I):
    print('\n')
    print('Please enter a date and option:')
    date_restrict_head = input('(yyyymmdd; option: -a = after, -o = only, -e = everything)\n')
    # split the input into its parts
    in_date_head = date_restrict_head[:8]
    in_opt_head = date_restrict_head[-2:]

    script_add = shesm.script_add_radec(in_date_head, in_opt_head)
    subprocess.call(['dos2unix', str(pf.script_add)])
    print('\n')
    print('Starting to update the headers now...')
    subprocess.call(['bash', str(pf.script_add)])

else:
    print('\n')
    print('No headers were updated.')
    print('\n')


# ask if the data should be sorted for a specific observation project
print('\n')
yn_sortproject = input('Do you want to get the data of a specific redmine project? ')

if re.match(r'^y', yn_sortproject, re.I) or re.match(r'^j', yn_sortproject, re.I):
    print('\n')
    redmine_id = input('Please provide the desired redmine project ID: ')
    print('\n')
    print('Please enter a date and option:')
    date_restrict_redID = input('(yyyymmdd; option: -a = after, -o = only, -e = everything)\n')
    # split the input into its parts
    in_date_red = date_restrict_redID[:8]
    in_opt_red = date_restrict_redID[-2:]

    # create and execute a script for searching the redmine ID
    script_grep_ID = shesm.script_grep_redmineid(redmine_id, in_date_red, in_opt_red)
    subprocess.call(['dos2unix', str(script_grep_ID)])
    print('\n')
    print('Successfully created bash script for grep. Starting to search now...')
    subprocess.call(['bash', str(script_grep_ID)])

    # write all observation dates to a file
    sf.get_obsnights(redmine_id)

else:
    print('\n')
    print('No files were searched.')
    print('\n')

# ask if data of a certain project should be copied to the gamse reduction folders
print('\n')
yn_copytogamse = input('Do you want to copy the data of a specific redmine project to the GAMSE reduction folders? ')

if re.match(r'^y', yn_copytogamse, re.I) or re.match(r'^j', yn_copytogamse, re.I):
    print('\n')
    redmine_id = input('Please provide the desired redmine project ID: ')
    print('\n')
    print('Please enter a date and option:')
    date_restrict_copy = input('(yyyymmdd; option: -a = after, -o = only, -e = everything)\n')
    # split the input into its parts
    in_date_copy = date_restrict_copy[:8]
    in_opt_copy = date_restrict_copy[-2:]

    # create and execute a script for copying the required raw data to the reduction folders
    shesm.script_sort_for_reduction(redmine_id, in_date_copy, in_opt_copy)
    subprocess.call(['dos2unix', str(pf.sort_copy_cmd.format(redmine_id))])
    print('\n')
    print('Successfully created bash script for copy. Starting to copy now...')
    subprocess.call(['bash', str(pf.sort_copy_cmd.format(redmine_id))])
    print('\n')
    print('Finished copying the files to the reduction folders.')


# ask if the data should be wavelength calibrated with GAMSE
print('\n')
yn_wvcal = input('Do you want to do the wavelength calibration with GAMSE? ')

if re.match(r'^y', yn_wvcal, re.I) or re.match(r'^j', yn_wvcal, re.I):
    print('\n')
    redmine_id = input('Please give the redmine ID once again: ')
    # read the dates that should be reduced from the file
    use_only_these_reduction_dates = sf.get_reductiondates(redmine_id)

    print('\n')
    print('Started wavelength calibration...')

    # start the wavelength calibration with the newest data folder
    use_only_these_reduction_dates.sort(reverse=True)
    for i in use_only_these_reduction_dates:
        red_folder_path = os.path.join(pf.abs_path_red_gamse, 'red_{}'.format(str(i)))
        # change the working directory to the data reduction folder, needed for GAMSE calls to work properly
        os.chdir(str(red_folder_path))
        print('\n')
        print('Data reduction started for : {}'.format(i))
        subprocess.call(['gamse', 'config'])
        subprocess.call(['gamse', 'list'])
        subprocess.call(['gamse', 'reduce'])


# ask if the data with wavelength calibration should be copied to the IRAF folder
print('\n')
yn_wvcal_copy = input('Do you want to copy the wavelength calibrated data to the IRAF folder? ')

if re.match(r'^y', yn_wvcal_copy, re.I) or re.match(r'^j', yn_wvcal_copy, re.I):
    print('\n')
    redmine_id = input('Just to be sure, enter the redmine ID one last time: ')
    sf.script_copy_reduced_data(redmine_id)
else:
    print('\n')
    print('No files were copied to the IRAF folder.')
    print('\n')


# convert the GAMSE data to IRAF readable form if required
print('\n')
yn_iraf_convert = input('Do you want to convert the wavelength calibrated data to IRAF readable form? ')

if re.match(r'^y', yn_iraf_convert, re.I) or re.match(r'^j', yn_iraf_convert, re.I):
    print('\n')
    str_redmine_id = input('Please enter the redmine ID and the name of the object (format: XXXX identifierforSIMBAD): ')
    str_redmine_id = str_redmine_id.strip()
    str_redmine_id = str_redmine_id.split()
    redmine_id = str_redmine_id[0]
    objname = str_redmine_id[1]
    iraf_converter(redmine_id, objname)

else:
    print('\n')
    print('No files were converted.')
    print('\n')


# prepare data for fxcor and give instructions for IRAF execution
print('\n')
yn_iraf_execute = input('Do you want to do the cross-correlation function for all data with IRAF? ')

if re.match(r'^y', yn_iraf_execute, re.I) or re.match(r'^j', yn_iraf_execute, re.I):
    print('\n')
    redmine_id = input('Surprise: I need the redmine ID again: ')
    shutil.copy(pf.make_orderlists, pf.iraf_output_folder.format(redmine_id))
    # subprocess.call(['cp', pf.make_orderlists, pf.iraf_output_folder.format(redmine_id)])
    orderlists_path = os.path.join(pf.iraf_output_folder.format(redmine_id), pf.recipe_orderlists)
    os.chdir(str(pf.iraf_output_folder.format(redmine_id)))
    subprocess.call(['dos2unix', str(orderlists_path)])
    subprocess.call(['bash', str(orderlists_path)])

    print('List of frames for this object: {}'.format(pf.all_used_frames.format(redmine_id)))
    template = input('Please choose a template that should be used for the cross correlation: '
                     '(e.g.: 20190903_0114_FOC1903_SCI0) ')
    outname = input('Please give a name for the fxcor output file: (e.g.: out_allRVs_200319) ')
    shesm.script_fxcor_lists(redmine_id, template, outname)
    subprocess.call(['dos2unix', str(pf.make_cl_fxcor.format(redmine_id))])
    subprocess.call(['bash', str(pf.make_cl_fxcor.format(redmine_id))])

    print('Please open a terminal now and type "xterm". Then go to the new window.')
    print('Type the following command in the xterm window: \n')
    input('$ cl')
    print('After IRAF has loaded, please execute the following commands: \n')
    print('vocl> reset obsdb=home$obsdb.dat')
    input('vocl> rv')
    print('Now navigate to the folder containing the data: \n')
    input('rv> cd {}'.format(pf.iraf_output_folder))
    print('make a list of all the spectra used as templates: \n')
    input('rv> files {}_*_A_*.fits > templates_ID{}.lis'.format(template, redmine_id))
    print('now do the heliocentric correction for the template spectra: enter the given command or open '
          '"epar rvcorrect" and put the template list as entry for '
          '"images": "images = @templates_ID{}.lis"\n'.format(redmine_id))
    input('rv> rvcorrect images=@templates_ID{}.lis'.format(redmine_id))
    print('finally, execute fxcor: (may take a while, please hit ENTER here when finished)\n')
    input('cl < fxcor_with_lists.cl')


# extract the RVs from the fxcor results
print('\n')
yn_RV_extract = input('Do you want to extract the RV values you got from fxcor? ')

if re.match(r'^y', yn_RV_extract, re.I) or re.match(r'^j', yn_RV_extract, re.I):
    print('\n')
    redmine_id = input('The redmine ID is needed once again: ')
    fxcor_outfile = input('Tell me which fxcor output file to use: (e.g.: out_allRVs_200319) ')
    sf.get_rvs(redmine_id, fxcor_outfile)
    RVs_single, tels_single = sf.split_rvs_tel(redmine_id)
    RVs_single_med, RVerr_single_med = sf.rv_and_err_median(RVs_single, 'obj')
    tels_single_med, telserr_single_med = sf.rv_and_err_median(tels_single, 'tel')

    yn_plot_singleorders = input('Do you want to plot the RV results for the single orders?')
    if re.match(r'^y', yn_plot_singleorders, re.I) or re.match(r'^j', yn_plot_singleorders, re.I):
        print('\n')
        sf.plot_single_orders(redmine_id)

    RVs_stds = sf.rv_weightedmean(redmine_id, RVs_single, RVs_single_med, RVerr_single_med, 'obj')
    tel_stds = sf.rv_weightedmean(redmine_id, tels_single, tels_single_med, telserr_single_med, 'tel')
    RVs_fixerr = sf.fix_missing_errors(redmine_id, 'obj', RVs_stds)
    tel_fixerr = sf.fix_missing_errors(redmine_id, 'tel', tel_stds)
    sf.get_tel_correction(redmine_id, RVs_fixerr, tel_fixerr)


# make a plot of the literature values compared to the FOCES data
print('\n')
yn_RV_complit = input('Do you want to plot the RV results and compare them to the literature? ')

if re.match(r'^y', yn_RV_complit, re.I) or re.match(r'^j', yn_RV_complit, re.I):
    print('\n')
    redmine_id = input('The redmine ID is needed once again: ')
    n_cand = input('Please enter the number of planet candidates: ')
    inst_list = input('Give a list of the instruments that were used (separate with space): ')
    inst_list = inst_list.split(' ')
    config_file = make_radvel_conffile(redmine_id, n_cand, inst_list)
    os.chdir(str(pf.location.resolve()))
    subprocess.call(['myradvel', 'fit', '-s', str(config_file), '-d', str(pf.abs_path_rvplots)])
    subprocess.call(['myradvel', 'plot', '-t', 'rv', '-s', str(config_file), '-d', str(pf.abs_path_rvplots)])


# make a plot of the RV values compared to other data (e.g. airmass)
print('\n')
yn_RV_nonRV = input('Do you want to plot the RV results and compare them to some other non-RV data? ')

if re.match(r'^y', yn_RV_nonRV, re.I) or re.match(r'^j', yn_RV_nonRV, re.I):
    print('\n')
    redmine_id = input('The redmine ID is needed once again: ')
    want_value, pos, filetype = sf.get_nonrv_type()
    sf.extract_nonrv_data(redmine_id, want_value, pos, filetype)
    config_file = pf.radvel_config.format(redmine_id)
    os.chdir(str(pf.location.resolve()))
    subprocess.call(['myradvel', 'fit', '-s', str(config_file), '-d', str(pf.abs_path_rvplots)])
    subprocess.call(['myradvel', 'plot', '-t', 'nonrv', '-s', str(config_file), '-d', str(pf.abs_path_rvplots)])

# do the fxcor reduction manually
print('\n')
input('Please hit ENTER when finished.')


# # plot the data produced by fxcor
# print('\n')
# yn_plotdata = input('Do you want to plot the RVs you got from fxcor? ')
#
# if re.match(r'^y', yn_wvcal_copy, re.I) or re.match(r'^j', yn_wvcal_copy, re.I):
#     print('\n')
#     redmine_id = input('I am sorry to ask for the redmine ID yet again: ')
#     plot_type = input('What kind of plot do you want to create? (single: only one dataset, '
#                       'double: comparison of two datasets)')
#
#     if re.search(r'single', plot_type, re.I):
#
#
#
