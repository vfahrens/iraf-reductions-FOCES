import os
import numpy as np
import matplotlib.pyplot as plt

import paths_and_files as pf


id_string = 'ID2894'
results_folder = os.path.join(pf.abs_path_output, id_string)
RV_file_path = os.path.join(results_folder, 'RVs_time_weighted.txt')

dates = []
RVs = []
RVerr = []

with open(RV_file_path) as RVfile:
    for line in RVfile:
        line = line.strip()
        line = line.split()
        dates.append(float(line[0]))
        RVs.append(float(line[1]))
        RVerr.append(float(line[2]))

# plot the RVs
x = np.arange(len(RVs))
fig = plt.figure()
plt.errorbar(x, RVs, yerr=RVerr)
# plt.hlines(rv_weightmean, [0], len(x), lw=2)
# plt.show()
plt.savefig('plot_RV_notime.pdf')

# plot the RVs
fig = plt.figure()
plt.errorbar(dates, RVs, yerr=RVerr)
# plt.hlines(rv_weightmean, [0], len(x), lw=2)
# plt.show()
plt.savefig('plot_RV_time.pdf')

