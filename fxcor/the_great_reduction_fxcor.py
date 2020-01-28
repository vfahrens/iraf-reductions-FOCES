#!/usr/bin/env python3
# makes file executable from shell without the "python3" command in front

import os
import sys
import subprocess
import re  # module for regular expressions

# Welcome message for the user
print('Hello! I see you want to reduce some data.')

# check whether an update of the data and logfiles is needed
yn_update = input('Do you want to update the data and logfile directories? ')

# if update is needed, execute shell scripts
# regular expressions: check if string starts with y/j (re.I = ignore case)
if re.match(r'^y', yn_update, re.I) or re.match(r'^j', yn_update, re.I):
    date_restrict = input('Do you want to specify a date? (options: start-end, a = after, b = before)\n')
    # subprocess.call('bash', 'whateverscript.sh')
    print('Working...')
else:
    print('No files were updated.')
