import json
import os
from random import choice
import time
import unicodedata

from dotenv import load_dotenv
from atproto import Client


def generate_valid_unicode(dump : bool = False) -> list[int]:
    # Inspired by https://appdividend.com/how-to-print-all-unicode-characters-in-python/
    valid_codes = []
    for char_hex in range(0x110000):
        char = chr(char_hex)
        try:
            unicodedata.name(char)
        except ValueError:
            pass
        else:
            valid_codes.append(char_hex)
    if dump:
        with open(os.path.join(os.path.dirname(__file__), "valid_unicode.json"), "w") as f:
            json.dump(valid_codes, f)
    return valid_codes


def load_valid_unicode() -> list[int]:
    with open(os.path.join(os.path.dirname(__file__), "valid_unicode.json"), "r") as f:
        valid_codes = json.load(f)
    return valid_codes


def post_random_unicode(client: Client):
    valid_codes = load_valid_unicode()
    rando = choice(valid_codes)
    char = chr(rando)
    name = unicodedata.name(char)
    try:
        client.post(char)
    except Exception as e:
        print(f"Failed! Tried to post U+{rando:04X}: {char} - {name}")
        print(e)
    else:
        print(f"Success! Posted U+{rando:04X}: {char} - {name}")


def log_in_and_post():
    load_dotenv()

    client = Client()
    client.login(os.environ["BLUESKY_USERNAME"], os.environ["BLUESKY_PASSWORD"])
    while True:
        post_random_unicode(client)
        time.sleep(60*60)


log_in_and_post()
