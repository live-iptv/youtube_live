import requests
import re

print('#EXTM3U')  # M3U file header

# Create a persistent session
s = requests.Session()

# Custom headers to mimic Postman
headers = {
    'User-Agent': 'PostmanRuntime/7.46.0',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br'
}

# Read and process the channel info file
with open('../youtube_channel_info_malayalam.txt') as f:
    for line in f:
        line = line.strip()

        # Skip empty lines or commented lines
        if not line or line.startswith('~~'):
            continue

        # Metadata line (channel name | group | logo | id)
        if not line.startswith('https:'):
            try:
                ch_name, grp_title, tvg_logo, tvg_id = [x.strip() for x in line.split('|')]
                grp_title = grp_title.title()  # Capitalize group title

                # Print EXTINF metadata for the playlist
                print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
            except ValueError:
                print(f"# Skipping invalid metadata line: {line}")
                continue

        # Link line (should be a video/channel/page URL)
        else:
            try:
                # Send HTTP GET request
                response = s.get(line, headers=headers, timeout=15).text

                # Extract first .m3u8 link using regex
                m3u8_links = re.findall(r'https://[^"]+\.m3u8', response)

                if m3u8_links:
                    link = m3u8_links[0]
                else:
                    # Fallback if no link found
                    link = 'https://live-iptv.github.io/youtube_live/assets/info.m3u8'

            except Exception as e:
                # Handle timeout or other errors gracefully
                link = 'https://live-iptv.github.io/youtube_live/assets/info.m3u8'

            print(link)
