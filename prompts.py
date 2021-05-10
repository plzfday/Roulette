import sys
from getpass import getpass

from games import *
from statics import MASTER_PASSWORD, ROULETTE, DISCLAIMER, SELECT_MODE, LOCKED
from utility import *
from manager import Manager, signup


def menu(manager: Manager):
    # Keyword: SUCCESS, FAILED 같은 걸 리턴하는 게 좋음
    if manager.locked:
        colored_print(LOCKED + "\nPlease contact an administrator.", (255, 0, 0))
        if not master_key(manager):
            exit()

    print(ROULETTE)
    # Case: Already signed in or not yet
    if manager.user.is_online():
        print("1. Play")
        print("2. Record")
        print("3. Sign Out")
        print("Q. Quit Game")

        menu_num = colored_input((0, 255, 0))

        if menu_num == "1":
            select_mode(manager)
        elif menu_num == "2":
            manager.user.display_record()
        elif menu_num == "3":
            manager.logout()
        elif menu_num == "Q" or menu_num == "q":
            manager.save()
            sys.exit()
        else:
            colored_print("Please Type Correctly", (255, 0, 0))
    else:
        print("1. Sign In")
        print("2. Create an Account")
        print("Q. Quit Game")

        menu_num = colored_input((0, 255, 0))

        if menu_num == "1":
            return manager.login()
        elif menu_num == "2":
            signup()
        elif menu_num == "Q" or menu_num == "q":
            sys.exit()
        else:
            colored_print("Please Type Correctly", (255, 0, 0))


def disclaimer(manager: Manager) -> bool:
    colored_print(DISCLAIMER, (255, 0, 0))
    colored_print("You are more likely to lose your money and the odds are against you.", (255, 0, 0))
    colored_print("You must agree that you're taking a risk.", (255, 0, 0))
    colored_print('Please type "AGREE" if you agree and want to continue.', (255, 0, 0))
    agreement = colored_input((255, 255, 0))
    if agreement != "AGREE":
        colored_print("Since you didn't agree with this disclaimer, you're redirected to the main.", (66, 245, 212))
        input()
        return False
    manager.agree = True
    return True


def select_mode(manager: Manager):
    if not manager.agree and not disclaimer(manager):
        return

    while True:
        if not manager.user.is_affordable():
            colored_print("Sorry. You don't have enough money. Please top up.", (255, 0, 0))
            input()
            break

        print(SELECT_MODE)
        print("1. Guess Number                        (return x36)")
        print("2. Guess Whether Number Is Odd or Even (return x2)")
        print("3. Guess the Right Range               (return x2)")
        print("Q. Quit to Title")

        mode_num = colored_input((0, 255, 0))

        if mode_num == "1":
            choose_one(manager)
        elif mode_num == "2":
            odd_even(manager)
        elif mode_num == "3":
            up_down(manager)
        elif mode_num == "Q" or mode_num == "q":
            menu(manager)
            break
        else:
            pass


def master_key(manager: Manager) -> bool:
    password = getpass("Master Key: ")
    if MASTER_PASSWORD == password:
        manager.unlock_machine()
        return True
    return False
