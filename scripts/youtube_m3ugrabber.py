#! /usr/bin/python3

import requests
import os
import sys
import re

print('#EXTM3U')
s = requests.Session()
with open('../youtube_channel_info.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
            print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
        else:
            response = s.get(line, timeout=15).text
            print(response)
            m3u8_links = re.findall(r'https://[^"]+\.m3u8', response)
            if m3u8_links:
                link = m3u8_links[0] 
            else:
                link = 'https://live-iptv.github.io/youtube_live/assets/info.m3u8'                    
            print(link)
            
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
