#!/usr/bin/env python3

from pathlib import Path
import os
import numpy as np
import astropy.io.fits as fits
from datetime import datetime
import datetime as dt
from astroquery.simbad import Simbad
# import other python scripts
import paths_and_files as pf


# use an already GAMSE reduced frame to get the wavelength borders of each order
def find_order_startend_wl():
    infolder = '/mnt/e/GAMSE/red_20200904/onedspec/'
    fname_lst = ['20200904_0131_FOC1903_SCI0_ods.fits']

    # define the folders for reading the data and saving the new files
    path_in = infolder

    for fname in fname_lst:
        file_in = os.path.join(path_in, fname)

        # open the GAMSE fits file and read the data section
        data = fits.getdata(file_in)

        with open('template_orders_startendwl.txt', 'w') as ordersborders_file:

            # check if the data are single or multi fiber: it is required that the reduction was made with
            # double-fiber configuration, even if the observation was without simultaneous calibration; this is
            # only the case, if the keyword 'fiber' is present in the data frame
            if 'fiber' in data.dtype.names:
                # treat the results of fiber A and B separately and independently
                for fiber in np.unique(data['fiber']):
                    # make a mask that contains all apertures which contain light of either fiber A or B
                    mask = data['fiber'] == fiber

                    # read the data row by row (aperture by aperture)
                    for row in data[mask]:
                        order = row['order']  # physical order of the aperture
                        wave = row['wavelength']  # all wavelength values for the current order (aperture)

                        wl_gamse_start = wave[0]
                        wl_gamse_end = wave[-1]
                        wl_gamse_start_tol = wave[24]
                        wl_gamse_end_tol = wave[-25]

                        wl_templ_start = wl_gamse_start - np.abs(wl_gamse_start - wl_gamse_start_tol)
                        wl_templ_end = wl_gamse_end + np.abs(wl_gamse_end - wl_gamse_end_tol)

                        startend_str = str(order) + ' ' + str(wl_templ_start) + ' ' + str(wl_templ_end) + '\n'
                        ordersborders_file.write(startend_str)

        input('Do you want to cancel? ')

    return


# extract the single orders from the GAMSE result files, add header entries with wavelength calibration information
def harps_template_converter():
    print('Started HARPS template conversion.')

    # define the folders for reading the data and saving the new files
    path_in_templ = '/mnt/e/HARPS_data_51Peg'
    fname_lst_templ = ['harps_mask_G2.dat', 'harps_mask_K5.mas', 'harps_mask_M2.mas']
    path_out_templ = pf.abs_path_output

    for fname_templ in fname_lst_templ:
        file_in_templ = os.path.join(path_in_templ, fname_templ)
        file_out_templ = os.path.join(path_in_templ, fname_templ)

        mask_data = []

        # read the input mask file of HARPS
        with open(file_in_templ, 'r') as mask_infile:
            for line_mask in mask_infile:
                line_mask = line_mask.strip()
                line_mask = line_mask.split()
                # convert the input to a list of floats instead of strings
                mask_vals = [float(val) for val in line_mask]
                mask_data.append(mask_vals)
        # convert to a numpy array for easier data handling
        mask_data = np.array(mask_data)
        mask_data = np.transpose(mask_data)

        # define a dummy value for the midtime of observation
        exp_midtime = datetime.strptime('2010-01-01T00:00:00.0', '%Y-%m-%dT%H:%M:%S.%f')

        # make a new (empty) header for this template file
        head_temp = fits.Header()

        # add ra/dec coordinates to the empty header
        objname = input('Please give the name of the object for a coordinate search with SIMBAD: ')
        radec_table = Simbad.query_object(objname)
        objcoord_ra = radec_table['RA'][0].replace(' ', ':')
        objcoord_dec = radec_table['DEC'][0].replace(' ', ':')
        head_temp['PERA2000'] = (objcoord_ra, 'Right ascension coordinate')
        head_temp['PEDE2000'] = (objcoord_dec, 'Declination coordinate')
        print('Ra/Dec coordinates added to header.')

        head_temp['EQUINOX'] = (2000.0, 'Epoch of observation')
        head_temp['UTMID'] = (datetime.isoformat(exp_midtime), 'UT of midpoint of observation')
        head_temp['FRAME'] = (datetime.isoformat(exp_midtime), 'UT of midpoint of observation')
        head_temp['EXPOSURE'] = (0.0001, 'Exposure time')

        # save the primary header of the MEF file (primary data section is empty)
        empty_primary_temp = fits.PrimaryHDU(header=head_temp)
        hdu_list_temp = fits.HDUList([empty_primary_temp])

        # read the individual order borders from the file
        with open('template_orders_startendwl.txt', 'r') as ordersborders_infile:
            # each line corresponds to a physical order
            for line_b in ordersborders_infile:
                line_b = line_b.strip()
                line_b = line_b.split(' ')
                physord = int(line_b[0])

                # make a new (empty) header for the extensions, add the physical order number
                ext_head_temp = fits.Header()

                # add all the header entries required for the CCF calculation
                ext_head_temp['PERA2000'] = head_temp['PERA2000']
                ext_head_temp['PEDE2000'] = head_temp['PEDE2000']
                ext_head_temp['FRAME'] = head_temp['FRAME']
                ext_head_temp['UTMID'] = head_temp['UTMID']
                ext_head_temp['EXPOSURE'] = head_temp['EXPOSURE']
                ext_head_temp['EQUINOX'] = head_temp['EQUINOX']

                # add the required standard header entries for IRAF wavelength calibration
                ext_head_temp['WCSDIM'] = 2
                ext_head_temp['CTYPE1'] = 'MULTISPE'
                ext_head_temp['CTYPE2'] = 'MULTISPE'
                ext_head_temp['CDELT1'] = 1.
                ext_head_temp['CDELT2'] = 1.
                ext_head_temp['CD1_1'] = 1.
                ext_head_temp['CD2_2'] = 1.
                ext_head_temp['LTM1_1'] = 1.
                ext_head_temp['LTM2_2'] = 1.
                ext_head_temp['WAXMAP01'] = '1 0 0 0 '
                ext_head_temp['WAT0_001'] = 'system=multispec'
                # only this way of writing works with fxcor!
                ext_head_temp['WAT1_001'] = 'wtype=multispec label=Wavelength units=angstroms'
                
                wl_temp_start = float(line_b[1])
                wl_temp_end = float(line_b[2])
                wl_temp_center = (wl_temp_end - wl_temp_start) / 2

                templ_order_chunk = []

                # from the mask data, get the part which is between the start and end wavelength of this order
                templ_order_chunk = np.where((mask_data[0] >= wl_temp_start) & (mask_data[0] <= wl_temp_end))
                templ_order_chunk = np.transpose(templ_order_chunk)

                templ_wave = []
                # if there are no lines in the template for this order, use dummy values to get 1 everywhere
                if len(templ_order_chunk) == 0:
                    templ_wave.append([wl_temp_start, wl_temp_center - 0.00002, 1.0])
                    templ_wave.append([wl_temp_center + 0.00002, wl_temp_end, 1.0])
                # otherwise, take the lines from the template spectrum
                else:
                    for index in range(len(templ_order_chunk)):
                        templ_wave.append([float(mask_data[0][templ_order_chunk][index]),
                                           float(mask_data[1][templ_order_chunk][index]),
                                           float(mask_data[2][templ_order_chunk][index])])

                    # check if there are any "half" lines at the beginning or end of the wavelength range
                    # and add their data to the array, with dummy values for the line start/end wavelength
                    ind_before = int(templ_order_chunk[0]) - 1
                    ind_after = int(templ_order_chunk[-1]) + 1
                    # deal with the special case that the "after" index can be out of range at the end of the mask_data array
                    if ind_after >= len(mask_data[0]):
                        ind_after = len(mask_data[0]) - 1

                    if mask_data[1][ind_before] >= wl_temp_start:
                        templ_wave.insert(0, [0.0, mask_data[1][ind_before], mask_data[2][ind_before]])
                    if mask_data[0][ind_after] <= wl_temp_end:
                        templ_wave.append([mask_data[0][ind_after], 10000.0, mask_data[2][ind_after]])

                # each order has to be stored in a separate extension, so in each extension the
                # data is in aperture 1
                aperture = 1

                wave = []  # this will contain all wavelength values for the current order (aperture)
                flux = []  # this will contain all flux values as given in the HARPS template

                # check where the first spectral line starts and use all information of the first wavelength entry
                # this is if the order starts inside a line
                if templ_wave[0][0] == 0.0:
                    # the first wl data point is inside a line
                    wave.append(wl_temp_start)
                    flux.append(templ_wave[0][2])
                    # the second one is the edge of this line
                    wave.append(templ_wave[0][1])
                    flux.append(templ_wave[0][2])
                    # the third one is a value just outside of the line
                    wave.append(templ_wave[0][1] + 0.00001)
                    flux.append(1.0)
                # this is if the order starts outside of a line
                elif templ_wave[0][0] != 0.0 and templ_wave[0][0] > wl_temp_start:
                    # the first point is somewhere outside a line
                    wave.append(wl_temp_start)
                    flux.append(1.0)
                    # the second one is right at the edge of the line
                    wave.append(templ_wave[0][0] - 0.00001)
                    flux.append(1.0)
                    # then just inside the line
                    wave.append(templ_wave[0][0])
                    flux.append(templ_wave[0][2])
                    # this is the other edge of the line
                    wave.append(templ_wave[0][1])
                    flux.append(templ_wave[0][2])
                    # and finally just outside of that line
                    wave.append(templ_wave[0][1] + 0.00001)
                    flux.append(1.0)
                # this is if the border of the line coincides with the start of the order
                elif templ_wave[0][0] != 0.0 and templ_wave[0][0] == wl_temp_start:
                    # the first value is exactly on the edge of the line
                    wave.append(templ_wave[0][0])
                    flux.append(templ_wave[0][2])
                    # this is the other edge of the line
                    wave.append(templ_wave[0][1])
                    flux.append(templ_wave[0][2])
                    # and finally just outside of that line
                    wave.append(templ_wave[0][1] + 0.00001)
                    flux.append(1.0)

                # add all the lines between the start and the end of this order
                for pnt in range(len(templ_wave) - 2):
                    # we begin with the point just outside of the edge of the line
                    wave.append(templ_wave[pnt + 1][0] - 0.00001)
                    flux.append(1.0)
                    # then just inside the line
                    wave.append(templ_wave[pnt + 1][0])
                    flux.append(templ_wave[pnt + 1][2])
                    # this is the other edge of the line
                    wave.append(templ_wave[pnt + 1][1])
                    flux.append(templ_wave[pnt + 1][2])
                    # and finally just outside of that line
                    wave.append(templ_wave[pnt + 1][1] + 0.00001)
                    flux.append(1.0)

                # now check how to proceed with the end of the order
                # this is if the order ends inside of a line
                if templ_wave[-1][1] == 10000.0:
                    # the first wl data point is just outside a line
                    wave.append(templ_wave[-1][0] - 0.00001)
                    flux.append(1.0)
                    # the second one is the edge of this line
                    wave.append(templ_wave[-1][0])
                    flux.append(templ_wave[-1][2])
                    # the third one is a value inside of the line
                    wave.append(wl_temp_end)
                    flux.append(templ_wave[-1][2])
                elif templ_wave[-1][1] != 10000.0 and templ_wave[-1][0] < wl_temp_end:
                    # the first wl data point is just outside a line
                    wave.append(templ_wave[-1][0] - 0.00001)
                    flux.append(1.0)
                    # the second one is the edge of this line
                    wave.append(templ_wave[-1][0])
                    flux.append(templ_wave[-1][2])
                    # the third one is on the other edge of the line
                    wave.append(templ_wave[-1][1])
                    flux.append(templ_wave[-1][2])
                    # then there is one just outside of the line
                    wave.append(templ_wave[-1][1] + 0.00001)
                    flux.append(1.0)
                    # and the last one is somewhere outside of lines
                    wave.append(wl_temp_end)
                    flux.append(1.0)
                elif templ_wave[-1][1] != 10000.0 and templ_wave[-1][0] == wl_temp_end:
                    # the first wl data point is just outside a line
                    wave.append(templ_wave[-1][0] - 0.00001)
                    flux.append(1.0)
                    # the second one is the edge of this line
                    wave.append(templ_wave[-1][0])
                    flux.append(templ_wave[-1][2])
                    # the third and last one is exactly on the other edge of the line
                    wave.append(templ_wave[-1][1])
                    flux.append(templ_wave[-1][2])

                # add the physical order number to the header
                ext_head_temp['PHYSORD'] = (physord, 'Physical order of aperture')

                # definition of other parameters that IRAF needs for correct interpretation
                # of the wavelength calibration
                dtype = 2  # non-linear dispersion function
                wave1 = wave[0]  # wavelength coordinate of the first pixel
                delta_wave = (wave[-1] - wave[0]) / len(wave)  # average dispersion interval per pixel
                num_pix = len(wave)  # number of valid pixels
                z_corr = 0.  # Doppler correction factor
                aplow = 0.0  # dummy value for the lower aperture extraction limit
                aphigh = 0.0  # dummy value for the upper aperture extraction limit
                weight_i = 1.  # weight of this dispersion function
                zero_off_i = 0.  # zero point offset of this dispersion function
                ftype_i = 5  # pixel coordinate array is used as dispersion information

                # put the whole string together
                wave_str = ''
                wlcalib_str = ''
                separ = ' '
                wave_str = separ.join(str(wl) for wl in wave)  # converts the wave array to a string
                wlcalib_paramlst = [aperture, physord, dtype, wave1, delta_wave, num_pix, z_corr, aplow,
                                    aphigh, weight_i, zero_off_i, ftype_i, num_pix, wave_str]
                wlcalib_str = separ.join(str(item) for item in wlcalib_paramlst)

                longstring = ''
                longstring = 'wtype=multispec spec{} = "{}" '.format(aperture, wlcalib_str)

                # define the keyword for each header entry and fill it with the corresponding
                # part of the long string
                head_key = 'WAT2_{:03d}'
                i = 0
                new_str_start = 0
                for x in range(len(longstring)):
                    i += 1
                    head_key_num = head_key.format(i)
                    # calculate the maximum length of the string in the header
                    longstr_len = 81 - len(head_key_num) - 5

                    # find the right part of the string to write into the header
                    if new_str_start <= len(longstring) \
                            and len(longstring) - new_str_start > 81 - 5 - len(head_key.format(i + 1)):
                        string_part = longstring[new_str_start:new_str_start + longstr_len]
                        new_str_start = new_str_start + longstr_len
                        ext_head_temp[head_key_num] = string_part

                    # at the end of the string, use the rest and leave the for loop
                    else:
                        string_part = longstring[new_str_start:]
                        ext_head_temp[head_key_num] = string_part
                        break

                # convert the flux values to arrays for saving in a FITS file
                flux_np = np.array(flux)

                # create multi-extension FITS files, one for the reduced and one for the raw flux
                image_hdu_fred = fits.ImageHDU(data=flux_np, header=ext_head_temp)
                hdu_list_temp.append(image_hdu_fred)

        # save the new IRAF compatible multi-extension FITS files with the reduced and raw flux
        fname_fred = '20200101_0000_{}_ods_fred.fits'.format(fname_templ[:-4])
        out_fred = os.path.join(path_out_templ, fname_fred)
        hdu_list_temp.writeto(out_fred, overwrite=True)
        print('Saved FITS. ')

    print('IRAF conversion completed.')
    return


harps_template_converter()
# find_order_startend_wl()
