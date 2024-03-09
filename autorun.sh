#!/bin/bash

echo $(dirname $0)

python3 -m pip install requests

cd $(dirname $0)/scripts/

python3 youtube_m3ugrabber.py > ../youtube.m3u

python3 youtube_m3ugrabber_malayalam.py > ../malayalam.m3u

python3 youtube_m3ugrabber_tamil.py > ../tamil.m3u

python3 youtube_m3ugrabber_kids.py > ../kids.m3u

python3 fix_m3u.py > ../fix_m3u.m3u

echo m3u grabbed
