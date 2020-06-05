#
import os
import numpy as np
import astropy.io.fits as fits

# import statements for other python scripts
import paths_and_files as pf


# extract the single orders from the GAMSE result files, add missing header entries
# and interpolate to log-linear wavelength grid
def iraf_converter(redmine_id):
    # define the folders for reading the data and saving the new files
    path = pf.iraf_data_folder.format(redmine_id)
    pathout = pf.iraf_smd_folder.format(redmine_id)

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
                        new_headyyy['PHYSORD'] = (order, 'Physical order of aperture')
                            

                        # make a new fits file with the header and data BOTH as primary HDU,
                        # because this is what IRAF expects
                        new_fitsiii2 = fits.PrimaryHDU(header=new_headyyy, data=wave)
                        # new_fitsiii2 = fits.PrimaryHDU(header=new_headyyy, data=flux)

                        newname = '{}_ord{:03d}_{}_wave.fits'.format(fname[:-22], order, fiber)
                        # newname = '{}_ord{:03d}_{}_flux.fits'.format(fname[:-22], order, fiber)
                        outname = os.path.join(pathout, newname)
                        new_fitsiii2.writeto(outname)

            else:
                print('Warning: This is a single fiber file: {}. IRAF conversion is not possible (yet).'.format(fname))

    print('IRAF conversion completed.')
    return


iraf_converter('2864_diffthar')
