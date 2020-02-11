rm ~/copy_logs/*
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.190923 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.190924 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.190925 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.190926 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.190927 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.190928 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.190929 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.190930 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.1910* ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.1911* ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/logfile.1912* ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/ ~/copy_logs/obslog
echo "Finished syncing to USM!"
