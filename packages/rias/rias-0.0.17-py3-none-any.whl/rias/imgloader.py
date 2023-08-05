import os
import requests
from bs4 import BeautifulSoup
import sys


def main() -> None:
    url = sys.argv[2]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")

    save_path = sys.argv[3]
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for image in images:
        img_url = image["src"]
        if not img_url.startswith("http"):
            img_url = url + img_url
        response = requests.get(img_url)
        open(f"{save_path}/{os.path.basename(img_url)}", "wb").write(response.content)
