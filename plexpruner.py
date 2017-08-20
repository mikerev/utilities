#!/usr/bin/env python
import subprocess

# Leveraging GNU find, this will link content downloaded to a specific directory
# to respective directories based on how 'long ago' they were downloaded.

# This can be used with Plex on top of automated torrents via flexget to index
# downloaded content based on how new it is.
# 
# It's structured like so:
# /opt/data/shows main repo for shows downloaded
# /opt/data/today shows downloaded in the last day
# /opt/data/this_week shows downloaded this week
# /opt/data/this_month shows downloaded this month
# /opt/data/this_year shows downloaded this year

schedule = {'today': 1,
            'this_week': 7,
            'this_month': 31,
            'this_year': 365}

file_root = '/opt/data'

filters = "-maxdepth 1 ! -iname 'this_*' ! -iname 'today' ! -iname 'shows'"

for job in schedule:
    prune = 'rm %s/%s/*' % (file_root, job)
    refresh = "find %s/shows %s -mtime -%s -exec ln -s {} %s/%s \;" % (file_root, filters, schedule[job], file_root, job)
    subprocess.call(prune, shell=True)
    subprocess.call(refresh, shell=True)
