import os
from pathlib import Path
import sys
import datetime as dt
import calendar

# define the required paths and filenames
path_scripts = 'scripts/'
file_script_USM = 'sync_obslogfiles_USM.sh'
data_script_USM = 'sync_datafiles_USM.sh'

# initialize all paths and filenames and make them platform independent
location = Path(__file__).parent
abs_path_scripts = (location / path_scripts).resolve()
script_USM = os.path.join(abs_path_scripts, file_script_USM)
script2_USM = os.path.join(abs_path_scripts, data_script_USM)

# create a list with all years from when FOCES data exist
now = dt.datetime.now()
years_log = list(range(2016, now.year + 1))
years_comm = list(range(2018, now.year + 1))
# list of years where data is available in fcs_links
years_data = list(range(2019, now.year + 1))
# standard command for rsync from ohiaai to USM PC
cmd1 = 'rsync -av wstobserver@195.37.68.19:/data/3kk/{}/'
# standard command for rsync from FOCES PC to USM PC
cmd2 = 'rsync -av foces@195.37.68.140:/data/fcs_links/'
dif_files = ['log', 'comments']


def script_data_update(date, option):
    startdate = dt.datetime.strptime(str(date), '%Y%m%d')
    if startdate < dt.datetime.strptime(str(20190430), '%Y%m%d'):
        print('Warning: The date you chose is before the start of automatic data collection (20190430).')
    with open(script2_USM, 'w') as scriptout2:
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
    return data_script_USM


def script_logs_update(date, option):
    with open(script_USM, 'w') as scriptout1:
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
    return file_script_USM


# script_data_update(20180324, '-e')


#
#
# echo "Syncing the logfiles to USM host machine..."
#
# echo
# "Please provide the password for the USM machine (ltsp01):"
# ssh
# fahrenschon @ ltsp01.usm.uni - muenchen.de
# "bash ~/scripts/sync_TempPressLogs.sh"
#
# echo
# "Syncing the logfiles to the local machine..."
# echo
# "Please provide the password for the USM machine (ltsp01) again:"
# rsync - av
# fahrenschon @ ltsp01.usm.uni - muenchen.de: ~ / copy_logs / *.log / mnt / c / Users / Vanessa / Documents / work / FOCES_instrumentation / TempPressLogs / logfiles
# echo
# "copying is done"
