import os
from colorama import Fore
from tabulate import tabulate
import time
from client.cheeto.globals import memory, offsets
from client.cheeto.objects.engine import Engine
from client.cheeto.objects.entity import Entity
from client.cheeto.objects.player import Player
from ctypes import c_int32


def main_game_thread():
    if os.getenv("DEBUG"):
        table = [
            [Fore.LIGHTCYAN_EX + k, Fore.LIGHTWHITE_EX + hex(v).upper()]
            for k, v in vars(offsets).items()
            if not k.startswith("_")
        ]
        print(tabulate(table, ("Name", "Pointer / Offset"), "pretty", showindex=True))

    offsets.client = memory.module_from_name("client.dll")
    offsets.engine = memory.module_from_name("engine.dll")

    while True:
        time.sleep(0.0025)
        if (engineObject := Engine()).is_in_game():
            #: cannot get local player / entity
            localPlayer = engineObject.get_local_player()
            print("[+] Found local player: 0x%X, health: %d\n" % (localPlayer.address, localPlayer.get_health()))
        else:
            time.sleep(0.5)
            print("[+] Waiting for game to start...")
            continue


