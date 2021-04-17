from manage import init
from prompts import menu

# TODO 전적 보여주기
# TODO 파일 관련 코드들 예외처리 하기

if __name__ == '__main__':
    manager = init()
    while True:
        menu(manager)
