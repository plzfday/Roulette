import os

from manager import Manager
from prompts import menu


if __name__ == '__main__':
    os.system('')  # Needed for windows CMD font colouring
    manager = Manager()
    while True:
        menu(manager)
