"""
This script uses python-mpd2 library to show
current queue and file being played
"""

MPD_HOST = "localhost"
MPD_PORT = 6600

import os
import socket
import tornado.template

from mpd import MPDClient

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

client = MPDClient()
client.timeout = 10
try:
    client.connect(MPD_HOST, MPD_PORT)
    all_tracks = client.playlistinfo()
    cur_track = client.currentsong()
    client.disconnect()

    for i in range(0, len(all_tracks)):
        all_tracks[i]['time'] = '%d:%02d' % (int(all_tracks[i]['time'])/60, int(all_tracks[i]['time'])%60)
    with open(os.path.join(ROOT_DIR, 'mpd_queue.html'), 'r') as fp:
        print(tornado.template.Template(fp.read()).generate(tracks=all_tracks, current=cur_track))

except socket.error:
    print("MPD coulnd't be connected")
