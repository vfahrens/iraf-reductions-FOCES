#!/usr/bin/bash

rsync -av foces@195.37.68.140:/data/fcs_links/20200220 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200221 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200222 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200223 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200224 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200225 ~/temp_frames
echo "Finished syncing data to USM!"
