mkdir -p ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.200215 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.200216 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.200217 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.200218 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.200215 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.200216 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.200217 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.200218 ~/copy_logs/obslog
echo "Finished syncing logs to USM!"
