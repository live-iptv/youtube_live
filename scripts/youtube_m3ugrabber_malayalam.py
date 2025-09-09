import subprocess
import re
import sys

print('#EXTM3U')
headers = {
    'User-Agent': 'PostmanRuntime/7.46.0',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br'
}

def curl_request(url):
    """Execute curl command and return response text"""
    try:
        # Build curl command with headers - --compressed handles gzip automatically
        cmd = ['curl', '-s', '-L', '--compressed', '--connect-timeout', '15', '--max-time', '20']
        
        # Add headers
        for key, value in headers.items():
            cmd.extend(['-H', f'{key}: {value}'])
        
        cmd.append(url)
        
        # Execute curl command
        result = subprocess.run(cmd, capture_output=True, timeout=25)
        
        if result.returncode == 0:
            # Try to decode with UTF-8, fallback to latin-1 if needed
            try:
                return result.stdout.decode('utf-8')
            except UnicodeDecodeError:
                return result.stdout.decode('latin-1')
        else:
            error_msg = result.stderr.decode('utf-8', errors='ignore') if result.stderr else 'Unknown error'
            print(f"# Curl error for {url}: {error_msg}", file=sys.stderr)
            return None
            
    except subprocess.TimeoutExpired:
        print(f"# Curl timeout for {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"# Curl exception for {url}: {e}", file=sys.stderr)
        return None

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
            response = curl_request(line)
            if response:
                m3u8_links = re.findall(r'https://[^"]+\.m3u8', response)
                if m3u8_links:
                    link = m3u8_links[0] 
                else:
                    link = 'https://live-iptv.github.io/youtube_live/assets/info.m3u8'
            else:
                link = 'https://live-iptv.github.io/youtube_live/assets/info.m3u8'
                    
            print(link)