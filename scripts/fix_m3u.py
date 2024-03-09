import re
import requests

def fix_m3u_from_url(url):
    # Fetch the M3U file content from the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the M3U file from the URL. Status code: {response.status_code}")
        return

    lines = response.text.split('\n')

    # Extract group titles and URLs
    entries = []
    current_group = None
    for line in lines:
        if line.startswith('#EXTINF:'):
            match = re.search(r'group-title="([^"]+)"', line)
            if match:
                current_group = match.group(1)
            else:
                current_group = 'Uncategorized'
        elif line.startswith('http'):
            entries.append((current_group, line.strip()))

    # Group and sort entries
    grouped_entries = {}
    for group, url in entries:
        if group not in grouped_entries:
            grouped_entries[group] = []
        grouped_entries[group].append(url)

    # Write the sorted M3U content
    sorted_m3u_content = []
    for group in sorted(grouped_entries.keys()):
        for url in sorted(grouped_entries[group]):
            sorted_m3u_content.append(f'{url} tvg-logo="" group-title="{group}",name="{group}"')

    # Display or save the fixed M3U content
    for line in sorted_m3u_content:
        print(line)

if __name__ == "__main__":
    m3u_url = 'https://raw.githubusercontent.com/manisat30/Sat/main/BALAVIDEO.m3u'
    fix_m3u_from_url(m3u_url)
