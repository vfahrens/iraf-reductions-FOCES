#!/usr/bin/bash

rm /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
cat /mnt/e/logfiles/observations/logfile.200901 | awk '{if($24=="object|"){print $0}}' >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200901 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200902 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200903 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200904 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200905 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200906 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200907 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200908 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200909 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200910 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
awk -v redmineid=2864 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200911 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2864.txt
