from random import randint

from manager import Manager
from static_data import DEFAULT_BET, GUESS_WHAT, ODD_OR_EVEN, GUESS_RANGE
from utility import colored_input, system_notification


def choose_one(manager: Manager):
    """
    Game Mode: Choose One (Within range of 1 to 36, choose one number)
    Default bet: 10 pounds ; Guessing right, returns 360 pounds
                             or just lose the bet (total -10 pounds)
    :param manager: an object that controls overall game circumstance
    :return: None
    """
    print(GUESS_WHAT)
    print(f"Bet Amount: £{DEFAULT_BET}")
    print("You can choose one number within the range of 1-36")
    print("If you guess the right number, you will get 36x of your bet")
    random_num = randint(1, 36)
    while True:
        try:
            guess = int(colored_input((0, 255, 0)))
            break
        except ValueError:
            pass
    while guess < 1 or guess > 36:
        guess = int(colored_input((0, 255, 0)))
    if random_num == guess:
        system_notification("Congratulations! You've got it right and earned £360.", (66, 245, 212))
        manager.update_balance(36)
        manager.log("Choose One", "W")
    else:
        system_notification("Unfortunately, you've got it wrong. You've lost £10.", (66, 245, 212))
        manager.update_balance(-1)
        manager.log("Choose One", "L")


def odd_even(manager: Manager):
    """
    Game Mode: Odd or Even (Guess whether a number would be odd or even)
    Default bet: 10 pounds ; Guessing right, returns 20 pounds
                             or just lose the bet (total -10 pounds)
    :param manager: an object that controls overall game circumstance
    :return: None
    """
    print(ODD_OR_EVEN)
    print(f"Bet Amount: £{DEFAULT_BET}")
    print("You can guess whether the number is odd or even")
    print("1. Odd!")
    print("2. Even!")
    random_num = randint(1, 36)
    guess = colored_input((0, 255, 0))
    while guess != "1" and guess != "2":
        guess = colored_input((0, 255, 0))

    if (guess == "1" and random_num % 2 == 1) or (guess == "2" and random_num % 2 == 0):
        system_notification("Congratulations! You've got it right and earned £20.", (66, 245, 212))
        manager.update_balance(2)
        manager.log("Odd or Even", "W")
    else:
        system_notification("Unfortunately, you've got it wrong. You've lost £10.", (66, 245, 212))
        manager.update_balance(-1)
        manager.log("Odd or Even", "L")


def up_down(manager: Manager):
    """
    Game Mode: Guess Range (Guess whether a number would be in between 1-18 or 19-36)
    Default bet: 10 pounds ; Guessing right, returns 20 pounds
                             or just lose the bet (total -10 pounds)
    :param manager: an object that controls overall game circumstance
    :return: None
    """
    print(GUESS_RANGE)
    print(f"Bet Amount: £{DEFAULT_BET}")
    print("You can guess whether the number is between 1-18 or 19-38")
    print("1. 1-18!")
    print("2. 19-38!")
    random_num = randint(1, 36)
    guess = colored_input((0, 255, 0))
    while guess != "1" and guess != "2":
        guess = colored_input((0, 255, 0))

    if (guess == "1" and random_num <= 18) or (guess == "2" and 19 <= random_num):
        system_notification("Congratulations! You've got it right and earned £20.", (66, 245, 212))
        manager.update_balance(2)
        manager.log("Guess Range", "W")
    else:
        system_notification("Unfortunately, you've got it wrong. You've lost £10.", (66, 245, 212))
        manager.update_balance(-1)
        manager.log("Guess Range", "L")
