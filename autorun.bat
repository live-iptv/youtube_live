pip install requests

cd scripts/
python youtube_m3ugrabber.py > ../youtube.m3u

python youtube_m3ugrabber_malayalam.py > ../malayalam.m3u

python youtube_m3ugrabber_tamil.py > ../tamil.m3u

python youtube_m3ugrabber_kids.py > ../kids.m3u

python youtube_m3ugrabber_sports.py > ../sports.m3u

python fix_m3u.py > ../fix_m3u.m3u
