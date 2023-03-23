import os
from colorama import Fore
from tabulate import tabulate
import time
from client.cheeto.globals import memory, offsets
from client.cheeto.objects.engine import Engine
from client.cheeto.objects.entity import Entity
from client.internal.memwrapper.exceptions import NullPointerError
from client.cheeto.objects.player import Player
from ctypes import c_int32


def main_game_thread():
    def debug(*args):
        if os.getenv("DEBUG"):
            print(' '.join(map(str, args)))

    def log(*args):
        print(' '.join(map(str, args)))

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

        engine = Engine()
        if engine.is_in_game():
            localPlayer = engine.get_local_player()
            for index in range(0, engine.get_max_clients()):
                try:
                    player = Entity.get_client_entity(index)
                except NullPointerError:
                    continue

                isLocalPlayer = player.address == localPlayer.address

                if (health := player.get_health()) <= 0:
                    debug('[-] Skipping player 0x%X with health %d' % (player.address, health))
                    continue

                if lifestate := player.get_life_state():
                    debug('[-] Skipping player 0x%X with lifestate %d' % (player.address, lifestate))
                    continue

                if dormant := player.is_dormant():
                    debug('[-] Skipping player 0x%X with dormant %d' % (player.address, dormant))
                    continue

                print("[+] Found player: 0x%X, health: %d, position: %s, isLocalPlayer: %s" % (player.address, health, player.get_bone_pos(6), isLocalPlayer))


            """localPlayer = engine.get_local_player()
            print("[+] Found local player: 0x%X, health: %d, position: %s" % (localPlayer.address, localPlayer.get_health(), localPlayer.get_bone_pos(6)))"""
        else:
            time.sleep(0.5)
            print("[+] Waiting for game to start...")
            continue


