#!/usr/bin/bash

rm /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2908.txt
cat /mnt/e/logfiles/observations/logfile.190910 | awk '{if($24=="object|"){print $0}}' >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2908.txt
awk -v redmineid=2908 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190910 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID2908.txt
