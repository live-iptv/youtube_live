import http.client
import re
# Specify the URL and path
url = 'www.youtube.com'
path = '/channel/UCup3etEdjyF1L3sRbU-rKLw/live'

# Create a connection
conn = http.client.HTTPSConnection(url, timeout=15)

try:
    # Make the request
    conn.request("GET", path)
    
    # Get the response
    response = conn.getresponse()
    
    # Read and decode the response
    data = response.read().decode('utf-8')
    
    m3u8_links = re.findall(r'https://[^"]+\.m3u8', data)
    if m3u8_links:
        link = m3u8_links[0] 
    else:
        link = 'https://live-iptv.github.io/youtube_live/assets/info.m3u8'                    
    print(link)
finally:
    conn.close()
