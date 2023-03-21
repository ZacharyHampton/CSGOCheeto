from internal.memwrapper.memwrapper import Memory
import internal.wss as wss
import threading


def main():
    threading.Thread(target=wss.start).start()
    Memory()


if __name__ == '__main__':
    main()
