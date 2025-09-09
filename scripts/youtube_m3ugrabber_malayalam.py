import requests
import re

print('#EXTM3U')
s = requests.Session()
headers = {
    'User-Agent': 'PostmanRuntime/7.36.3',
    'Cookie': 'GPS=1; VISITOR_INFO1_LIVE=3RZ8w7ZfbwY; VISITOR_PRIVACY_METADATA=CgJJThIEGgAgIg%3D%3D; YSC=yfv3133jOhg; __Secure-ROLLOUT_TOKEN=CPbMm7iincnhAxCAgMuh38uPAxiAgMuh38uPAw%3D%3D'
}

with open('../youtube_channel_info_malayalam.txt') as f:
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
            response = s.get(line, headers=headers, timeout=15).text
            m3u8_links = re.findall(r'https://[^"]+\.m3u8', response)
            if m3u8_links:
                link = m3u8_links[0] 
            else:
                link = 'https://live-iptv.github.io/youtube_live/assets/info.m3u8'                    
            print(link)
            