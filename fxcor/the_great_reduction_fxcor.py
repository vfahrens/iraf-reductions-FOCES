#!/usr/bin/env python3
# makes file executable from shell without the "python3" command in front

import os
import sys
import subprocess
import re  # module for regular expressions

# import other scripts and stuff
from shell_script_maker import script_logs_update, script_data_update


# Welcome message for the user
print('Hello! I see you want to reduce some data.')

# check whether an update of the data and logfiles is needed
yn_update = input('Do you want to update the data and logfile directories? ')

# if update is needed, execute shell scripts
# regular expressions: check if string starts with y/j (re.I = ignore case)
if re.match(r'^y', yn_update, re.I) or re.match(r'^j', yn_update, re.I):
    # ask the user for the desired date and options
    date_restrict = input('Please specify a date: (yyyymmdd; options: -a = after, -o = only, -e = everything)\n')
    # create a script for syncing the desired dates
    file_script_USM = script_logs_update(date_restrict[:8], date_restrict[-2:])
    data_script_USM = script_data_update(date_restrict[:8], date_restrict[-2:])
    scp_copy_location = 'fahrenschon@ltsp01.usm.uni-muenchen.de:~/scripts/'
    # securely copy the scripts to ltsp01
    print('Please provide your password for ltsp01:')
    subprocess.call(['scp', 'scripts/' + file_script_USM, scp_copy_location + file_script_USM])
    subprocess.call(['scp', 'scripts/' + data_script_USM, scp_copy_location + data_script_USM])
    print('Success!')

    # # regular expressions: search the whole string if an option is present
    # if re.search(r'-a', date_restrict, re.I):
    #     #subprocess.call('bash', 'whateverscript.sh')
    #     print('Working...')
else:
    print('No files were updated.')