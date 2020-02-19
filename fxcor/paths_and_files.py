import os
from pathlib import Path

# define the required paths and filenames
path_scripts = 'scripts/'
path_output = 'output/'
path_obslog_local = '../../../logfiles/observations'
path_data_local = '../../../FOCES_data'

# definition of many filenames
file_script_USM = 'sync_obslogfiles_USM.sh'
data_script_USM = 'sync_datafiles_USM.sh'
file_script_local = 'sync_obslogfiles_local.sh'
add_header_script = 'add_header_entries.sh'
grep_redmineID_script = 'grep_redID_cmd.sh'
grep_redmineID_results = 'grep_redID_out.txt'

# initialize all paths and make them platform independent
location = Path(__file__).parent
abs_path_scripts = (location / path_scripts).resolve()
abs_path_output = (location / path_output).resolve()
abs_path_obslog = (location / path_obslog_local).resolve()
abs_path_data = (location / path_data_local).resolve()

# make absolute paths to the files
script_USM = os.path.join(abs_path_scripts, file_script_USM)
script2_USM = os.path.join(abs_path_scripts, data_script_USM)
script_local = os.path.join(abs_path_scripts, file_script_local)
script_add = os.path.join(abs_path_scripts, add_header_script)
grep_redID_cmd = os.path.join(abs_path_scripts, grep_redmineID_script)
grep_redID_out = os.path.join(abs_path_output, grep_redmineID_results)

