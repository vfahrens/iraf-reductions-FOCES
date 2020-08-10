import astropy.io.fits as fits


# open one of the GAMSE fits files
with fits.open("samples/20191019_0110_FOC1903_SCC2_ods.fits") as datei:
    # show what the content of the file looks like
    print(datei.info())
    # read the header and the data into variables
    headyyy = datei[0].header
    datennn = datei[1].data
    # print the exposure time from the header
    print(headyyy['EXPOSURE'])
    print("----------------------------------------")

# open Roberto's sample fits file and check how that looks
with fits.open("samples/junk.fits") as datei2:
    head1 = datei2[0].header
    print(datei2.info())
    # print(repr(head1))
    print("----------------------------------------")

# check the file info of the new fits file
with fits.open("output/new_fits_test_ord128_A.fits") as datei:
    print(datei.info())

# check the file info of the new fits file
with fits.open("output/new_fits_test2_ord128_A.fits") as datei:
    head1 = datei[0].header
    print(datei.info())
    print(repr(head1))
    print("----------------------------------------")

# check the file info of McDonald data
with fits.open("samples/20180504_0075_lss_0_cr_r90_fl_sc_ex_wv.fits") as datei:
    head1 = datei[0].header
    print(datei.info())
    # print(repr(head1))
    print("----------------------------------------")