#!/usr/bin/env python3
# makes file executable from shell without the "python3" command in front

import os
import sys
import subprocess
import re  # module for regular expressions

# import other scripts and stuff
import shell_script_maker as shesm
# from shell_script_maker import script_logs_update, script_data_update, script_local_update, script_USM


# Welcome message for the user
print('Hello! I see you want to reduce some data.')
print(str(shesm.abs_path_scripts))

# check whether an update of the data and logfiles is needed
yn_update = input('Do you want to update the data and logfile directories? ')

# if update is needed, execute shell scripts
# regular expressions: check if string starts with y/j (re.I = ignore case)
if re.match(r'^y', yn_update, re.I) or re.match(r'^j', yn_update, re.I):
    # ask the user for the desired date and options
    print('Please specify a date:')
    date_restrict = input('(yyyymmdd; option1: -a = after, -o = only, -e = everything; '
                          'option2: -lo = logs/comments only, -do = data frames only, -ld = both)\n')
    # split the input into its parts
    in_date = date_restrict[:8]
    in_opt1 = date_restrict[-6:-4]
    in_opt2 = date_restrict[-3:]

    # create a script for syncing the desired dates
    if re.search(r'-lo', date_restrict, re.I):
        file_script_USM = shesm.script_logs_update(in_date, in_opt1)
        subprocess.call(['dos2unix', str(shesm.script_USM)])
    if re.search(r'-do', date_restrict, re.I):
        data_script_USM = shesm.script_data_update(in_date, in_opt1)
        subprocess.call(['dos2unix', str(shesm.script2_USM)])
    if re.search(r'-ld', date_restrict, re.I):
        file_script_USM = shesm.script_logs_update(in_date, in_opt1)
        data_script_USM = shesm.script_data_update(in_date, in_opt1)
        subprocess.call(['dos2unix', str(shesm.script_USM)])
        subprocess.call(['dos2unix', str(shesm.script2_USM)])
    file_script_local = shesm.script_local_update(in_opt2)
    subprocess.call(['dos2unix', str(shesm.script_local)])
    print('Successfully created bash scripts. Starting to sync now...')

    subprocess.call(['bash', str(shesm.script_local)])

    # # scp to remote machine not needed with new ssh syntax
    # scp_copy_location = 'fahrenschon@ltsp01.usm.uni-muenchen.de:~/scripts/'
    # # securely copy the scripts to ltsp01
    # print('Please provide your password for ltsp01:')
    # subprocess.call(['scp', 'scripts/' + file_script_USM, scp_copy_location + file_script_USM])
    # subprocess.call(['scp', 'scripts/' + data_script_USM, scp_copy_location + data_script_USM])

    # # regular expressions: search the whole string if an option is present
    # if re.search(r'-a', date_restrict, re.I):
    #     #subprocess.call('bash', 'whateverscript.sh')
    #     print('Working...')
else:
    print('No files were updated.')
