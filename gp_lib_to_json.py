#!/usr/bin/env python

import json
from gmusicapi import Mobileclient

class SetEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj,set):
      return list(obj)
    return json.JSONEncoder.default(self, obj)

if len(sys.argv) >= 3:
  username = sys.argv[1]
  app_passwd= sys.argv[2]
else:
  print "Usage: %s <username> <app password> [-n]" % (sys.argv[0],)
  sys.exit()

api = Mobileclient()

logged_in = api.login(username, app_passwd)

if (not logged_in):
  print "could not log in"
  exit(1)

song_gen = api.get_all_songs(incremental=True)

artist_albums = {}

for songs in song_gen:
  for song in songs:
    if (song['artist'] in artist_albums):
      artist_albums[song['artist']].add(song['album'])
    else:
      artist_albums[song['artist']] = set([song['album']])

print json.dumps(artist_albums, cls=SetEncoder, indent=2)

api.logout()
