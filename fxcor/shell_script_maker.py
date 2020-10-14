import os
import datetime as dt
import calendar
import re  # module for regular expressions

# import statements for other python scripts
import paths_and_files as pf
import small_functions as sf


now = dt.datetime.now()
# # create a list with all years from when FOCES data exist
# years_log = list(range(2016, now.year + 1))
# years_comm = list(range(2018, now.year + 1))
# list of years where data is available in fcs_links
years_data = list(range(2019, now.year + 1))

# standard command for rsync from ohiaai to USM PC
cmd1 = 'rsync -av wstobserver@195.37.68.19:/data/3kk/{}/'
# standard command for rsync from FOCES PC to USM PC
cmd2 = 'rsync -av foces@195.37.68.140:/data/fcs_links/'
# standard command for rsync from USM PC to local machine
cmd3 = 'rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/{}'
# standard command for executing remote sync scripts via ssh
cmd4 = 'ssh fahrenschon@ltsp01.usm.uni-muenchen.de "bash -s" < {}\n'
# standard command for adding header entries from obslog files
cmd5 = 'bash /mnt/e/FOCES_data/add_radec.sh {}\n'
# standard command for grepping the redmine ID of a project
# cmd6 = 'grep -l -R "PROJECT[[:blank:]]*=[[:blank:]]*{}" '  # for grepping in the FITS headers
cmd6 = 'cat {0}/logfile.{1} | awk \'{{if($24=="{2}|"){{print $0}}}}\' >> {3}\n'  # prints the output only to the file
cmd61 = 'awk -v redmineid={0} -f {1} {2}/logfile.{3} >> {4}\n'  # call the awk script to sort the logfile entries for the redmine ID
# cmd61 = 'cat {0}/logfile.{1} | awk \'/fcs_/{{if($24=="{2}|"){{print $0}}}}\' >> {3}\n'  # prints the output only to the file
# cmd6 = '(cat {0}/logfile.{1} | grep "{2}") | tee {3}\n'  # prints the output also to console
# standard commands for preparing the GAMSE reduction
cmd7 = 'mkdir {}\n'
# messages to be displayed by the scripts
msg_pw_usm = 'echo "Please provide the password for the USM machine (ltsp01):"\n'
msg_sync_to_usm = 'echo "Syncing the {} files to USM HOST machine..."\n'
msg_sync_to_local = 'echo "Syncing the {} files to the LOCAL machine..."\n'

# dif_files = ['log', 'comments']
dif_folders = ['copy_logs/obslog', 'temp_frames']


# function to create script for syncing all requested log and comment files to USM PC
def script_logs_update(date, option):
    years_list, directory, file1 = sf.get_category()
    with open(pf.script_USM, 'w') as scriptout1:
        scriptout1.write('#!/usr/bin/bash\n')
        scriptout1.write('\n')
        scriptout1.write('mkdir -p ~/copy_logs/obslog\n')
        with open(pf.script_local, 'w') as scriptout3:
            scriptout3.write('#!/usr/bin/bash\n')
            scriptout3.write('\n')
            # add commands to execute the remote script
            scriptout3.write(msg_sync_to_usm.format('log and comment'))
            scriptout3.write(msg_pw_usm)
            scriptout3.write(cmd4.format(pf.script_USM))
            scriptout3.write(msg_sync_to_local.format('log and comment'))
            scriptout3.write(msg_pw_usm)

            # make logfile syncing script for single date
            if option == '-o':
                yr = str(date)[:4]
                # handle ohiaai to USM part
                for cat in range(len(directory)):
                    rsync_cmd1_usm = cmd1.format(directory[cat]) + '{}/{}.{} ~/copy_logs/obslog\n'.format(yr, file1[cat],
                                                                                                 str(date))
                    scriptout1.write(rsync_cmd1_usm)

                # handle the USM to local part
                scriptout3.write(cmd3.format('copy_logs/obslog/*.{}'.format(str(date))) +
                                 ' ' + str(pf.abs_path_obslog) + '\n')

            # make logfile syncing script starting with specific date
            if option == '-a':
                startdate = dt.datetime.strptime(str(date), '%Y%m%d')
                # handle ohiaai to USM part
                for cat in range(len(directory)):
                    for yr in years_list[cat]:
                        # this is how to handle the year when the request starts
                        if yr == startdate.year:
                            # handle the rest of the starting month
                            startmonth = str(startdate.year) + str('{:02d}').format(startdate.month)
                            # add all days that are still left from the starting month
                            if startdate.year == now.year and startdate.month == now.month:
                                days = list(range(startdate.day, now.day + 1))
                            else:
                                end_of_month = calendar.monthrange(yr, startdate.month)[1]
                                days = list(range(startdate.day, end_of_month + 1))

                            # add a rsync command for all individual days of the starting month
                            for single_day in days:
                                expl_date = (startmonth[2:] + '{:02d}'.format(single_day))
                                # add command for ohiaai to USM
                                rsync_cmd1_usm = cmd1.format(directory[cat]) + '{0}/{1}.{2} ~/copy_logs/obslog\n'.format(yr, file1[cat], expl_date)
                                scriptout1.write(rsync_cmd1_usm)

                                # handle USM to local part
                                # (write command only for the logfile dates, because they will exist in any case)
                                if file1[cat] == 'logfile':
                                    scriptout3.write(cmd3.format('copy_logs/obslog/*.{}'.format(expl_date)) +
                                                 ' ' + str(pf.abs_path_obslog) + '\n')

                            # handle the other months of the starting year
                            if startdate.year < now.year:
                                months = list(range(startdate.month + 1, 13))
                            if startdate.year == now.year and startdate.month <= now.month:
                                months = list(range(startdate.month + 1, now.month + 1))
                            for single_month in months:
                                cur_month = str(startdate.year)[2:] + '{:02d}'.format(single_month)
                                # handle ohiaai to USM part
                                rsync_cmd1_usm = cmd1.format(directory[cat]) + '{0}/{1}.{2} ~/copy_logs/obslog\n'.format(yr, file1[cat], (cur_month + '*'))
                                scriptout1.write(rsync_cmd1_usm)

                                # handle USM to local part
                                if file1[cat] == 'logfile':
                                    scriptout3.write(cmd3.format('copy_logs/obslog/*.{}'.format(cur_month + '*')) +
                                                 ' ' + str(pf.abs_path_obslog) + '\n')

                        # for all years after that, copy the complete folder of each year
                        if yr > startdate.year:
                            # handle ohiaai to USM part
                            rsync_cmd1_usm = cmd1.format(directory[cat]) + '{0}/ ~/copy_logs/obslog\n'.format(yr)
                            scriptout1.write(rsync_cmd1_usm)

                            # handle USM to local part
                            if file1[cat] == 'logfile':
                                scriptout3.write(cmd3.format('copy_logs/obslog/*.{}'.format(str(yr)[2:] + '*')) +
                                             ' ' + str(pf.abs_path_obslog) + '\n')

            if option == '-e':
                # copy the complete folders of all years
                for cat in range(len(directory)):
                    for yr in years_list[cat]:
                        # handle ohiaai to USM part
                        rsync_cmd1_usm = cmd1.format(directory[cat]) + '{0}/ ~/copy_logs/obslog\n'.format(yr)
                        scriptout1.write(rsync_cmd1_usm)

                        # handle USM to local part
                        if file1[cat] == 'logfile':
                            scriptout3.write(cmd3.format('copy_logs/obslog/*.{}'.format(str(yr)[2:] + '*')) +
                                             ' ' + str(pf.abs_path_obslog) + '\n')

        # add a nice message to indicate the regular end of the sync process
        scriptout1.write('echo "Finished syncing logs to USM!"\n')
        print('Sync script for logfiles successfully created!')

    # return the file name of the script that was created for copying etc.
    return pf.file_script_USM, pf.file_script_local


# # function to create script for syncing all requested data files (FITS frames) to USM PC
# def script_data_update(date, option):
#     startdate = dt.datetime.strptime(str(date), '%Y%m%d')
#     if startdate < dt.datetime.strptime(str(20190430), '%Y%m%d'):
#         print('Warning: The date you chose is before the start of automatic data collection (20190430).')
#     with open(pf.script2_USM, 'w') as scriptout2:
#         scriptout2.write('#!/usr/bin/bash\n')
#         scriptout2.write('\n')
#
#         with open(pf.script2_local, 'w') as scriptout3x:
#             scriptout3x.write('#!/usr/bin/bash\n')
#             scriptout3x.write('\n')
#             # add commands to execute the remote script
#             scriptout3x.write(msg_sync_to_usm.format('data'))
#             scriptout3x.write(msg_pw_usm)
#             scriptout3x.write(cmd4.format(pf.script2_USM))
#             scriptout3x.write(msg_sync_to_local.format('data'))
#             scriptout3x.write(msg_pw_usm)
#
#             # make data syncing script for single date
#             if option == '-o':
#                 # handle ohiaai to USM part
#                 rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format(str(date))
#                 scriptout2.write(rsync_cmd2_usm)
#
#                 # handle USM to local part
#                 scriptout3x.write(cmd3.format('temp_frames/{}'.format(str(date))) + ' ' + str(pf.abs_path_data) + '\n')
#
#             # make data syncing script starting with specific date
#             if option == '-a':
#                 for yr in years_data:
#                     # this is how to handle the year when the request starts
#                     if yr == startdate.year:
#                         # handle the rest of the starting month
#                         startmonth = str(startdate.year) + str('{:02d}').format(startdate.month)
#                         # add all days that are still left from the starting month
#                         if startdate.year == now.year and startdate.month == now.month:
#                             days = list(range(startdate.day, now.day + 1))
#                         else:
#                             end_of_month = calendar.monthrange(yr, startdate.month)[1]
#                             days = list(range(startdate.day, end_of_month + 1))
#
#                         # add a rsync command for all individual days of the starting month
#                         for single_day in days:
#                             expl_date = (startmonth + '{:02d}'.format(single_day))
#
#                             # handle ohiaai to USM part
#                             rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format(expl_date)
#                             scriptout2.write(rsync_cmd2_usm)
#                             # handle USM to local part
#                             scriptout3x.write(cmd3.format('temp_frames/{}'.format(expl_date)) + ' ' + str(pf.abs_path_data) + '\n')
#
#                         # handle the other months of the starting year
#                         if startdate.year < now.year:
#                             months = list(range(startdate.month + 1, 13))
#                         if startdate.year == now.year and startdate.month <= now.month:
#                             months = list(range(startdate.month + 1, now.month + 1))
#                         for single_month in months:
#                             cur_month = str(startdate.year) + '{:02d}'.format(single_month)
#
#                             # handle ohiaai to USM part
#                             rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format((cur_month + '*'))
#                             scriptout2.write(rsync_cmd2_usm)
#                             # handle USM to local part
#                             scriptout3x.write(cmd3.format('temp_frames/{}'.format((cur_month + '*'))) + ' ' + str(pf.abs_path_data) + '\n')
#
#                     # for all years after that, copy all folders of each year
#                     if yr > startdate.year:
#                         # handle ohiaai to USM part
#                         rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format((str(yr) + '*'))
#                         scriptout2.write(rsync_cmd2_usm)
#                         # handle USM to local part
#                         scriptout3x.write(cmd3.format('temp_frames/{}'.format((str(yr) + '*'))) + ' ' + str(pf.abs_path_data) + '\n')
#
#             if option == '-e':
#                 # copy the complete folders of all years
#                 for yr in years_data:
#                     # handle ohiaai to USM part
#                     rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format((str(yr) + '*'))
#                     scriptout2.write(rsync_cmd2_usm)
#                     # handle USM to local part
#                     scriptout3x.write(cmd3.format('temp_frames/{}'.format((str(yr) + '*'))) + ' ' + str(pf.abs_path_data) + '\n')
#
#         # add a nice message to indicate the regular end of the sync process
#         scriptout2.write('echo "Finished syncing data to USM!"\n')
#         print('Sync script for data successfully created!')
#
#     # return the file name of the script that was created for copying etc.
#     return pf.data_script_USM, pf.data_script_local


# make script to automatically add the project ID etc. to the FITS header
def script_add_radec(date, option):
    startdate = dt.datetime.strptime(str(date), '%Y%m%d')
    if startdate < dt.datetime.strptime(str(20190430), '%Y%m%d'):
        print('Warning: The date you chose is before the start of automatic data collection (20190430).')
        startdate = dt.datetime.strptime(str(20190430), '%Y%m%d')
    with open(pf.script_add, 'w') as scriptout4:
        scriptout4.write('#!/usr/bin/bash\n')
        scriptout4.write('\n')

        # make script for header editing for single date
        if option == '-o':
            str_expl_date = dt.datetime.strftime(startdate, '%Y%m%d')
            add_cmd = cmd5.format(str_expl_date)
            scriptout4.write(add_cmd)

        # make script for header editing starting with specific date
        if option == '-a':
            if startdate <= now:
                # look at all the dates between startdate and now
                dates_delta = now - startdate
                for each_date in range(dates_delta.days + 1):
                    expl_date = startdate + dt.timedelta(days=each_date)
                    str_expl_date = dt.datetime.strftime(expl_date, '%Y%m%d')
                    date_path = os.path.join(pf.abs_path_data, str_expl_date)
                    # check if a data directory exists for that date and add a command to the script
                    if os.path.exists(str(date_path)):
                        add_cmd = cmd5.format(str_expl_date)
                        scriptout4.write(add_cmd)

        # make script for all the available data
        if option == '-e':
            startdate = dt.datetime.strptime(str(20190430), '%Y%m%d')
            # look at all the dates between startdate and now
            dates_delta = now - startdate
            for each_date in range(dates_delta.days + 1):
                expl_date = startdate + dt.timedelta(days=each_date)
                str_expl_date = dt.datetime.strftime(expl_date, '%Y%m%d')
                date_path = os.path.join(pf.abs_path_data, str_expl_date)
                # check if a data directory exists for that date and add a command to the script
                if os.path.exists(str(date_path)):
                    add_cmd = cmd5.format(str_expl_date)
                    scriptout4.write(add_cmd)


# make script to automatically search the project ID of one specific project
def script_grep_redmineid(redmine_id, date, option):
    startdate = dt.datetime.strptime(str(date), '%Y%m%d')
    if startdate < dt.datetime.strptime(str(20190430), '%Y%m%d'):
        print('Warning: The date you chose is before the start of automatic data collection (20190430).')
        startdate = dt.datetime.strptime(str(20190430), '%Y%m%d')
    with open(pf.grep_redID_cmd.format(redmine_id), 'w') as scriptout5:
        scriptout5.write('#!/usr/bin/bash\n')
        scriptout5.write('\n')
        scriptout5.write('rm {}\n'.format(str(pf.grep_redID_out.format(redmine_id))))
        # get the first line with the column titles of the obslogfiles
        grep_title_cmd = cmd6.format(str(pf.abs_path_obslog), dt.datetime.strftime(startdate, '%Y%m%d')[2:],
                                     'object', str(pf.grep_redID_out.format(redmine_id)))
        scriptout5.write(grep_title_cmd)

        # make script for searching in a single date
        if option == '-o':
            str_expl_date = dt.datetime.strftime(startdate, '%Y%m%d')
            grep_cmd = cmd61.format(redmine_id, str(pf.awk_script), str(pf.abs_path_obslog), str_expl_date[2:],
                                   str(pf.grep_redID_out.format(redmine_id)))
            scriptout5.write(grep_cmd)

        # make script for search starting with specific date
        if option == '-a':
            if startdate <= now:
                # look at all the dates between startdate and now
                dates_delta = now - startdate
                for each_date in range(dates_delta.days + 1):
                    expl_date = startdate + dt.timedelta(days=each_date)
                    str_expl_date = dt.datetime.strftime(expl_date, '%Y%m%d')
                    logfile_path = os.path.join(pf.abs_path_obslog, 'logfile.{}'.format(str_expl_date[2:]))
                    # check if a logfile exists for that date and add a command to the script
                    if os.path.exists(str(logfile_path)):
                        grep_cmd = cmd61.format(redmine_id, str(pf.awk_script), str(pf.abs_path_obslog), str_expl_date[2:],
                                               str(pf.grep_redID_out.format(redmine_id)))
                        scriptout5.write(grep_cmd)

        # make script for all the available data
        if option == '-e':
            startdate = dt.datetime.strptime(str(20190430), '%Y%m%d')
            # look at all the dates between startdate and now
            dates_delta = now - startdate
            for each_date in range(dates_delta.days + 1):
                expl_date = startdate + dt.timedelta(days=each_date)
                str_expl_date = dt.datetime.strftime(expl_date, '%Y%m%d')
                logfile_path = os.path.join(pf.abs_path_obslog, 'logfile.{}'.format(str_expl_date[2:]))
                # check if a logfile exists for that date and add a command to the script
                if os.path.exists(str(logfile_path)):
                    grep_cmd = cmd61.format(redmine_id, str(pf.awk_script), str(pf.abs_path_obslog), str_expl_date[2:],
                                           str(pf.grep_redID_out.format(redmine_id)))
                    scriptout5.write(grep_cmd)

    return pf.grep_redID_cmd.format(redmine_id)


# make script to automatically copy the folders containing data of one specific project
def script_sort_for_reduction(redmine_id, date, option):
    dates_for_red = []
    dates_for_red_lim = []

    for line in open(pf.out_gamse_sorted.format(redmine_id), 'r'):
        line = line.strip()
        dates_for_red.append(line)

    # remove all unnecessary dates from the list for copying
    startdate = dt.datetime.strptime(str(date), '%Y%m%d')
    # use only one specific night
    if option == '-o':
        if date in set(dates_for_red):
            dates_for_red_lim.append(date)
        else:
            print('WARNING: There is no data with redmine ID {} in the night {}.\n'.format(redmine_id, date))
            print(dates_for_red)
            new_date = input('Please choose one of the dates listed above: ')
            dates_for_red_lim.append(new_date)
    # use all observed nights after (and including) a specific date
    if option == '-a':
        for night in dates_for_red:
            if startdate <= dt.datetime.strptime(str(night), '%Y%m%d'):
                dates_for_red_lim.append(night)
    # use all observed nights
    if option == '-e':
        for night in dates_for_red:
            dates_for_red_lim.append(night)

    dates_for_red_with_discard = dates_for_red_lim.copy()

    with open(pf.sort_copy_cmd.format(redmine_id), 'w') as scriptout6:
        for single_date in dates_for_red_lim:
            new_folder = os.path.join(pf.abs_path_red_gamse, 'red_{}'.format(str(single_date)))
            orig_data_links = os.path.join(pf.abs_path_data, str(single_date))
            # make a new folder if a reduction folder does not already exist
            if os.path.exists(str(new_folder)):
                print('\n')
                yn_overwrite_old = input('Data were already reduced for the date {}. '
                                         'Do you want to discard and overwrite those? '.format(single_date))
                # discard old reduction data if needed
                if re.match(r'^y', yn_overwrite_old, re.I) or re.match(r'^j', yn_overwrite_old, re.I):
                    scriptout6.write('rm -r {}/*\n'.format(new_folder))
                    scriptout6.write(cmd7.format(str(new_folder) + '/rawdata'))
                    # copy the symbolic links to the rawdata folder
                    cmd8 = 'cp -s {0}/{1}_*.fits {2}/rawdata/.\n'.format(str(orig_data_links), str(single_date),
                                                                         str(new_folder))
                    scriptout6.write(cmd8)
                else:
                    dates_for_red_with_discard.remove(single_date)
                    print('Will not copy rawdata for {}.\n'.format(single_date))
            else:
                scriptout6.write(cmd7.format(str(new_folder)))
                scriptout6.write(cmd7.format(str(new_folder) + '/rawdata'))
                # copy the symbolic links to the rawdata folder
                cmd8 = 'cp -s {0}/{1}_*.fits {2}/rawdata/.\n'.format(str(orig_data_links), str(single_date),
                                                                     str(new_folder))
                scriptout6.write(cmd8)

    with open(pf.out_gamse_copy.format(redmine_id), 'w') as copyfile:
        for each_date in dates_for_red_with_discard:
            copyfile.write(each_date + '\n')

    return


# # make a script to generate a input cl file for fxcor
# def script_fxcor_lists(redmine_id, template_name, output_name):
#     with open(pf.make_cl_fxcor.format(redmine_id), 'w') as scriptout_fx:
#         scriptout_fx.write('#!/usr/bin/bash\n')
#         scriptout_fx.write('\n')
#         scriptout_fx.write('rm -f fxcor_with_lists.cl\n')
#         scriptout_fx.write('name1="fxcor_ord"\n')
#         scriptout_fx.write('name2=".lis"\n')
#         scriptout_fx.write('for i in {1..84..1}\n')
#         scriptout_fx.write('do\n')
#         scriptout_fx.write('  let k=i+64\n')
#         scriptout_fx.write('  for j in `ls $name1$k$name2`\n')
#         scriptout_fx.write('  do\n')
#         scriptout_fx.write('    echo "fxcor @"$j "{}_ods_fred.fits["$i"] output={} osample=p150-1998 '
#                            'rsample=p150-1998" >> fxcor_with_lists.cl\n'.format(template_name, output_name))
#         scriptout_fx.write('  done\n')
#         scriptout_fx.write('done\n')
#
#     return

# script_fxcor_lists(2864, 'testwhatever')
