FOR %%A in (tmp/song*) DO ffmpeg.exe -i tmp/%%A -i tmp/thumb.jpg -map 0:0 -map 1:0 -id3v2_version 3 -y -metadata title=%1 -metadata artist=%2 -metadata album=%3 -b:a 320k %4
