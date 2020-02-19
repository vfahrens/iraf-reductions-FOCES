#!/usr/bin/env python3
# makes file executable from shell without the "python3" command in front

import os
import sys
import subprocess
import re  # module for regular expressions
import datetime as dt

# import statements for other python scripts
import shell_script_maker as shesm
import paths_and_files as pf


in_date = dt.datetime.strftime(dt.datetime.now(), '%Y%m%d')
in_opt1 = '-o'
in_opt2 = '-ld'

# Welcome message for the user
print('Hello! I see you want to reduce some data.')

# check whether an update of the data and logfiles is needed
print('\n')
yn_update = input('Do you want to update the data and logfile directories? ')

# if update is needed, execute shell scripts
# regular expressions: check if string starts with y/j (re.I = ignore case)
if re.match(r'^y', yn_update, re.I) or re.match(r'^j', yn_update, re.I):
    # ask the user for the desired date and options
    print('\n')
    print('Please enter "today" or specify a date:')
    date_restrict = input('(yyyymmdd; option1: -a = after, -o = only, -e = everything; '
                          'option2: -lo = logs/comments only, -do = data frames only, -ld = both)\n')
    if date_restrict != 'today':
        # split the input into its parts
        in_date = date_restrict[:8]
        in_opt1 = date_restrict[-6:-4]
        in_opt2 = date_restrict[-3:]

    # create a script for syncing the desired dates
    if re.search(r'-lo', date_restrict, re.I):
        file_script_USM = shesm.script_logs_update(in_date, in_opt1)
        subprocess.call(['dos2unix', str(pf.script_USM)])
    if re.search(r'-do', date_restrict, re.I):
        data_script_USM = shesm.script_data_update(in_date, in_opt1)
        subprocess.call(['dos2unix', str(pf.script2_USM)])
    if re.search(r'-ld', date_restrict, re.I):
        file_script_USM = shesm.script_logs_update(in_date, in_opt1)
        data_script_USM = shesm.script_data_update(in_date, in_opt1)
        subprocess.call(['dos2unix', str(pf.script_USM)])
        subprocess.call(['dos2unix', str(pf.script2_USM)])
    file_script_local = shesm.script_local_update(in_opt2)
    subprocess.call(['dos2unix', str(pf.script_local)])
    print('Successfully created bash scripts. Starting to sync now...')

    subprocess.call(['bash', str(pf.script_local)])

    # check whether an update of the data file headers is needed
    print('\n')
    yn_header = input('Do you also want to update the data file headers? ')
    if re.match(r'^y', yn_header, re.I) or re.match(r'^j', yn_header, re.I):
        script_add = shesm.script_add_radec(in_date, in_opt1)
        subprocess.call(['dos2unix', str(pf.script_add)])
        print('Starting to update the headers now...')
        subprocess.call(['bash', str(pf.script_add)])

else:
    print('No files were updated.')

# ask if the data should be sorted for a specific observation project
print('\n')
yn_sortproject = input('Do you want to get the data of a specific redmine project? ')

if re.match(r'^y', yn_sortproject, re.I) or re.match(r'^j', yn_sortproject, re.I):
    print('\n')
    redmine_id = input('Please provide the desired redmine project ID: ')
    shesm.script_grep_redmineID(redmine_id)

