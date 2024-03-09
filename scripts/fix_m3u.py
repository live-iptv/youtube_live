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
            match = re.search(r'tvg-logo="([^"]+)" group-title="([^"]+)",(.+)', lines[i])
            if match:
                tvg_logo = match.group(1) if match.group(1) else ''
                group_title = match.group(2) if match.group(2) else ''
                name = match.group(3)
                url = lines[i + 1].strip()
                entries.append((tvg_logo, group_title, name, url))

    # Sort entries based on group-title
    sorted_entries = sorted(entries, key=lambda x: x[1])

    # Write the sorted M3U content
    sorted_m3u_content = []
    for tvg_logo, group_title, name, url in sorted_entries:
        sorted_m3u_content.append(f'#EXTINF:-1 tvg-logo="{tvg_logo}" group-title="{group_title}",{name}\n{url}\n')

    # Display or save the fixed M3U content
    for line in sorted_m3u_content:
        print(line)

if __name__ == "__main__":
    m3u_url = 'https://raw.githubusercontent.com/manisat30/Sat/main/BALAVIDEO.m3u'
    fix_m3u_from_url(m3u_url)
