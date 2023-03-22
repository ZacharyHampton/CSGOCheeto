import os
import requests
import json


def parse_dump_offsets():
    offset_website = "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"
    web = False if os.path.isfile("client/data/csgo.json") else True

    class Offsets:
        pass

    offsets = requests.get(offset_website).json() if web else json.load(open("client/data/csgo.json"))
    [setattr(Offsets, k, v) for k, v in offsets["signatures"].items()]
    [setattr(Offsets, k, v) for k, v in offsets["netvars"].items()]

    return Offsets
