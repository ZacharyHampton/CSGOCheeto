import os
from colorama import Fore
from tabulate import tabulate
import time
from client.cheeto.globals import memory, offsets


def main_game_thread():
    if os.getenv("DEBUG"):
        table = [
            [Fore.LIGHTCYAN_EX + k, Fore.LIGHTWHITE_EX + hex(v).upper()]
            for k, v in vars(offsets).items()
            if not k.startswith("_")
        ]
        print(tabulate(table, ("Name", "Pointer / Offset"), "pretty", showindex=True))

    client = memory.module_from_name("client.dll")
    engine = memory.module_from_name("engine.dll")
    engine_ptr = memory.read_ptr(engine + offsets.dwClientState)

    while True:
        time.sleep(0.0025)
