import os
from pathlib import Path
import sys

path_scripts = 'scripts/'
file_script_USM = 'sync_obslogfiles_USM.sh'

location = Path(__file__).parent
abs_path_scripts = (location / path_scripts).resolve()
script_USM = os.path.join(abs_path_scripts, file_script_USM)

years = [2016, 2017, 2018, 2019, 2020]
cmd1 = 'rsync -av wstobserver@195.37.68.19:/data/3kk/log/'

def script_update(option, date):
    with open(script_USM, 'w') as scriptout1:
        scriptout1.write('rm ~/copy_logs/*\n')
        if option == '-o':
            rsync_cmd_USM = cmd1 + '{}/logfile.{} ~/copy_logs\n'.format(str(date)[:4], str(date))
            scriptout1.write(rsync_cmd_USM)

        if option == '-a':
            for yr in years:
                ## hier fehlt noch die Behandlung vom laufenden Jahr
                # if yr == date[:4]:
                #     rsync_cmd_USM = cmd1 + '{}/logfile.{} ~/copy_logs\n'.format(str(yr))
                #     scriptout1.write(rsync_cmd_USM)
                if yr > date[:4]:
                    rsync_cmd_USM = cmd1 + '{}/ ~/copy_logs\n'.format(yr)
                    scriptout1.write(rsync_cmd_USM)
            print('Dummy do!')

        if option == '0':
            for yr in years:
                rsync_cmd_USM = cmd1 + '{}/ ~/copy_logs\n'.format(yr)
                scriptout1.write(rsync_cmd_USM)

        scriptout1.write('echo "Finished syncing to USM!"\n')

script_update('0', 20190903)


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
