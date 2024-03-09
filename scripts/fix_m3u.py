import re
import requests

def fix_m3u_from_url(url):
    # Fetch the M3U file content from the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the M3U file from the URL. Status code: {response.status_code}")
        return

    lines = response.text.split('\n')

    # Extract URLs with associated information
    entries = []
    for i in range(0, len(lines) - 1, 2):
        if lines[i].startswith('#EXTINF:'):
            match = re.search(r'#EXTINF:-1 (.+?),(.+)', lines[i])
            if match:
                attributes_str = match.group(1)
                name = match.group(2)
                url = lines[i + 1].strip()

                # Extract individual attributes
                group_title = re.search(r'group-title="([^"]*)"', attributes_str).group(1) if re.search(r'group-title="([^"]*)"', attributes_str) else ''
                tvg_logo = re.search(r'tvg-logo="([^"]*)"', attributes_str).group(1) if re.search(r'tvg-logo="([^"]*)"', attributes_str) else ''
                tvg_id = re.search(r'tvg-id="([^"]*)"', attributes_str).group(1) if re.search(r'tvg-id="([^"]*)"', attributes_str) else ''

                entries.append((group_title, tvg_logo, tvg_id, name, url))

    # Sort entries based on name
    sorted_entries = sorted(entries, key=lambda x: x[3])

    # Write the sorted M3U content
    sorted_m3u_content = []
    for group_title, tvg_logo, tvg_id, name, url in sorted_entries:
        sorted_m3u_content.append(f'#EXTINF:-1 group-title="{group_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}",{name}\n{url}\n')

    # Display or save the fixed M3U content
    for line in sorted_m3u_content:
        print(line)

if __name__ == "__main__":
    m3u_url = 'https://raw.githubusercontent.com/manisat30/Sat/main/BALAVIDEO.m3u'
    fix_m3u_from_url(m3u_url)
