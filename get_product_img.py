import os

from bs4 import BeautifulSoup
import requests
import html5lib

PATH = os.getcwd()

def download_image(tts_url, filename):
    """
    Download an image from a URL and save it to a file.
    """
    r = requests.get(tts_url)
    soup = BeautifulSoup(r.content, 'html5lib')

    table = soup.find_all('img', attrs={"class": "lazy-img"})
    img_url = table[0]['data-src']

    response = requests.get(img_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image saved as {filename}")
    else:
        print(f"Failed to download image: {response.status_code}")

    return filename