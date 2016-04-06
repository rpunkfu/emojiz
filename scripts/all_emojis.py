import json
import os
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from emoji_urls import EMOJI_URLS

FAKE_USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
EMOJIS_CONTAINER_CLASS = "emoji-grid"
EMOJI_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../emojis/"
MODIFIER = "+_emoji_modifier_fitzpatrick_type-"


def read_website(url):
    headers = {"User-Agent": FAKE_USER_AGENT}
    request = urllib.request.Request(url, None, headers)
    with urllib.request.urlopen(request) as response:
        return response.read()


def get_emojis_container(html):
    yummm = BeautifulSoup(html, 'html.parser')
    return yummm.find(class_=EMOJIS_CONTAINER_CLASS)


def get_emoji_images(container):
    return container.find_all("img")


def parse_emoji_image(image):
    name = image["title"].lower().replace(" ", "_").replace(MODIFIER, "type_")
    url = image["src"]
    return (name, url)


def get_emojis_filename(emojis_creator):
    return "{creator}_emojis.json".format(creator=emojis_creator)


def create_emoji_json_file(emojis_creator, emojis_dict):
    emojis_filename = get_emojis_filename(emojis_creator)
    with open(EMOJI_DIR + emojis_filename, 'w') as file:
        json.dump(emojis_dict, file)


def main():
    all_emojis = dict()

    for emojis_creator, emoji_url in EMOJI_URLS.items():
        website_html = read_website(emoji_url)
        emojis_container = get_emojis_container(website_html)
        emoji_images = get_emoji_images(emojis_container)
        emojis = list(map(parse_emoji_image, emoji_images))
        emojis_dict = {name: url for name, url in emojis}
        all_emojis[emojis_creator] = emojis_dict
        create_emoji_json_file(emojis_creator, emojis_dict)

    create_emoji_json_file('all', all_emojis)

if __name__ == '__main__':
    main()
