#!/usr/bin/env python
import time
import json
from datetime import datetime
import socket
import psutil
import dbus

main_color="#2E3440"
# in seconds
update_rate = 10

def separator(c1, c2):
    obj = {
        "full_text": "",
        "separator": "false",
        "separator_block_width": 0,
        "border": main_color,
        "border_left": 0,
        "border_right": 0,
        "border_top": 0,
        "border_bottom": 0,
        "color": c1,
        "background": c2
    }
    return json.dumps(obj)

def getSpotifyInfo():
    try:
        sessionBus = dbus.SessionBus()
        spotify_object = sessionBus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        spotify_props = dbus.Interface(spotify_object,'org.freedesktop.DBus.Properties')

        spotify_meta = spotify_props.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

        return "{} - {}".format(spotify_meta['xesam:artist'][0], spotify_meta['xesam:title'])

    except Exception as e:
        # spotify is closed
        if isinstance(e, dbus.exceptions.DBusException):
            return ''
        else:
            print(e)
            return ''

class Item:
    def __init__(self, name, full_text, color, background, enabled):
        self.name = name
        self.full_text = full_text
        self.color = color
        self.background = background
        self.enabled = enabled
    def print(self, prev_color):
        obj = {
            "full_text": self.full_text,
            "name": self.name,
            "color": self.color,
            "background": self.background,
            "separator": "false",
            "separator_block_width": 0,
            "border": main_color,
            "border_left": 0,
            "border_right": 0,
            "border_top": 0,
            "border_bottom": 0,
        }
        return ",".join([separator(self.background, prev_color), json.dumps(obj)])


def items_array():
    spotifyInfo = getSpotifyInfo()
    return list(filter(lambda i: i.enabled, [
        Item(
            name="id_spotify_info",
            full_text=" {} ".format(spotifyInfo),
            color="#EEEEEE",
            background="#666666",
            enabled=len(spotifyInfo) > 0
        ),
        Item(
            name="id_ip_local",
            full_text="  {} ".format(socket.gethostbyname(socket.gethostname())),
            color="#333333",
            background="#C49D58",
            enabled=True
        ),
        Item(
            name="id_disk_usage",
            full_text="  {}% ".format(psutil.disk_usage('/').percent),
            color="#EEEEEE",
            background="#3949AB",
            enabled=True
        ),
        Item(
            name="id_memory",
            full_text="  {}% ".format(psutil.virtual_memory()[2]),
            color="#DDDDDD",
            background="#B87238",
            enabled=True
        ),
        Item(
            name="id_cpu_usage",
            full_text="  {}% ".format(psutil.cpu_percent(interval=1)),
            color="#FFFFFF",
            background="#A7282E",
            enabled=True
        ),
        Item(
            name="id_date",
            full_text="  {} ".format(datetime.now().strftime("%H:%M %a %d-%B")),
            color="#333333",
            background="#80B3B1",
            enabled=True
        )
    ]))


if __name__ == '__main__':
    print('{ "version": 1 }')
    print("[")
    print("[]")

    while True:
        items = []
        items_arr = items_array()
        for i, item in enumerate(items_arr):
            prev_color = main_color if i == 0 else items_arr[i-1].background
            items.append(item.print(prev_color))

        items.append(separator(main_color, items_arr[-1].background))

        print(",[{}]".format(",".join(items)))
        time.sleep(update_rate)

