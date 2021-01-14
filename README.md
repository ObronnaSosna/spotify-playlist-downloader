# spotify-playlist-downloader
It's a simple script that scrapes all important metadata from spotify playlist, downloads it from youtube and embeds metadata and cover art from spotify using ffmpeg without need to add an app to your spotify account.
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
4. Put ffmpeg.exe in script directory
```
pip install -r requirements.txt
```
## USAGE
### Linux
```
python3 spd.py <playlist id>
```
### Windows
```
py spd_win.py <playlist id>
```
It will create directory in your current directory with downloaded files named "playlist id", log file named "playlist id".log and tmp directory.
On subsequent runs it will download only new songs (not in "playlist id".log)
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
