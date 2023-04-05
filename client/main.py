import time
import client.internal.wss as wss
from client.cheeto.game_thread import main_game_thread
import threading


def main():
    threading.Thread(target=wss.start).start()
    while not wss.manager:
        pass

    time.sleep(3)
    threading.Thread(target=main_game_thread).start()


if __name__ == '__main__':
    main()
