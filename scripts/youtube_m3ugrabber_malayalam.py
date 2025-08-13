import requests
import re

print('#EXTM3U')
s = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
            