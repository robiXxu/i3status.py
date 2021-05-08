#!/usr/bin/env python
import time
import json
from datetime import datetime
import socket
import psutil
import dbus

mainColor="#2E3440"

def separator(c1, c2):
    obj = {
        "full_text": "",
        "separator": "false",
        "separator_block_width": 0,
        "border": mainColor,
        "border_left": 0,
        "border_right": 0,
        "border_top": 0,
        "border_bottom": 0,
        "color": c1,
        "background": c2
    }
    return json.dumps(obj)


def item(name, full_text, color, background, prevColor):
    obj = {
        "full_text": full_text,
        "name": name,
        "color": color,
        "background": background,
        "separator": "false",
        "separator_block_width": 0,
        "border": mainColor,
        "border_left": 0,
        "border_right": 0,
        "border_top": 0,
        "border_bottom": 0,
    }
    return ",".join([separator(background, prevColor), json.dumps(obj)])

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

if __name__ == '__main__':
    print('{ "version": 1 }')
    print("[")
    print("[]")

    while True:
        items = [
                item(
                    name="id_spotify_info",
                    full_text=" {} ".format(getSpotifyInfo()),
                    color="#444444",
                    background="#DBCB7E",
                    prevColor=mainColor
                ),
                item(
                    name="id_ip_local",
                    full_text="  {} ".format(socket.gethostbyname(socket.gethostname())),
                    color="#333333",
                    background="#C49D58",
                    prevColor="#DBCB7E"
                ),
                item(
                    name="id_disk_usage",
                    full_text="  {}% ".format(psutil.disk_usage('/').percent),
                    color="#EEEEEE",
                    background="#3949AB",
                    prevColor="#C49D58"
                ),
                item(
                    name="id_memory",
                    full_text="  {}% ".format(psutil.virtual_memory()[2]),
                    color="#DDDDDD",
                    background="#B87238",
                    prevColor="#3949AB"
                ),
                item(
                    name="id_cpu_usage",
                    full_text="  {}% ".format(psutil.cpu_percent(interval=1)),
                    color="#FFFFFF",
                    background="#A7282E",
                    prevColor="#B87238"
                ),
                item(
                    name='id_date',
                    full_text="  {} ".format(datetime.now().strftime("%H:%M %a %d-%B")),
                    color="#333333",
                    background="#80B3B1",
                    prevColor="#A7282E",
                ),
                separator(mainColor, "#80B3B1")
        ]
        print(",[{}]".format(",".join(items)))
        time.sleep(5)

