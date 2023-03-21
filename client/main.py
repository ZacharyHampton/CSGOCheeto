import client.internal.wss as wss
from client.cheeto.game_thread import main_game_thread
import threading


def main():
    threading.Thread(target=wss.start).start()
    threading.Thread(target=main_game_thread).start()


if __name__ == '__main__':
    main()
