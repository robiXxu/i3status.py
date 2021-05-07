#!/usr/bin/env python
import time
import json
from datetime import datetime
import socket
import psutil

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


if __name__ == '__main__':
    print('{ "version": 1 }')
    print("[")
    print("[]")

    while True:
        items = [
                item(
                    name="ip_local",
                    full_text="  {} ".format(socket.gethostbyname(socket.gethostname())),
                    color="#333333",
                    background="#C49D58",
                    prevColor=mainColor
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
        time.sleep(10)

