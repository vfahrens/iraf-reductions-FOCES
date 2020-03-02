#!/usr/bin/bash

echo "Syncing the log files to USM HOST machine..."
echo "Please provide the password for the USM machine (ltsp01):"
ssh fahrenschon@ltsp01.usm.uni-muenchen.de "bash -s" < /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/sync_obslogfiles_USM.sh
echo "Syncing the log files to the LOCAL machine..."
echo "Please provide the password for the USM machine (ltsp01):"
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/copy_logs/obslog/ /mnt/e/logfiles/observations
echo "Syncing the data files to USM HOST machine..."
echo "Please provide the password for the USM machine (ltsp01):"
ssh fahrenschon@ltsp01.usm.uni-muenchen.de "bash -s" < /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/sync_datafiles_USM.sh
echo "Syncing the data files to the LOCAL machine..."
echo "Please provide the password for the USM machine (ltsp01):"
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/temp_frames/ /mnt/e/FOCES_data
echo "Finished syncing to local machine!"
