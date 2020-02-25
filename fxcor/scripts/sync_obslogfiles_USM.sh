#!/usr/bin/bash

mkdir -p ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.200220 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.200221 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.200222 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.200223 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.200224 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/log/2020/logfile.200225 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.200220 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.200221 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.200222 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.200223 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.200224 ~/copy_logs/obslog
rsync -av wstobserver@195.37.68.19:/data/3kk/comments/2020/comments.200225 ~/copy_logs/obslog
echo "Finished syncing logs to USM!"
