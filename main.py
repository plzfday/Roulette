from manage import init
from prompts import menu

import os

# TODO 전적 보여주기 - Pagination 설정, 시간 순서 반대로
# TODO 파일 관련 코드들 예외처리 하기

if __name__ == '__main__':
    os.system('')
    manager = init()
    while True:
        menu(manager)
