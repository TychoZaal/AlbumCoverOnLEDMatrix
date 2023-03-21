from dotenv import load_dotenv
from urllib.request import urlopen
from PIL import Image
from requests import post, get
from ytmusicapi import YTMusic
import time


def get_current_song(last_song_id, time_since_last_duplicate_result):
    last_listened_song = ytmusic.get_history()[0]

    if last_song_id != last_listened_song["videoId"]:

        # Found different song, resetting variables
        last_song_id = last_listened_song["videoId"]
        time_since_last_duplicate_result = 0
        print(last_listened_song["title"])

        # Get new song thumbnail
        get_thumbnail(last_listened_song=last_listened_song)

    else:
        # Still the same song, wait before sending a new request
        sleep_time = 1.0
        time.sleep(sleep_time)
        time_since_last_duplicate_result = time_since_last_duplicate_result + sleep_time

    # If more than 5 minutes have passed, assume the player is idle / closed, and display default logo instead
    if time_since_last_duplicate_result < 300:
        get_current_song(last_song_id, time_since_last_duplicate_result)
    else:
        display_default_logo(last_song_id=last_song_id)


def get_thumbnail(last_listened_song):
    song_thumnails = last_listened_song["thumbnails"]

    lowestResolution = 0
    url = ""

    for thumbnail in song_thumnails:
        resolution = thumbnail["width"] * thumbnail["height"]

        if resolution > lowestResolution:
            url = thumbnail["url"]
            lowestResolution = resolution

    img = Image.open(urlopen(url))
    # print(img)


def display_default_logo(img, last_song_id):
    # TODO display default logo when the user is not listening to anything
    print(img)
    # TODO check last_listened_song once in a while


def convert_thumnail_data(img):
    # TODO convert img to pixel array or something
    print("converting data...")


def visualize_thumbnail():
    # TODO send data to LED Matrix
    print("visualizing...")


ytmusic = YTMusic('headers_auth.json')  # Youtube music API

# Get currently playing / last played song
get_current_song(None)
