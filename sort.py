from colorsys import rgb_to_hsv

from PIL import Image, ImageStat
from sys import argv
from requests import get, post, put
from base64 import b64encode
from io import BytesIO
from time import sleep
from json import loads

CONFIG = loads(open("config.json", "r").read())


def insertion_sort(seq: list, from_: int, to: int, playlist_id: str):
    if from_ == to:
        return seq

    min_ = AvgColor([255, 255, 255])
    pos = 0
    for i in range(from_, to):
        if seq[i][1] < min_:
            min_ = seq[i][1]
            pos = i

    to_move = seq[pos]
    seq = seq[:pos] + seq[pos + 1:]
    seq.insert(from_, to_move)

    response = put(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
                   headers={"Authorization": f"Bearer {CONFIG['oauth_token']}", "Content-Type": "application/json",
                            "Accept": "application/json"},
                   json={"range_start": pos, "insert_before": from_, "range_length": 1})

    if response.status_code != 200:
        print("An error occurred: ")
        print(response.content)
        exit(1)

    sleep(1)
    print(f"\033[1;{from_+1}H#\t\033[2;1H({from_+1}/{to})")
    seq = insertion_sort(seq, from_ + 1, to, playlist_id)
    return seq


def step(rgb, repetitions=1):
    r, g, b = rgb
    lum = (.241 * r + .691 * g + .068 * b) ** 0.5

    h, s, v = rgb_to_hsv(r, g, b)

    h2 = int(h * repetitions)
    v2 = int(v * repetitions)

    if h2 % 2 == 1:
        v2 = repetitions - v2
        lum = repetitions - lum

    return h2, lum, v2


def avg_color(img: Image):
    return ImageStat.Stat(img).rms


def float_2_int(band_array: list):
    for index, element in enumerate(band_array):
        band_array[index] = int(element) + 1
    return band_array


class AvgColor:

    def __init__(self, band_array: list):
        self.__int_array = float_2_int(band_array.copy())

    def get_numeric_value(self):
        return step(self.__int_array)

    def __gt__(self, other):
        self_value = self.get_numeric_value()
        other_value = other.get_numeric_value()

        return self_value > other_value

    def __lt__(self, other):
        self_value = self.get_numeric_value()
        other_value = other.get_numeric_value()

        return self_value < other_value

    def __le__(self, other):
        self_value = self.get_numeric_value()
        other_value = other.get_numeric_value()

        return self_value <= other_value

    def __ge__(self, other):
        self_value = self.get_numeric_value()
        other_value = other.get_numeric_value()

        return self_value >= other_value

    def __eq__(self, other):
        self_value = self.get_numeric_value()
        other_value = other.get_numeric_value()

        return self_value == other_value


if __name__ == "__main__":

    if len(argv) < 2:
        print("Usage: python main.py [PLAYLIST ID]")
        exit(0)

    p_id = argv[1]

    client_id = CONFIG["client_id"]
    client_secret = CONFIG["client_secret"]

    basic_auth = b64encode(bytes(client_id + ":" + client_secret, "utf8")).decode("utf-8")
    token_request = post(f"https://accounts.spotify.com/api/token",
                         headers={"Authorization": "Basic " + basic_auth},
                         data={"grant_type": "client_credentials"})

    access_token = token_request.json()["access_token"]
    playlist = get(f"https://api.spotify.com/v1/playlists/{p_id}",
                   headers={"Authorization": f"Bearer {access_token}"})

    playlist_tracks = playlist.json()["tracks"]["items"]
    track_amount = len(playlist_tracks)

    color_mean = []

    for track in playlist_tracks:
        track_cover = get(track["track"]["album"]["images"][0]["url"])
        image = AvgColor(avg_color(Image.open(BytesIO(track_cover.content))))
        color_mean.append((track["track"]["uri"], image))
        print(f"Loaded track \"{track['track']['name']}\"")

    print("\033[2J")
    print("Sorting the tracks... (please keep in mind that this takes one second per song to avoid API rate limiting)")
    insertion_sort(color_mean, 0, len(color_mean), p_id)

    sorted_colors = None
    sorted_track_ids = []
