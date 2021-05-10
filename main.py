from manage import init
from prompts import menu

import os

# TODO 전적 보여주기 - Pagination 설정
# TODO 주석 달기

if __name__ == '__main__':
    os.system('')
    manager = init()
    while True:
        menu(manager)
