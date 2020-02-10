#
import os
import sys
import logging

logger = logging.getLogger(__name__)
import configparser

import numpy as np
import astropy.io.fits as fits
from pathlib import Path
from datetime import datetime
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

# from ..utils.obslog import read_obslog, find_log
# from ..utils.misc   import write_system_info
# from . import foces


###############################
# give the path to the input and output files as relative path
path_to_infiles = 'data/51Peg/'
path_to_outfiles = 'data/51Peg_time/'
# # for quick tests:
# path_to_infiles = "../file_parser/testfiles/"
# path_to_outfiles = '../file_parser/testfiles/testout/'

location = Path(__file__).parent
path = (location / path_to_infiles).resolve()
pathout = (location / path_to_outfiles).resolve()

# check if the output directory exists, create if it does not
if not os.path.exists(pathout):
    os.makedirs(pathout)

objcoord_ra = '22:57:28.00'
objcoord_dec = '+20:46:07.82'
CCD_readtime = 89.0


fname_lst = sorted(os.listdir(path))
prev_frameid = 0
for fname in fname_lst:
    if fname[-5:] != '.fits':
        continue
    else:
        print(fname)

    # open one of the GAMSE fits files
    # with fits.open("samples/20191019_0110_FOC1903_SCC2_ods.fits") as datei:
    with fits.open((path / fname).resolve()) as datei:
        # show what the content of the file looks like
        print(datei.info())
        # read the header and the data into variables
        headyyy = datei[0].header
        datennn = datei[1].data
        # print the exposure time from the header
        print(headyyy['EXPOSURE'])
        print("----------------------------------------")


    # make a new header entry (2 different ways)
    # headyyy['TESTENT'] = 'This is something new.'
    # headyyy.set('TESTENT2', 'This is something more new.')
    # print the header in a nicely readable form
    # print(repr(headyyy))

    # show different things about the fits file data section
    # print(datennn.shape)
    # print(datennn[-3])
    # print(datennn.columns.info())

    # open the GAMSE fits file and read the data section into the data variable
    # data = fits.getdata("samples/20191019_0110_FOC1903_SCC2_ods.fits")
    data = fits.getdata((path / fname).resolve())

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
                # ATTENTION: the timestamp iin the header is the time when the file is saved, after exposure and readout
                exp_endtime = datetime.strptime(headyyy['FRAME'], '%Y-%m-%dT%H:%M:%S.%f')
                exp_midtime = exp_endtime - 0.5*dt.timedelta(seconds=headyyy['EXPOSURE']) - dt.timedelta(seconds=CCD_readtime)

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
                new_headyyy["RA"] = (objcoord_ra, "Right ascension coordinate")
                new_headyyy["DEC"] = (objcoord_dec, "Declination coordinate")
                new_headyyy["EQUINOX"] = (2000.0, "Epoch of observation")
                new_headyyy["UTMID"] = (datetime.isoformat(exp_midtime), "UT of midpoint of observation")

                # # convert the header to a (primary) HDU object
                # new_headyyy_HDU = fits.PrimaryHDU(header=new_headyyy)
                # # put the wavelength and flux data into a Binary Table
                # col_wave = fits.Column(name='wavelength', format='D', array=wave)
                # col_flux = fits.Column(name='flux', format='D', array=flux)
                # collies = fits.ColDefs([col_wave, col_flux])
                # new_datennn = fits.BinTableHDU.from_columns(collies)

                # # make a new fits file with the new header as primary and data as BinTable HDU
                # new_fitsiii = fits.HDUList([new_headyyy_HDU, new_datennn])
                # # new_fitsiii.writeto('output/new_fits_test_ord{:03d}_{}.fits'.format(order, fiber))

                # make a new fits file with the header and data BOTH as primary HDU, because this is what IRAF expects
                new_fitsiii2 = fits.PrimaryHDU(header=new_headyyy, data=flux_interpol)

                newname = '{}_ord{:03d}_{}_lin_IRAF.fits'.format(fname[:-5], order, fiber)
                new_fitsiii2.writeto((pathout / newname).resolve())
                #
                # figname = '{}_ord{:03d}_{}_lin_IRAF.png'.format(fname[:-5], order, fiber)
                # plt.plot(wave, flux, 'o')
                # plt.plot(wave_lin, flux_interpol, '-x')
                # plt.savefig((pathout / figname).resolve())
                # plt.close()

    else:
        print("Warning: this is a single fiber file: {}".format(fname))
