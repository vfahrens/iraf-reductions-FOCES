#!/usr/bin/bash

rm /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
cat /mnt/e/logfiles/observations/logfile.200101 | awk '{if($24=="object|"){print $0}}' >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190609 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190813 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190814 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190815 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190816 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190817 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190818 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190821 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190822 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190823 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190824 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190825 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190826 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190828 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190830 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190831 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190902 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190903 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190904 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190905 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190906 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190907 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190908 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190909 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190910 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190911 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190912 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190913 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190914 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190915 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190916 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190917 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190918 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190919 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190920 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190921 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190922 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190923 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190924 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190925 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190926 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190927 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190928 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190929 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.190930 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191001 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191002 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191003 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191004 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191005 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191006 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191007 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191008 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191009 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191010 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191011 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191012 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191013 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191014 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191015 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191016 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191017 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191018 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191019 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191020 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191021 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191022 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191023 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191025 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191026 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191029 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191030 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191031 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191101 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191102 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191103 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191104 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191105 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191107 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191108 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191109 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191110 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191111 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191112 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191113 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191115 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191116 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191117 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191118 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191119 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191120 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191121 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191122 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191123 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191124 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191125 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191126 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191127 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191128 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191129 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191130 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191201 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191202 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191203 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191204 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191205 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191206 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191207 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191208 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191212 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191213 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191214 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191215 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191216 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191217 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191218 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191219 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191220 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191221 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191222 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191223 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191224 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191225 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191226 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191227 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191228 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191229 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191230 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.191231 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200101 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200103 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200104 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200105 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200106 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200107 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200108 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200109 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200110 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200111 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200112 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200113 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200114 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200115 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200116 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200117 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200118 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200119 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200120 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200121 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200122 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200123 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200124 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200125 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200126 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200127 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200128 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200129 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200130 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200131 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200201 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200202 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200203 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200204 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200205 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200206 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200207 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200208 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200209 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200210 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200211 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200213 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200214 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200215 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200216 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200217 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200218 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200219 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200220 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200221 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200222 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200223 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200224 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200225 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200226 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200227 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200228 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200229 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200301 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200302 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200303 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200304 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200305 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200530 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200630 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200712 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200713 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200715 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200716 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200809 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
awk -v redmineid=1236 -f /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/scripts/grep_redID.awk /mnt/e/logfiles/observations/logfile.200810 >> /mnt/e/IRAF/iraf-reductions-FOCES/fxcor/output/grep_ID1236.txt
