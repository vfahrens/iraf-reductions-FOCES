rm ~/copy_logs/*
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2016/ ~/copy_logs
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2017/ ~/copy_logs
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2018/ ~/copy_logs
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2019/ ~/copy_logs
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/ ~/copy_logs
echo "Finished copying to USM!"
