import paths_and_files as pf
# import radvel
from matplotlib import pyplot as pl
from argparse import ArgumentParser
import os


def plot_test(x, y, num_planets):
    pl.scatter(x, y)



location = '/mnt/e/IRAF/iraf-reductions-FOCES/fxcor/rv_results/'  # Path(__file__).parent
# path_rv_results = 'rv_results/'
# abs_path_rvout = (location / path_rv_results).resolve()
nonrv_data_file = os.path.join(location, 'nonRVs_ID2864.txt')
nonrvdat = []
nonrvtimes = []
with open(nonrv_data_file)as nonrvfile:
    for line in nonrvfile:
        if len(line) > 0:
            line = line.strip()
            line = line.split(' ')
            nonrvdat.append(float(line[0]))
            nonrvtimes.append(float(line[1]))

n_plan = 3


plot_test(nonrvdat, nonrvtimes, n_plan)


pl.show()

