#!/usr/bin/env python3

import json, requests
from sys import argv
from os import system

playlist_id = argv[1]

# get token as if we were webplayer
token = requests.get(
    "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
).text
token = json.loads(token)
headers = {"Authorization": "Bearer " + token["accessToken"]}

data = []

# spotify api only allows 100 tracks at once so this workaround is necessary
for a in range(0, 5000, 100):

    # get 100 tracks and parse it
    result = json.loads(
        requests.get(
            "https://api.spotify.com/v1/playlists/"
            + str(playlist_id)
            + "/tracks?offset="
            + str(a)
            + "&limit=100",
            headers=headers,
        ).text
    )

    if len(result["items"]) > 0:
        for i in result["items"]:
            track_name = i["track"]["name"]
            artists_names = " & ".join([name["name"] for name in i["track"]["artists"]])
            album_name = i["track"]["album"]["name"]
            duration_min = int(i["track"]["duration_ms"]) / 1000 / 60
            disc_number = i["track"]["disc_number"]
            track_number = i["track"]["track_number"]
            explicit = i["track"]["explicit"]
            release_date = i["track"]["album"]["release_date"]
            spotify_id = i["track"]["id"]
            added_at = i["added_at"]
            added_by = i["added_by"]["id"]

            # some songs don't have thumbnail for some reason so this prevents script from crashing when song without thumbnail is encountered
            try:
                thumbnail_link = i["track"]["album"]["images"][0]["url"]
            except:
                thumbnail_link = "not found"

            data.append(
                [
                    track_name,
                    artists_names,
                    album_name,
                    duration_min,
                    release_date,
                    disc_number,
                    track_number,
                    explicit,
                    added_by,
                    added_at,
                    spotify_id,
                    thumbnail_link,
                ]
            )
    else:
        break

system("mkdir tmp")
try:  # try reading .log file create new if does not exist
    f = open(argv[1] + ".log", "r")
    songs_logged = f.read().splitlines()
    f = open(argv[1] + ".log", "a")
except:
    f = open(argv[1] + ".log", "a")
    songs_logged = []
    system(
        "mkdir " + argv[1]
    )  # try creating download directory if .log file does not exist

for i in data:  # loopt through songs
    spotify_id = i[10]
    if spotify_id not in songs_logged:  # check if not already downloaded
        title = (
            i[0].replace("'", "").replace('"', "")
        )  # assign variables remove symbols that break filepaths
        artist = i[1].replace("'", "").replace('"', "")
        album = i[2].replace("'", "").replace('"', "")
        thumb = i[11]
        system('del /S /Q tmp\*')#clear temp
        system(  # download song from youtube
            'youtube-dl -x --no-continue "ytsearch1: '
            + artist
            + " "
            + title
            + '" -o tmp/song.%(ext)s'
        )
        open("tmp/thumb.jpg", "wb").write(  # download thumbnail
            requests.get(thumb, allow_redirects=True).content
        )
        system(
            'ffmpeg_script "'
            + title
            + '" "'
            + artist
            + '" "'
            + album
            + '" "'
            + playlist_id
            + "/"
            + title
            + "_"
            + spotify_id
            + '.mp3"'
        )
    f.write(spotify_id + "\n")
f.close()
