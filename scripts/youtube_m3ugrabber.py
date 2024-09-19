import urllib.request

url = 'https://www.youtube.com/channel/UCup3etEdjyF1L3sRbU-rKLw/live'

try:
    with urllib.request.urlopen(url, timeout=15) as response:
        data = response.read().decode('utf-8')
        print(data)
except Exception as e:
    print(f"An error occurred: {e}")
