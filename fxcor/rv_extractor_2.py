import os
import numpy as np
import matplotlib.pyplot as plt

###############################
# User definitions
path = "data/51Peg_time/" 
###############################

outname_lst = []

with os.scandir(path) as it:
    for entry in it:
        # if the file name contains fxcor_result
        if entry.name.rfind('fxcor_result.txt') != -1 and entry.is_file():
            # fname_lst.append(entry.name)

            # extract the RVs from the IRAF fxcor report files
            with open(path + entry.name) as file:
                with open(path + '{}_rv_allorders.txt'.format(entry.name[:13]), 'w') as outfile:
                    outname_lst.append(path + '{}_rv_allorders.txt'.format(entry.name[:13]))
                    for line in file:
                        line = str.split(line)
                        if len(line) == 13 and line[0].rfind('_A_lin_IRAF.fits') != -1 and line[2] != 'INDEF' \
                                and line[11] != 'INDEF':
                            # print(line[0], line[11], line[12])
                            rv_output = line[2] + ' ' + line[11] + ' ' + line[12] + '\n'
                            outfile.write(rv_output)

with open(path + '{}_RVs_weighted.txt'.format(path[:-1]), 'w') as final_out:
    dates = []
    means = []
    stddev = []


    for allrv_file in outname_lst:
        # calculate the weighted mean and stddev of that for each frame
        rvdata = np.loadtxt(allrv_file)
        dates.append(rvdata[0, 0])
        rv_weightmean = np.average(rvdata[40:-11, 1], weights=(1/np.abs(rvdata[40:-11, 2])))
        # rv_weightmean = np.average(rvdata[:, 1], weights=(1/np.abs(rvdata[:, 2])))
        means.append(rv_weightmean * 1000.)  # convert from km/s to m/s
        rv_stddev = np.std(rvdata[:, 1])
        stddev.append(rv_stddev * 1000.)  # convert from km/s to m/s

        # plot the RVs per order for each frame
        x = np.arange(len(rvdata[40:-11, 1]))
        fig = plt.figure()
        plt.errorbar(x, rvdata[40:-11, 1], yerr=rvdata[40:-11, 2])
        plt.hlines(rv_weightmean, [0], len(x), lw=2)
        plt.show()

    # write the results to a file
    outarray = np.array([dates, means, stddev])
    outarray = np.transpose(outarray)
    np.savetxt(path + '{}_RVs_weighted_trunc.vels'.format(path[:-1]), outarray)



