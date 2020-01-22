#
import os
import sys
import logging

logger = logging.getLogger(__name__)
import configparser

import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

# from ..utils.obslog import read_obslog, find_log
# from ..utils.misc   import write_system_info
# from . import foces


###############################
path = "data/51Peg/"


fname_lst = sorted(os.listdir(path))
prev_frameid = 0
for fname in fname_lst:
    if fname[-5:] != '.fits':
        continue
    else:
        print(fname)


    # open one of the GAMSE fits files
    # with fits.open("samples/20191019_0110_FOC1903_SCC2_ods.fits") as datei:
    with fits.open(path + fname) as datei:
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
    data = fits.getdata(path + fname)

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

                # make a header for the new fits file
                new_headyyy = headyyy
                new_headyyy["CRPIX1"] = ("1.", "Reference pixel")
                # get the starting wavelength of the current order
                start_wl = wave[0]
                new_headyyy["CRVAL1"] = (start_wl, "Coordinate at reference pixel")
                # calculate the step size of the current order
                wl_step = (wave[-1]-wave[0])/int(headyyy["HIERARCH GAMSE WLCALIB FIBER {} NPIXEL".format(fiber)])
                new_headyyy["CDELT1"] = (wl_step, "Coord.incr.per pixel(original value)")
                # add some more useful header entries
                new_headyyy["CTYPE1"] = ('                ', 'Units of coordinate')
                new_headyyy["BUNIT"] = ('                ', 'Units of data values')
                new_headyyy["DATAMAX"] = (str(np.max(flux)), "Maximum data value")
                new_headyyy["DATAMIN"] = (str(np.min(flux)), "Minimum data value")

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
                new_fitsiii2 = fits.PrimaryHDU(header=new_headyyy, data=flux)
                new_fitsiii2.writeto('output/{}_ord{:03d}_{}_IRAF.fits'.format(fname[:-5], order, fiber))

    else:
        print("Warning: this is a single fiber file: {}".format(fname))
