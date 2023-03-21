from client.internal.memwrapper.memwrapper import Memory
import client.internal.wss as wss
import threading


def main():
    threading.Thread(target=wss.start).start()
    Memory()


if __name__ == '__main__':
    main()
