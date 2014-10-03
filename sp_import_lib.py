#!/usr/bin/env python

# env vars need to be set for oauth token
# export SPOTIPY_CLIENT_ID='your-spotify-client-id'
# export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
# export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

import sys
import spotipy
import spotipy.util as util
import json

if len(sys.argv) >= 3:
  username = sys.argv[1]
  json_lib_file = sys.argv[2]
else:
  print "Usage: %s <username> <json library to import> [-n]" % (sys.argv[0],)
  sys.exit()

dry_run = False
if len(sys.argv) >= 4:
  dry_run = True if sys.argv[3] == '-n' else False

lib_file = open(json_lib_file, 'r')

scope = 'user-library-modify'

token = util.prompt_for_user_token(username, scope)

if token:
  sp = spotipy.Spotify(auth=token)

  artist_albums = json.loads(lib_file.read())

  found_albums = []

  for artist, album_list in artist_albums.iteritems():
    result = sp.search(q='artist:'+artist, type='album')

    album_set = set([ s.lower() for s in album_list])

    for album_dict in result['albums']['items']:
      album_name = album_dict['name'].lower()

      if (album_name in album_set):
        #print "Found album '{0}' for artist {1}".format(album_name, artist)
        album_set.remove(album_name)
        found_albums.append(album_dict)

    if (len(album_set) != 0):
      print "Could not find albums {0} for artist {1}".format(album_set, artist)

  for album_dict in found_albums:
    id = album_dict['id']
    tracks = sp.album_tracks(id)
  
    track_ids = []
    for track in tracks['items']:
      track_ids.append(track['id'])

    if (not dry_run) and (len(track_ids) > 0):
      print "Adding track ids {0} for album {1}".format(track_ids, album_dict['name'])
      sp.current_user_saved_tracks_add(track_ids)
else:
  print "Can't get token for", username

