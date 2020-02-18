#!/usr/bin/bash

mkdir -p ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.20200122 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.20200122 ~/copy_logs/obslog
echo "Finished syncing logs to USM!"
