# spotify-playlist-downloader
It's a simple script that scrapes all important metadata from spotify playlist, downloads it from youtube and embeds metadata and cover art from spotify using ffmpeg without need to add an app to your spotify account.
## INSTALL
```
git clone https://github.com/ObronnaSosna/spotify-playlist-downloader.git
cd spotify-playlist-downloader
pip3 install -r requirements.txt
sudo apt install ffmpeg wget
```
You need to have youtube-dl, wget and ffmpeg in your PATH
## USAGE
```
python3 spd.py <playlist id>
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
