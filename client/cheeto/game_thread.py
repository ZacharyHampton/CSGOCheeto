import ctypes
import os
from colorama import Fore
from tabulate import tabulate
import time
from client.cheeto.globals import memory, offsets
from client.cheeto.objects.engine import Engine
from client.cheeto.objects.entity import Entity
from client.internal.memwrapper.exceptions import NullPointerError
from client.cheeto.objects.player import Player
from ctypes import c_int32, c_int64


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

    previously_in_game = False

    while True:
        time.sleep(0.0025)

        engine = Engine()
        if engine.is_in_game():
            if not previously_in_game:
                log("[+] Game started!")
                previously_in_game = True
                #: TODO: send websocket that game has started with map information

            #: Get all players in game
            try:
                localPlayer = engine.get_local_player()
            except NullPointerError:
                debug("[-] Local player is null")
                continue

            for index in range(0, engine.get_max_clients()):
                try:
                    player = Entity.get_client_entity(index)
                except NullPointerError:
                    continue

                isLocalPlayer = player.address == localPlayer.address

                if dormant := player.is_dormant():
                    debug('[-] Skipping player 0x%X with dormant %d' % (player.address, dormant))
                    continue

                if not player.is_valid():
                    debug('[-] Skipping player 0x%X with health %d and life state %d' % (
                        player.address, player.get_health(), player.get_life_state()))
                    continue

                name = str(memory.read(engine.get_player_info(index) + 0x10, ctypes.create_string_buffer(128)))
                steam_id = str(memory.read(engine.get_player_info(index) + 0x94, ctypes.create_string_buffer(20)))
                health = player.get_health()

                log("[+] Found player: 0x%X, health: %d, position: %s, name: %s" % (
                    player.address, health, player.get_bone_pos(10), name))
        else:
            if previously_in_game:
                log("[+] Game ended!")
                previously_in_game = False
                #: TODO: send websocket that game has ended

            time.sleep(0.5)
            log("[+] Waiting for game to start...")
            continue
