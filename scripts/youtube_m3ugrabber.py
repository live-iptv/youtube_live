import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=15) as response:
            text = await response.text()
            print(text)  # Print the response text
            return text

url = 'https://www.youtube.com/channel/UCup3etEdjyF1L3sRbU-rKLw/live'

# Run the async function
asyncio.run(fetch(url))
