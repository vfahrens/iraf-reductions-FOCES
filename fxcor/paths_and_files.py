import os
from pathlib import Path

# define the required paths
path_scripts = 'scripts/'
path_output = 'output/'
path_obslog_local = '../../../logfiles/observations'
path_data_local = '../../../FOCES_data'
path_reduce_gamse = '../../../GAMSE'
path_gamse_results = 'red_{}/onedspec'
path_IRAF_datainput = 'data/'

# definition of many filenames
file_script_USM = 'sync_obslogfiles_USM.sh'
data_script_USM = 'sync_datafiles_USM.sh'
file_script_local = 'sync_obslogfiles_local.sh'
data_script_local = 'sync_datafiles_local.sh'
add_header_script = 'add_header_entries.sh'
grep_redmineID_script = 'grep_ID{}.sh'
grep_redmineID_results = 'grep_ID{}.txt'
sort_copy_gamse_script = 'copy_ID{}_to_gamse.sh'
sort_gamse_results = 'sort_ID{}_for_gamse.txt'
copy_dates_gamse = 'copy_ID{}_to_gamse.txt'
copy_wvcal_script = 'copy_wvcal_ID{}_to_IRAF.sh'

# initialize all paths and make them platform independent
location = Path(__file__).parent
abs_path_scripts = (location / path_scripts).resolve()
abs_path_output = (location / path_output).resolve()
abs_path_obslog = (location / path_obslog_local).resolve()
abs_path_data = (location / path_data_local).resolve()
abs_path_red_gamse = (location / path_reduce_gamse).resolve()
abs_path_IRAF = (location / path_IRAF_datainput).resolve()

# make absolute paths to the files
script_USM = os.path.join(abs_path_scripts, file_script_USM)
script2_USM = os.path.join(abs_path_scripts, data_script_USM)
script_local = os.path.join(abs_path_scripts, file_script_local)
script2_local = os.path.join(abs_path_scripts, data_script_local)
script_add = os.path.join(abs_path_scripts, add_header_script)
grep_redID_cmd = os.path.join(abs_path_scripts, grep_redmineID_script)
grep_redID_out = os.path.join(abs_path_output, grep_redmineID_results)
sort_copy_cmd = os.path.join(abs_path_scripts, sort_copy_gamse_script)
copy_reduced_cmd = os.path.join(abs_path_scripts, copy_wvcal_script)
out_gamse_sorted = os.path.join(abs_path_output, sort_gamse_results)
out_gamse_copy = os.path.join(abs_path_output, copy_dates_gamse)

# other paths
path_test_redult = os.path.join(abs_path_red_gamse, path_gamse_results.format('20200304'))
file_test_result = os.path.join(path_test_redult, 'whatever.fits')