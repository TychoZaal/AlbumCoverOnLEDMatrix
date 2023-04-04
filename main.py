from dotenv import load_dotenv
from urllib.request import urlopen
from PIL import Image
from requests import post, get
from ytmusicapi import YTMusic
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time


def get_current_song(last_song_id, time_since_last_duplicate_result):
    last_listened_song = ytmusic.get_history()[0]

    if last_song_id != last_listened_song["videoId"]:

        # Found different song, resetting variables
        last_song_id = last_listened_song["videoId"]
        time_since_last_duplicate_result = 0
        print(last_listened_song["title"])

        # Get new song thumbnail
        thumbnail = get_thumbnail(last_listened_song=last_listened_song)

        # TODO: convert and display image

    else:
        # Still the same song, wait before sending a new request
        sleep_time = 1.0
        time.sleep(sleep_time)
        time_since_last_duplicate_result = time_since_last_duplicate_result + sleep_time

    # If more than 5 minutes have passed, assume the player is idle / closed, and display default logo instead
    if time_since_last_duplicate_result < 10:
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
    return img


def display_default_logo(last_song_id):
    img = Image.open("YTMLOGO.png")
    img.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    visualize_thumbnail(img)

    get_current_song(last_song_id, 10)


def convert_thumnail_data(img):
    img.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    visualize_thumbnail(img)


def visualize_thumbnail(img):
    matrix.SetImage(img.convert('RGB'))


def setup_led_board():
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.gpio_slowdown = 4
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'

    matrix = RGBMatrix(options=options)
    return matrix


ytmusic = YTMusic('headers_auth.json')  # Youtube music API

matrix = setup_led_board()

# Get currently playing / last played song
get_current_song(None, 0)
