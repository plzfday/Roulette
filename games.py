from random import randint

from manager import Manager
from statics import GUESS_WHAT, ODD_OR_EVEN, GUESS_RANGE
from utility import *


def choose_one(manager: Manager):
    print(GUESS_WHAT)
    print("You can choose one number within the range of 1-36")
    print("If you guess the right number, you will get 36x of your bet")
    random_num = randint(1, 36)
    guess = int(colored_input((0, 255, 0)))
    while guess < 1 or guess > 36:
        guess = int(colored_input((0, 255, 0)))
    if random_num == guess:
        colored_print("Congratulations! You've got it right and earned £360.", (66, 245, 212))
        manager.update_balance(35)
        manager.log("Choose One", "W")
    else:
        colored_print("Unfortunately, you've got it wrong. You've lost £10.", (66, 245, 212))
        manager.update_balance(-1)
        manager.log("Choose One", "L")


def odd_even(manager: Manager):
    print(ODD_OR_EVEN)
    print("You can guess whether the number is odd or even")
    print("1. Odd!")
    print("2. Even!")
    random_num = randint(1, 36)
    guess = colored_input((0, 255, 0))
    while guess != "1" and guess != "2":
        guess = colored_input((0, 255, 0))

    if (guess == "1" and random_num % 2 == 1) or (guess == "2" and random_num % 2 == 0):
        colored_print("Congratulations! You've got it right and earned £20.", (66, 245, 212))
        manager.update_balance(1)
        manager.log("Odd or Even", "W")
    else:
        colored_print("Unfortunately, you've got it wrong. You've lost £10.", (66, 245, 212))
        manager.update_balance(-1)
        manager.log("Odd or Even", "L")


def up_down(manager: Manager):
    print(GUESS_RANGE)
    print("You can guess whether the number is between 1-18 or 19-38")
    print("1. 1-18!")
    print("2. 19-38!")
    random_num = randint(1, 36)
    guess = colored_input((0, 255, 0))
    while guess != "1" and guess != "2":
        guess = colored_input((0, 255, 0))

    if (guess == "1" and random_num <= 18) or (guess == "2" and 19 <= random_num):
        colored_print("Congratulations! You've got it right and earned £20.", (66, 245, 212))
        manager.update_balance(1)
        manager.log("Guess Range", "W")
    else:
        colored_print("Unfortunately, you've got it wrong. You've lost £10.", (66, 245, 212))
        manager.update_balance(-1)
        manager.log("Guess Range", "L")
