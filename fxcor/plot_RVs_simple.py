import os
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

import paths_and_files as pf


id_string = 'ID2908'
id_string2 = 'ID2894'
results_folder = os.path.join(pf.abs_path_output, id_string)
results_folder2 = os.path.join(pf.abs_path_output, id_string2)
RV_file_path = os.path.join(results_folder, 'RVs_time_weighted_200309.txt')
RV_file_path2 = os.path.join(results_folder2, 'RVs_time_weighted_200309.txt')

dates = []
RVs = []
RVerr = []
this_list = []
dates2 = []
RVs2 = []
RVerr2 = []
this_list2 = []

with open(RV_file_path) as RVfile:
    for line in RVfile:
        line = line.strip()
        line = line.split()
        this_list.append(line)

nicely = sorted(this_list, key=itemgetter(0))
nicely2 = np.transpose(nicely)
dates = nicely2[0]
RVs = nicely2[1]
RVerr = nicely2[2]

dates_fl = []
RVs_fl = []
RVerr_fl = []
for i in dates:
    dates_fl.append(float(i))
for j in RVs:
    RVs_fl.append(float(j))
for k in RVerr:
    RVerr_fl.append(float(k))


with open(RV_file_path2) as RVfile2:
    for line in RVfile2:
        line = line.strip()
        line = line.split()
        this_list2.append(line)

nicely_2 = sorted(this_list2, key=itemgetter(0))
nicely2_2 = np.transpose(nicely_2)
dates2 = nicely2_2[0]
RVs2 = nicely2_2[1]
RVerr2 = nicely2_2[2]

dates_fl2 = []
RVs_fl2 = []
RVerr_fl2 = []
for i in dates2:
    dates_fl2.append(float(i))
for j in RVs2:
    RVs_fl2.append(float(j))
for k in RVerr2:
    RVerr_fl2.append(float(k))


# plot the RVs
x = np.arange(len(RVs_fl))
x2 = np.arange(len(RVs_fl2))
fig = plt.figure()
plt.errorbar(x, RVs_fl, yerr=RVerr_fl, fmt='o', label='upsAnd', alpha=0.5)
plt.errorbar(x2, RVs_fl2, yerr=RVerr_fl2, fmt='o', label='HD9407', alpha=0.5)
# plt.hlines(rv_weightmean, [0], len(x), lw=2)
plt.xlabel('# of observation')
plt.ylabel('RV in m/s')
plt.legend()
# plt.show()
plt.savefig('plot_RV_notime.pdf')

# plot the RVs
fig = plt.figure()
plt.errorbar(dates_fl, RVs_fl, yerr=RVerr_fl, fmt='o', label='upsAnd', alpha=0.5)
plt.errorbar(dates_fl2, RVs_fl2, yerr=RVerr_fl2, fmt='o', label='HD9407', alpha=0.5)
# plt.hlines(rv_weightmean, [0], len(x), lw=2)
plt.xlabel('date of observation')
plt.ylabel('RV in m/s')
plt.legend()
# plt.show()
plt.savefig('plot_RV_time.pdf')




