import os

from manager import Manager
from prompts import menu

# TODO Comment
# TODO index != -1에서 Valid로 바꾸기

if __name__ == '__main__':
    os.system('')
    manager = Manager()
    while True:
        menu(manager)
