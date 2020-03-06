import os
import datetime as dt
import shutil

# import statements for other python scripts
import paths_and_files as pf


# distinguish between logfile and comment file paths, filenames and years
def get_category():
    now = dt.datetime.now()
    # create a list with all years from when FOCES data exist
    years_log = list(range(2016, now.year + 1))
    years_comm = list(range(2018, now.year + 1))

    dif_files = ['log', 'comments']
    years_list = []
    directory = []
    file1 = []
    for cat in dif_files:
        # check whether to use the log or comments year list
        if cat == 'log':
            years_list.append(years_log)
            directory.append('log')
            file1.append('logfile')
        if cat == 'comments':
            years_list.append(years_comm)
            directory.append('comments')
            file1.append('comments')

    return years_list, directory, file1


# extract all nights with observation data for a specific redmine project and write the dates to a file
def get_obsnights(redmine_id):
    dates_for_red = []
    # extract all observation night dates for this project
    with open(pf.grep_redID_out.format(redmine_id), 'r') as grepfile:
        with open(pf.out_gamse_sorted.format(redmine_id), 'w') as datefile:
            for line in grepfile:
                # remove whitespaces in the beginning and end of the string
                line = line.strip()
                # remove whitespaces inside the string
                line = line.replace(' ', '')
                # split the string into its single entries
                line = line.split('|')
                if line[0][0] != '#':
                    # extract the individual observation dates from the grep results
                    file_time = dt.datetime.strptime(line[0][4:18], '%Y%m%d%H%M%S')
                    folder_date = dt.datetime.strftime(file_time, '%Y%m%d')
                    day_before = file_time - dt.timedelta(days=1)
                    str_day_before = dt.datetime.strftime(day_before, '%Y%m%d')
                    if file_time.hour > 12 and folder_date not in dates_for_red:
                        dates_for_red.append(folder_date)
                        datefile.write(folder_date + '\n')
                    elif file_time.hour <= 12 and str_day_before not in dates_for_red:
                        dates_for_red.append(str_day_before)
                        datefile.write(str_day_before + '\n')
    return


# read the dates that should be used in GAMSE from a file
def get_reductiondates(redmine_id):
    red_dates = []
    for line in open(pf.out_gamse_copy.format(redmine_id), 'r'):
        line = line.strip()
        red_dates.append(line)
    return red_dates


# automatically copy the (sorted) wavelength calibrated data to the IRAF folder
def script_copy_reduced_data(redmine_id):
    total_files_copied = 0
    # check if a folder with this redmine ID exists already in IRAF data input
    iraf_data_folder = os.path.join(pf.abs_path_IRAF, 'ID{}'.format(redmine_id))
    if not os.path.exists(str(iraf_data_folder)):
        os.makedirs(str(iraf_data_folder))
    # read the results from the grep command
    with open(pf.grep_redID_out.format(redmine_id), 'r') as grepfile:
        for line in grepfile:
            # remove whitespaces in the beginning and end of the string
            line = line.strip()
            # remove whitespaces inside the string
            line = line.replace(' ', '')
            # split the string into its single entries
            line = line.split('|')
            if line[0][0] != '#':
                # extract the name of each file from the grep results
                file_name = line[0]
                file_time = dt.datetime.strptime(line[0][4:18], '%Y%m%d%H%M%S')

                # get the correct date for the night of observation
                folder_date = dt.datetime.strftime(file_time, '%Y%m%d')
                if file_time.hour <= 12:
                    day_before = file_time - dt.timedelta(days=1)
                    str_day_before = dt.datetime.strftime(day_before, '%Y%m%d')
                    folder_date = str_day_before
                # get the path of the .tab file corresponding to the .fits file
                data_folder_path = os.path.join(pf.abs_path_data, folder_date)
                tab_file_path = os.path.join(data_folder_path, file_name + '.tab')

                # from the .tab file extract the correct link name of the raw frame
                with open(tab_file_path, 'r') as tabfile:
                    for line in tabfile:
                        if 'LINKNAME' in line:
                            line = line.strip()
                            line = line.split('=')
                            raw_name = line[1]

                # generate the file name for the reduced frame and copy it
                red_name = raw_name[:-5] + '_ods.fits'
                gamse_red_folder = os.path.join(pf.abs_path_red_gamse, 'red_' + folder_date)
                gamse_result_folder = os.path.join(gamse_red_folder, 'onedspec')
                result_file_path = os.path.join(gamse_result_folder, red_name)
                shutil.copy(result_file_path, iraf_data_folder)
                total_files_copied += 1
    print('Successfully copied {} files!'.format(total_files_copied))

    return
