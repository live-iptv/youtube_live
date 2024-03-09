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
            match = re.search(r'#EXTINF:-1,(.+)\\n(.+)', lines[i])
            if match:
                name = match.group(1)
                url = lines[i + 1].strip()

                # Extract group-title and tvg-logo, if available
                group_match = re.search(r'group-title="([^"]*)"', lines[i])
                group_title = group_match.group(1) if group_match else ''

                logo_match = re.search(r'tvg-logo="([^"]*)"', lines[i])
                tvg_logo = logo_match.group(1) if logo_match else ''

                entries.append((name, url, group_title, tvg_logo))

    # Sort entries based on name
    sorted_entries = sorted(entries, key=lambda x: x[0])

    # Write the sorted M3U content
    sorted_m3u_content = []
    for name, url, group_title, tvg_logo in sorted_entries:
        sorted_m3u_content.append(f'#EXTINF:-1 tvg-logo="{tvg_logo}" group-title="{group_title}",{name}\n{url}\n')

    # Display or save the fixed M3U content
    for line in sorted_m3u_content:
        print(line)

if __name__ == "__main__":
    m3u_url = 'https://raw.githubusercontent.com/manisat30/Sat/main/BALAVIDEO.m3u'
    fix_m3u_from_url(m3u_url)
