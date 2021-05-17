#!/usr/bin/env python3

import json
import requests
from sys import argv
import os
import argparse


def getPlaylistSongs(playlist_id):
    # get token as if we were webplayer
    token = requests.get(
        "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
    ).text
    token = json.loads(token)
    headers = {"Authorization": "Bearer " + token["accessToken"]}

    songs = []

    # spotify api only allows 100 tracks at once so this workaround is necessary
    for offset in range(0, 5000, 100):

        # get 100 tracks and parse it
        result = json.loads(
            requests.get(
                "https://api.spotify.com/v1/playlists/"
                + str(playlist_id)
                + "/tracks?offset="
                + str(offset)
                + "&limit=100",
                headers=headers,
            ).text
        )

        if len(result["items"]) > 0:
            for i in result["items"]:
                try:
                    songs.append(
                        {
                            "track_name": i["track"]["name"],
                            "artists_names": " & ".join(
                                [name["name"] for name in i["track"]["artists"]]
                            ),
                            "album_name": i["track"]["album"]["name"],
                            "duration_min": int(i["track"]["duration_ms"]) / 1000 / 60,
                            "release_date": i["track"]["album"]["release_date"],
                            "disc_number": i["track"]["disc_number"],
                            "track_number": i["track"]["track_number"],
                            "explicit": i["track"]["explicit"],
                            "added_by": i["added_by"]["id"],
                            "added_at": i["added_at"],
                            "spotify_id": i["track"]["id"],
                            "thumbnail_link": i["track"]["album"]["images"][0]["url"],
                        }
                    )
                except:
                    pass
        else:
            break
    return songs


class PlaylistIdError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_id", help="Spotify playlist id")
    parser.add_argument("--tmp", nargs="?", default="tmp", help="tmp directory")
    parser.add_argument(
        "--dry-run", action="store_true", help="get data and don't download anything"
    )
    parser.add_argument(
        "--dump-json", action="store_true", help="prints json recieved from spotify api"
    )
    parser.add_argument(
        "-o", "--output", nargs="?", default=".", help="output directory"
    )
    parser.add_argument("-l", "--log", nargs="?", default=".", help="log directory")
    parser.add_argument("--no-log", action="store_true", help="don't use log file")
    parser.add_argument(
        "--long-filenames",
        action="store_true",
        help="filenames with artists names and song titles",
    )
    parser.add_argument(
        "--non-unique-filenames",
        action="store_true",
        help="don't append spotify id to filename",
    )
    parser.add_argument(
        "--no-watermark",
        action="store_true",
        help="do not add link to this script in comment",
    )
    parser.add_argument(
        "--no-metadata", action="store_true", help="no metadata in output files"
    )
    args = parser.parse_args()

    if "https://open.spotify.com/playlist/" in args.playlist_id:
        playlist_id = args.playlist_id[34:56]
    else:
        playlist_id = args.playlist_id
    if len(playlist_id) != 22:
        raise PlaylistIdError(
            "given link or id is wrong, if you've passed link try passing id"
        )
    tmp_path = args.tmp
    out_path = args.output
    log_path = args.log
    no_log = args.no_log
    no_metadata = args.no_metadata
    no_watermark = args.no_watermark
    dump_json = args.dump_json
    dry_run = args.dry_run
    long_filenames = args.long_filenames
    non_unique = args.non_unique_filenames

    # create tmp directory if not exist
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    # create output directory if not exist
    if not dry_run:
        if not os.path.exists(out_path):
            os.makedirs(out_path)

    # create directory with playlist
    if not dry_run:
        if not os.path.exists(os.path.join(out_path, playlist_id)):
            os.makedirs(os.path.join(out_path, playlist_id))

    if not no_log:
        # create log directory if not exist
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        f = open(os.path.join(log_path, playlist_id + ".log"), "a+")
        f.seek(0)
        songs_logged = f.read().splitlines()
    else:
        songs_logged = []

    songs = getPlaylistSongs(playlist_id)

    # loop through songs
    for song in songs:
        spotify_id = song["spotify_id"]
        # check if not already downloaded
        if spotify_id not in songs_logged:
            # assign variables remove symbols that break filepaths
            title = song["track_name"].replace("'", "").replace('"', "")
            artist = song["artists_names"].replace("'", "").replace('"', "")
            album = song["album_name"].replace("'", "").replace('"', "")
            thumb = song["thumbnail_link"]
            added_at = song["added_at"]
            added_by = song["added_by"]
            explicit = song["explicit"]
            year = song["release_date"]
            track_number = song["track_number"]

            if not dry_run:
                # windows has diffrent way of escaping strings
                if os.name == "nt":
                    youtube_dl_options = (
                        ' -x --no-continue "ytsearch1: '
                        + artist
                        + " "
                        + title
                        + '" -o '
                        + os.path.join(tmp_path, "song.%%%(ext%)s")
                    )
                else:
                    youtube_dl_options = (
                        ' -x --no-continue "ytsearch1: '
                        + artist
                        + " "
                        + title
                        + '" -o '
                        + os.path.join(tmp_path, "song.\%\(ext\)s")
                    )
                os.system(
                    "youtube-dl" + youtube_dl_options
                )  # download song from youtube

                if not no_metadata:
                    open(
                        os.path.join(tmp_path, "thumb.jpg"), "wb"
                    ).write(  # download thumbnail
                        requests.get(thumb, allow_redirects=True).content
                    )

                song_filename = [i for i in os.listdir(tmp_path) if "song" in i][0]

                ffmpeg_options = " -i " + os.path.join(tmp_path, song_filename)
                if not no_metadata:
                    ffmpeg_options += (
                        " -i "
                        + os.path.join(tmp_path, "thumb.jpg")
                        + ' -map 0:0 -map 1:0 -id3v2_version 4 -y -metadata title="'
                        + title
                        + '" -metadata artist="'
                        + artist
                        + '" -metadata album="'
                        + album
                        + '" -metadata date="'
                        + year
                        + '" -metadata track="'
                        + str(track_number)
                        + '" -metadata comments="'
                        + "Added by "
                        + added_by
                        + " at "
                        + added_at
                    )
                    if not no_watermark:
                        ffmpeg_options += " Downloaded using https://github.com/ObronnaSosna/spotify-playlist-downloader"
                    ffmpeg_options += '" '

                ffmpeg_options += " -b:a 320k "

                if long_filenames:
                    ffmpeg_options += '"' + os.path.join(
                        out_path,
                        playlist_id,
                        "".join(
                            [
                                c
                                for c in artist + " - " + title
                                if c.isalpha()
                                or c.isdigit()
                                or c == " "
                                or c == "&"
                                or c == "-"
                            ]
                        ).rstrip(),
                    )
                else:
                    ffmpeg_options += '"' + os.path.join(
                        out_path,
                        playlist_id,
                        "".join(
                            [
                                c
                                for c in title
                                if c.isalpha()
                                or c.isdigit()
                                or c == " "
                                or c == "&"
                                or c == "-"
                            ]
                        ).rstrip(),
                    )
                if non_unique:
                    ffmpeg_options += ".mp3" + '"'
                else:
                    ffmpeg_options += "_" + spotify_id + ".mp3" + '"'
                print(ffmpeg_options)
                os.system("ffmpeg " + ffmpeg_options)  # embed and encode everything
                os.remove(os.path.join(tmp_path, song_filename))  # clear tmp
                if not no_metadata:
                    os.remove(os.path.join(tmp_path, "thumb.jpg"))

            if not no_log:
                f.write(spotify_id + "\n")

    if not no_log:
        f.close()

    if no_log and dump_json:
        print(json.dumps(songs))
    elif dump_json:
        print(
            json.dumps(
                [song for song in songs if song["spotify_id"] not in songs_logged]
            )
        )


if __name__ == "__main__":
    main()
