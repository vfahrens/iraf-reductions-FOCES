#!/usr/bin/bash

echo "Syncing the log and comment files to USM HOST machine..."
echo "Please provide the password for the USM machine (ltsp01):"
ssh fahrenschon@ltsp01.usm.uni-muenchen.de "bash -s" < /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/sync_obslogfiles_USM.sh
echo "Syncing the log and comment files to the LOCAL machine..."
echo "Please provide the password for the USM machine (ltsp01):"
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/copy_logs/obslog/*.200222 /mnt/e/logfiles/observations
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/copy_logs/obslog/*.200223 /mnt/e/logfiles/observations
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/copy_logs/obslog/*.200224 /mnt/e/logfiles/observations
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/copy_logs/obslog/*.200225 /mnt/e/logfiles/observations
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/copy_logs/obslog/*.200226 /mnt/e/logfiles/observations
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/copy_logs/obslog/*.200227 /mnt/e/logfiles/observations
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/copy_logs/obslog/*.200228 /mnt/e/logfiles/observations
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/copy_logs/obslog/*.200229 /mnt/e/logfiles/observations
rsync -avu fahrenschon@ltsp01.usm.uni-muenchen.de:/home/moon/fahrenschon/copy_logs/obslog/*.2003* /mnt/e/logfiles/observations
