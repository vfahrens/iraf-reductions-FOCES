import os
from pathlib import Path
import sys
import datetime as dt
import calendar

# define the required paths and filenames
path_scripts = 'scripts/'
file_script_USM = 'sync_obslogfiles_USM.sh'

# initialize all paths and filenames and make them platform independent
location = Path(__file__).parent
abs_path_scripts = (location / path_scripts).resolve()
script_USM = os.path.join(abs_path_scripts, file_script_USM)

# create a list with all years from when FOCES data exist
now = dt.datetime.now()
years = list(range(2016, now.year + 1))
# standard command for rsync from ohiaai to USM PC
cmd1 = 'rsync -av wstobserver@195.37.68.19:/data/3kk/log/'


def script_update(date, option):
    with open(script_USM, 'w') as scriptout1:
        scriptout1.write('rm ~/copy_logs/*\n')

        # make logfile syncing script for single date
        if option == '-o':
            rsync_cmd_usm = cmd1 + '{}/logfile.{} ~/copy_logs/obslog\n'.format(str(date)[:4], str(date))
            scriptout1.write(rsync_cmd_usm)

        # make logfile syncing script starting with specific date
        if option == '-a':
            startdate = dt.datetime.strptime(str(date), '%Y%m%d')
            for yr in years:
                ## hier fehlt noch die Behandlung vom laufenden Jahr
                if yr == startdate.year:
                    # handle the rest of the starting month
                    startmonth = str(startdate.year) + str('{:02d}').format(startdate.month)
                    # add all days that are still left from the starting month
                    end_of_month = calendar.monthrange(yr, startdate.month)[1]
                    days = list(range(startdate.day, end_of_month + 1))
                    # add a rsync command for all individual days of the starting month
                    for single_day in days:
                        rsync_cmd_usm = cmd1 + '{}/logfile.{} ~/copy_logs/obslog\n'.format(yr, (startmonth[2:] + str(single_day)))
                        scriptout1.write(rsync_cmd_usm)
                    # handle the other months of the starting year
                    months = list(range(startdate.month + 1, 13))
                    for single_month in months:
                        cur_month = str(startdate.year)[2:] + str('{:02d}').format(single_month)
                        rsync_cmd_usm = cmd1 + '{}/logfile.{} ~/copy_logs/obslog\n'.format(yr, (cur_month + '*'))
                        scriptout1.write(rsync_cmd_usm)
                    print(months)
                #     rsync_cmd_USM = cmd1 + '{}/logfile.{} ~/copy_logs\n'.format(str(yr))
                #     scriptout1.write(rsync_cmd_usm)
                if yr > startdate.year:
                    rsync_cmd_usm = cmd1 + '{}/ ~/copy_logs/obslog\n'.format(yr)
                    scriptout1.write(rsync_cmd_usm)
            print('Dummy do!')

        if option == '-e':
            for yr in years:
                rsync_cmd_usm = cmd1 + '{}/ ~/copy_logs/obslog\n'.format(yr)
                scriptout1.write(rsync_cmd_usm)

        scriptout1.write('echo "Finished syncing to USM!"\n')


script_update(20190923, '-a')


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
