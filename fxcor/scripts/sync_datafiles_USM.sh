#!/usr/bin/bash

rsync -av foces@195.37.68.140:/data/fcs_links/20200215 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200216 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200217 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200218 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200219 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200220 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200221 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200222 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200223 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200224 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200225 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200226 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200227 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200228 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/20200229 ~/temp_frames
rsync -av foces@195.37.68.140:/data/fcs_links/202003* ~/temp_frames
echo "Finished syncing data to USM!"
