from random import randint

from manage import Manager, update_balance
from static_text import GUESS_WHAT, ODD_OR_EVEN, GUESS_RANGE
from utility import *


# TODO 게임마다 설명 집어넣기


def choose_one(manager: Manager):
    print(GUESS_WHAT)
    random_num = randint(1, 36)
    guess = int(colored_input((0, 255, 0)))
    while guess < 1 or guess > 36:
        guess = int(colored_input((0, 255, 0)))
    if random_num == guess:
        colored_print("Congratulations! You've got it right and earned £360.", (66, 245, 212))
        update_balance(manager, 35)
    else:
        colored_print("Unfortunately, you've got it wrong. You've lost £10.", (66, 245, 212))
        update_balance(manager, -1)


def odd_even(manager: Manager):
    print(ODD_OR_EVEN)
    random_num = randint(1, 36)
    guess = colored_input((0, 255, 0))
    while guess != "1" or guess != "2":
        guess = colored_input((0, 255, 0))

    if (guess == "1" and random_num % 2 == 1) or (guess == "2" and random_num % 2 == 0):
        colored_print("Congratulations! You've got it right and earned £20.", (66, 245, 212))
        update_balance(manager, 1)
    else:
        colored_print("Unfortunately, you've got it wrong. You've lost £10.", (66, 245, 212))
        update_balance(manager, -1)


def up_down(manager: Manager):
    print(GUESS_RANGE)
    random_num = randint(1, 36)
    guess = colored_input((0, 255, 0))
    while guess != "1" and guess != "2":
        guess = colored_input((0, 255, 0))

    if (guess == "1" and random_num <= 18) or (guess == "2" and 19 <= random_num):
        colored_print("Congratulations! You've got it right and earned £20.", (66, 245, 212))
        update_balance(manager, 1)
    else:
        colored_print("Unfortunately, you've got it wrong. You've lost £10.", (66, 245, 212))
        update_balance(manager, -1)
