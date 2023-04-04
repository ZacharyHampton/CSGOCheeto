import ctypes
import os
from colorama import Fore
from tabulate import tabulate
import time
from client.internal.wss import manager
from client.cheeto.globals import memory, offsets
from client.cheeto.objects.engine import Engine
from client.cheeto.objects.entity import Entity
from client.internal.memwrapper.exceptions import NullPointerError
from client.cheeto.models.packet import Packet
from client.cheeto.models.player import Player
from client.cheeto.models.map import Map
from client.cheeto.models.status import Status
import asyncio


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
    players = {
        #: steam_id: Player
    }

    while True:
        time.sleep(0.0025)

        engine = Engine()
        if engine.is_in_game():
            if not previously_in_game:
                log("[+] Game started!")
                previously_in_game = True

                asyncio.run(manager.broadcast(Packet(
                    map=Map(name=engine.get_map_name()),
                    status=Status(status="game_started")
                )))

            try:
                localPlayer = engine.get_local_player()
            except NullPointerError:
                debug("[-] Local player is null")
                continue

            #: Get all players in game
            players_to_send = []
            for index in range(0, engine.get_max_clients()):
                try:
                    player = Entity.get_client_entity(index)
                except NullPointerError:
                    continue

                if player.address == 0:
                    continue

                isLocalPlayer = player.address == localPlayer.address

                if dormant := player.is_dormant():
                    debug('[-] Skipping player 0x%X with dormant %d' % (player.address, dormant))
                    continue

                name = str(memory.read(engine.get_player_info(index) + 0x10, ctypes.create_string_buffer(128)))
                steam_id = str(memory.read(engine.get_player_info(index) + 0x94, ctypes.create_string_buffer(20)))
                health = player.get_health()

                if steam_id == "BOT":
                    name = ' '.join([steam_id, name])
                    steam_id = name

                try:
                    weapon_id = player.get_weapon_id()
                except NullPointerError:
                    weapon_id = 0

                team = player.get_team_number()
                if player.get_life_state() == 0:
                    position = player.get_bone_pos(10)
                else:
                    position = None

                packet_player = Player(
                        steam_id=steam_id,
                        name=name,
                        team=team,
                        health=health,
                        position=position,
                        weapon_id=weapon_id,
                        isLocalPlayer=isLocalPlayer
                    )

                if steam_id not in players.keys():
                    log("[+] Found player: 0x%X, health: %d, position: %s, name: %s" % (
                        player.address, health, position, name))

                    players[steam_id] = packet_player
                    players_to_send.append(packet_player)
                else:
                    previous_player = players[steam_id].copy()
                    players[steam_id].health = health
                    players[steam_id].name = name
                    players[steam_id].team = packet_player.team
                    players[steam_id].position = packet_player.position
                    players[steam_id].weapon_id = weapon_id

                    if previous_player.dict() != players[steam_id].dict():
                        log("[+] Player updated: 0x%X, health: %d, position: %s, name: %s" % (
                            player.address, health, position, name))
                        players_to_send.append(players[steam_id])

            if len(players_to_send) > 0:
                asyncio.run(manager.broadcast(Packet(
                    players=players_to_send,
                    status=Status(status="players_updated")
                )))
        else:
            if previously_in_game:
                log("[+] Game ended!")
                previously_in_game = False

                asyncio.run(manager.broadcast(Packet(
                    status=Status(status="game_ended")
                )))
                players = {}

            time.sleep(0.5)
            log("[+] Waiting for game to start...")
            continue
