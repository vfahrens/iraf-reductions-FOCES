#
import os
import numpy as np
import astropy.io.fits as fits
from pathlib import Path
from datetime import datetime
import datetime as dt

# import statements for other python scripts
import paths_and_files as pf


# extract the single orders from the GAMSE result files, add missing header entries
# and interpolate to log-linear wavelength grid
def iraf_converter(redmine_id):
    # give the readout time of the camera for the calculation of the mid-time of observation
    CCD_readtime = 87.5

    # define the folders for reading the data and saving the new files
    path = pf.iraf_data_folder.format(redmine_id)
    pathout = pf.iraf_output_folder.format(redmine_id)

    # check if the input directory exists, give a warning if not
    if not os.path.exists(path):
        raise Exception('Input directory not found. Please check the redmine ID or previous reduction steps.')
    # check if the output directory exists, create if it does not
    if not os.path.exists(pathout):
        os.makedirs(pathout)

    # make a list of all files in the input folder
    fname_lst = sorted(os.listdir(path))
    for fname in fname_lst:
        if fname[-5:] != '.fits':
            continue
        else:
            file_in = os.path.join(path, fname)
            # open one of the GAMSE fits files
            with fits.open(file_in) as datei:
                # read the header of the file
                headyyy = datei[0].header

            # open the GAMSE fits file and read the data section into the data variable
            data = fits.getdata(file_in)
            print(headyyy['FRAME'])
            print(type(data))

            # check if the data are single or multi fiber
            if 'fiber' in data.dtype.names:
                # multi fiber
                for fiber in np.unique(data['fiber']):
                    spec = {}
                    mask = data['fiber'] == fiber
                    for row in data[mask]:
                        # read the data row by row
                        order = row['order']
                        wave = row['wavelength']  # this is an array
                        flux = row['flux']  # this is an array

                        # interpolate the spectra to get a linear wavelength space
                        wave_lin = np.linspace(wave[0], wave[-1], len(wave))
                        flux_interpol = np.interp(wave_lin, wave, flux)

                        # calculate the midtime of observation
                        # ATTENTION: the timestamp in the header is the time when the file is saved,
                        # after exposure and readout
                        exp_endtime = datetime.strptime(headyyy['FRAME'], '%Y-%m-%dT%H:%M:%S.%f')
                        exp_midtime = exp_endtime - 0.5*dt.timedelta(seconds=headyyy['EXPOSURE']) - \
                                      dt.timedelta(seconds=CCD_readtime)
                        print(exp_midtime)

                        # make a header for the new fits file
                        new_headyyy = headyyy
                        new_headyyy["PHYSORD"] = (order, "Physical order of aperture")
                        new_headyyy["CRPIX1"] = ("1.", "Reference pixel")

                        # get the starting wavelength of the current order
                        start_wl = wave_lin[0]
                        new_headyyy["CRVAL1"] = (start_wl, "Coordinate at reference pixel")
                        # calculate the step size of the current order
                        wl_step = (wave_lin[-1]-wave_lin[0])/len(wave_lin)
                        new_headyyy["CDELT1"] = (wl_step, "Coord.incr.per pixel(original value)")

                        # add some more useful header entries
                        new_headyyy["CTYPE1"] = ('                ', 'Units of coordinate')
                        new_headyyy["BUNIT"] = ('                ', 'Units of data values')
                        new_headyyy["DATAMAX"] = (str(np.max(flux_interpol)), "Maximum data value")
                        new_headyyy["DATAMIN"] = (str(np.min(flux_interpol)), "Minimum data value")

                        # add ra/dec coordinates to header if not present
                        if 'TESRA' not in new_headyyy:
                            objcoord_ra = '22:57:27.98042'
                            new_headyyy['TESRA'] = (objcoord_ra, 'Right ascension coordinate')
                        if 'TESDEC' not in new_headyyy:
                            objcoord_dec = '+20:46:07.78224'
                            new_headyyy["TESDEC"] = (objcoord_dec, "Declination coordinate")
                            print('Header entry added.')

                        new_headyyy["EQUINOX"] = (2000.0, "Epoch of observation")
                        new_headyyy["UTMID"] = (datetime.isoformat(exp_midtime), "UT of midpoint of observation")

                        # make a new fits file with the header and data BOTH as primary HDU,
                        # because this is what IRAF expects
                        new_fitsiii2 = fits.PrimaryHDU(header=new_headyyy, data=flux_interpol)

                        newname = '{}_ord{:03d}_{}_lin_IRAF.fits'.format(fname[:-5], order, fiber)
                        outname = os.path.join(pathout, newname)
                        new_fitsiii2.writeto(outname)

            else:
                print("Warning: this is a single fiber file: {}".format(fname))

    print('IRAF conversion completed.')
    return