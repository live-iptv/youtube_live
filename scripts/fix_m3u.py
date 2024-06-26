import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def fix_m3u_from_url(url):
    # Fetch the M3U file content from the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the M3U file from the URL. Status code: {response.status_code}")
        return

    lines = response.text.split('\n')

    # Extract URLs with associated information
    entries = []
    current_entry = None

    for line in lines:
        if line.startswith('#EXTINF:-1'):
            match = re.search(r'#EXTINF:-1(.*?),(.+)', line)
            if match:
                attributes = match.group(1)
                # Extract individual attributes
                group_title_match = re.search(r'group-title="([^"]*)"', attributes)
                group_title = group_title_match.group(1) if group_title_match else 'Others'
                
                tvg_logo_match = re.search(r'tvg-logo="([^"]*)"', attributes)
                tvg_logo = tvg_logo_match.group(1) if tvg_logo_match else ''
                
                name = match.group(2).strip()
                current_entry = {
                    'group_title': group_title,
                    'tvg_logo': tvg_logo,
                    'name': name,
                }
        elif current_entry is not None:
            current_entry['url'] = line.strip()
            entries.append(current_entry)
            current_entry = None

    def is_url_reachable(entry):
        try:
            url_response = requests.head(entry['url'], timeout=5)
            if url_response.status_code == 200:
                return entry
        except requests.RequestException:
            print(f"")
        return None

    # Verify if URLs are reachable concurrently
    reachable_entries = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_entry = {executor.submit(is_url_reachable, entry): entry for entry in entries}
        for future in as_completed(future_to_entry):
            result = future.result()
            if result is not None:
                reachable_entries.append(result)

    # Sort entries based on group title
    sorted_entries = sorted(reachable_entries, key=lambda x: x['group_title'])

    # Write the sorted M3U content
    sorted_m3u_content = []
    for entry in sorted_entries:
        sorted_m3u_content.append(f'#EXTINF:-1 group-title="{entry["group_title"]}" tvg-logo="{entry["tvg_logo"]}",{entry["name"]}\n{entry["url"]}')

    # Display or save the fixed M3U content
    print('#EXTM3U')
    for line in sorted_m3u_content:
        print(line)

if __name__ == "__main__":
    m3u_url = 'https://raw.githubusercontent.com/manisat30/Sat/main/DSC.m3u'
    fix_m3u_from_url(m3u_url)
