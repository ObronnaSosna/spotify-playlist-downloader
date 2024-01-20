# spotify-playlist-downloader
It's a simple script that scrapes all important metadata from spotify playlist, downloads it from youtube and embeds metadata and cover art from spotify using ffmpeg without need to add an app to your spotify account.
## NOTE
At the time I didn't know about existence of [spotDL/spotify-downloader](https://github.com/spotDL/spotify-downloader), which does pretty much everything that this script does, but it's much better written and supported, you probably want to use that instead.
## INSTALL
### Linux
```
sudo apt install ffmpeg python3 python3-pip git
git clone https://github.com/ObronnaSosna/spotify-playlist-downloader.git
cd spotify-playlist-downloader
pip3 install -r requirements.txt
```
You need to have youtube-dl and ffmpeg in your PATH
### Windows
1. Download this repo
2. Install [python](https://www.python.org/downloads/)
3. Download [ffmpeg](https://ffmpeg.org/download.html)
4. Download [youtube-dl](http://ytdl-org.github.io/youtube-dl/download.html)
5. Put ffmpeg.exe and youtube-dl.exe in script directory
```
py -m pip install -r requirements.txt

```
## USAGE
### Linux
```
python3 spd.py <playlist id or link>
```
### Windows
```
py spd.py <playlist id or link>
```
It will create directory in your current directory with downloaded files named "playlist id", log file named "playlist id".log and tmp directory.
On subsequent runs it will download only new songs (not in "playlist id".log)
## Options
```
-o, --output - set output directory
-l, --log - set log directory
--tmp - set tmp directory
--dry-run - get playlist info and don't download anything
--no-log - don't use log file (no incremental updates)
--no-metadata - don't embed metadata
--long-filenames - filenames with artists and song title
--non-unique-filenames - filenames without spotify id
--dump-json - prints spotify api response after running
--no-watermark - don't add link to this script in comment
--ffmpeg-path - path to ffmpeg
--youtube-dl-path - path to youtube-dl
```
## Using with other programs
You can use this script with shell programs for getting playlist info by running it with --dry-run --dump-json.
--dump-json without --no-log prints differences between log file and spotify api. 
You can also import this script and use getPlaylistSongs(playlist_id) from python scripts for this.
## Using with cron
You need to set --ffmpeg-path, --youtube-dl-path, --tmp, -o and -l in command that crontab is running.
Example crontab entry for ubuntu:
```
0 0 * * * /usr/bin/python3 <script path>/spotify-playlist-downloader/spd.py <playlist id> --o <script path>/spotify-playlist-downloader/ -l <script path>/spotify-playlist-downloader/ --tmp <script path>/spotify-playlist-downloader/tmp/ --ffmpeg-path /usr/bin/ffmpeg --youtube-dl-path /home/<user>/.local/bin/youtube-dl
```
## How to get playlist id
You can get playlist id from share link in spotify app. Id is everything after playlist/ and before ?si
For example in:
```
https://open.spotify.com/user/spotifycharts/playlist/37i9dQZEVXbMDoHDwVN2tF?si=Dd2q7nM4SC6w_En1zy85_w
```
id is
```
37i9dQZEVXbMDoHDwVN2tF
```

- Kunal Kushwaha says this community is amazing 
- Rutvik Shinde says git is amazing 