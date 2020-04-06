#!/usr/bin/bash

echo "Syncing the data files to USM HOST machine..."
echo "Please provide the password for the USM machine (ltsp01):"
ssh fahrenschon@ltsp01.usm.uni-muenchen.de "bash -s" < /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/sync_datafiles_USM.sh
echo "Syncing the data files to the LOCAL machine..."
echo "Please provide the password for the USM machine (ltsp01):"
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/temp_frames/20191016 /mnt/e/FOCES_data
