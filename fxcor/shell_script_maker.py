import os
from pathlib import Path
import sys
import datetime as dt
import calendar

# import statements for other python scripts
import paths_and_files as pf

# # define the required paths and filenames
# path_scripts = 'scripts/'
# path_obslog_local = '../../../logfiles/observations'
# path_data_local = '../../../FOCES_data'
# file_script_USM = 'sync_obslogfiles_USM.sh'
# data_script_USM = 'sync_datafiles_USM.sh'
# file_script_local = 'sync_obslogfiles_local.sh'
# add_header_script = 'add_header_entries.sh'
#
# # initialize all paths and filenames and make them platform independent
# location = Path(__file__).parent
# abs_path_scripts = (location / path_scripts).resolve()
# abs_path_obslog = (location / path_obslog_local).resolve()
# abs_path_data = (location / path_data_local).resolve()
# script_USM = os.path.join(abs_path_scripts, file_script_USM)
# script2_USM = os.path.join(abs_path_scripts, data_script_USM)
# script_local = os.path.join(abs_path_scripts, file_script_local)
# script_add = os.path.join(abs_path_scripts, add_header_script)

now = dt.datetime.now()
# create a list with all years from when FOCES data exist
years_log = list(range(2016, now.year + 1))
years_comm = list(range(2018, now.year + 1))
# list of years where data is available in fcs_links
years_data = list(range(2019, now.year + 1))

# standard command for rsync from ohiaai to USM PC
cmd1 = 'rsync -av wstobserver@195.37.68.19:/data/3kk/{}/'
# standard command for rsync from FOCES PC to USM PC
cmd2 = 'rsync -av foces@195.37.68.140:/data/fcs_links/'
# standard command for rsync from USM PC to local machine
cmd3 = 'rsync -av fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/{}'
# standard command for executing remote sync scripts via ssh
cmd4 = 'ssh fahrenschon@ltsp01.usm.uni-muenchen.de "bash -s" < {}\n'
# standard command for adding header entries from obslog files
cmd5 = 'bash /mnt/e/FOCES_data/add_radec.sh {}\n'
# standard command for grepping the redmine ID of a project
# cmd6 = 'grep -l -R "PROJECT[[:blank:]]*=[[:blank:]]*{}" '  # for grepping in the FITS headers
cmd6 = 'cat {0}/logfile.{1} | grep "{2}" >> {3}\n'  # prints the output only to the file
# cmd6 = '(cat {0}/logfile.{1} | grep "{2}") | tee {3}\n'  # prints the output also to console

dif_files = ['log', 'comments']
dif_folders = ['copy_logs/obslog', 'temp_frames']


# function to create script for syncing all requested log and comment files to USM PC
def script_logs_update(date, option):
    with open(pf.script_USM, 'w') as scriptout1:
        scriptout1.write('#!/usr/bin/bash\n')
        scriptout1.write('\n')
        scriptout1.write('mkdir -p ~/copy_logs/obslog\n')

        for cat in dif_files:
            # check whether to use the log or comments year list
            if cat == 'log':
                years_list = years_log
                dir = 'log'
                file1 = 'logfile'
            if cat == 'comments':
                years_list = years_comm
                dir = 'comments'
                file1 = 'comments'

            # make logfile syncing script for single date
            if option == '-o':
                yr = str(date)[:4]
                rsync_cmd1_usm = cmd1.format(dir) + '{0}/{1}.{2} ~/copy_logs/obslog\n'.format(yr, file1, str(date))
                scriptout1.write(rsync_cmd1_usm)

            # make logfile syncing script starting with specific date
            if option == '-a':
                startdate = dt.datetime.strptime(str(date), '%Y%m%d')
                for yr in years_list:
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
                            rsync_cmd1_usm = cmd1.format(dir) + '{0}/{1}.{2} ~/copy_logs/obslog\n'.format(yr, file1, expl_date)
                            scriptout1.write(rsync_cmd1_usm)

                        # handle the other months of the starting year
                        if startdate.year < now.year:
                            months = list(range(startdate.month + 1, 13))
                        if startdate.year == now.year and startdate.month <= now.month:
                            months = list(range(startdate.month + 1, now.month + 1))
                        for single_month in months:
                            cur_month = str(startdate.year)[2:] + '{:02d}'.format(single_month)
                            rsync_cmd1_usm = cmd1.format(dir) + '{0}/{1}.{2} ~/copy_logs/obslog\n'.format(yr, file1, (cur_month + '*'))
                            scriptout1.write(rsync_cmd1_usm)
                    # for all years after that, copy the complete folder of each year
                    if yr > startdate.year:
                        rsync_cmd1_usm = cmd1.format(dir) + '{0}/ ~/copy_logs/obslog\n'.format(yr)
                        scriptout1.write(rsync_cmd1_usm)

            if option == '-e':
                # copy the complete folders of all years
                for yr in years_list:
                    rsync_cmd1_usm = cmd1.format(dir) + '{0}/ ~/copy_logs/obslog\n'.format(yr)
                    scriptout1.write(rsync_cmd1_usm)

        # add a nice message to indicate the regular end of the sync process
        scriptout1.write('echo "Finished syncing logs to USM!"\n')
        print('Sync script for logfiles successfully created!')

    # return the file name of the script that was created for copying etc.
    return pf.file_script_USM


# function to create script for syncing all requested data files (FITS frames) to USM PC
def script_data_update(date, option):
    startdate = dt.datetime.strptime(str(date), '%Y%m%d')
    if startdate < dt.datetime.strptime(str(20190430), '%Y%m%d'):
        print('Warning: The date you chose is before the start of automatic data collection (20190430).')
    with open(pf.script2_USM, 'w') as scriptout2:
        scriptout2.write('#!/usr/bin/bash\n')
        scriptout2.write('\n')
        # make data syncing script for single date
        if option == '-o':
            rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format(str(date))
            scriptout2.write(rsync_cmd2_usm)

        # make logfile syncing script starting with specific date
        if option == '-a':
            for yr in years_data:
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
                        expl_date = (startmonth + '{:02d}'.format(single_day))
                        rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format(expl_date)
                        scriptout2.write(rsync_cmd2_usm)

                    # handle the other months of the starting year
                    if startdate.year < now.year:
                        months = list(range(startdate.month + 1, 13))
                    if startdate.year == now.year and startdate.month <= now.month:
                        months = list(range(startdate.month + 1, now.month + 1))
                    for single_month in months:
                        cur_month = str(startdate.year) + '{:02d}'.format(single_month)
                        rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format((cur_month + '*'))
                        scriptout2.write(rsync_cmd2_usm)
                # for all years after that, copy all folders of each year
                if yr > startdate.year:
                    rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format((str(yr) + '*'))
                    scriptout2.write(rsync_cmd2_usm)

        if option == '-e':
            # copy the complete folders of all years
            for yr in years_data:
                rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format((str(yr) + '*'))
                scriptout2.write(rsync_cmd2_usm)

        # add a nice message to indicate the regular end of the sync process
        scriptout2.write('echo "Finished syncing data to USM!"\n')
        print('Sync script for data successfully created!')

    # return the file name of the script that was created for copying etc.
    return pf.data_script_USM


# function for executing sync to USM PC and sync to local machine
def script_local_update(option2):
    msg_pw_USM = 'echo "Please provide the password for the USM machine (ltsp01):"\n'
    msg_sync_to_USM = 'echo "Syncing the {} files to USM HOST machine..."\n'
    msg_sync_to_local = 'echo "Syncing the {} files to the LOCAL machine..."\n'
    with open(pf.script_local, 'w') as scriptout3:
        scriptout3.write('#!/usr/bin/bash\n')
        scriptout3.write('\n')

        if option2 == '-lo' or option2 == '-ld':
            scriptout3.write(msg_sync_to_USM.format('log'))
            scriptout3.write(msg_pw_USM)
            scriptout3.write(cmd4.format(pf.script_USM))
            scriptout3.write(msg_sync_to_local.format('log'))
            scriptout3.write(msg_pw_USM)
            scriptout3.write(cmd3.format('copy_logs/obslog/') + ' ' + str(pf.abs_path_obslog) + '\n')

        if option2 == '-do' or option2 == '-ld':
            scriptout3.write(msg_sync_to_USM.format('data'))
            scriptout3.write(msg_pw_USM)
            scriptout3.write(cmd4.format(pf.script2_USM))
            scriptout3.write(msg_sync_to_local.format('data'))
            scriptout3.write(msg_pw_USM)
            scriptout3.write(cmd3.format('temp_frames/') + ' ' + str(pf.abs_path_data) + '\n')

        # # make data syncing script for single date
        # if option == '-o':
        #     rsync_cmd2_usm = cmd2 + '{} ~/temp_frames\n'.format(str(date))
        #     scriptout2.write(rsync_cmd2_usm)

        scriptout3.write('echo "Finished syncing to local machine!"\n')

    # return the file name of the script that was created for copying etc.
    return pf.file_script_local


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
def script_grep_redmineID(redmine_ID, date, option):
    startdate = dt.datetime.strptime(str(date), '%Y%m%d')
    if startdate < dt.datetime.strptime(str(20190430), '%Y%m%d'):
        print('Warning: The date you chose is before the start of automatic data collection (20190430).')
        startdate = dt.datetime.strptime(str(20190430), '%Y%m%d')
    with open(pf.grep_redID_cmd, 'w') as scriptout5:
        scriptout5.write('#!/usr/bin/bash\n')
        scriptout5.write('\n')
        # get the first line with the column titles of the obslogfiles
        grep_title_cmd = cmd6.format(str(pf.abs_path_obslog), dt.datetime.strftime(startdate, '%Y%m%d')[2:], 'object', str(pf.grep_redID_out))
        scriptout5.write(grep_title_cmd)

        # make script for searching in a single date
        if option == '-o':
            str_expl_date = dt.datetime.strftime(startdate, '%Y%m%d')
            grep_cmd = cmd6.format(str(pf.abs_path_obslog), str_expl_date[2:], redmine_ID, str(pf.grep_redID_out))
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
                        grep_cmd = cmd6.format(str(pf.abs_path_obslog), str_expl_date[2:], redmine_ID,
                                               str(pf.grep_redID_out))
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
                    grep_cmd = cmd6.format(str(pf.abs_path_obslog), str_expl_date[2:], redmine_ID,
                                           str(pf.grep_redID_out))
                    scriptout5.write(grep_cmd)


# script_grep_redmineID('2894', 20200124, '-e')


#
#
# echo
# "copying is done"
