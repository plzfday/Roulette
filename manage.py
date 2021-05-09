import json
from datetime import datetime

from manage_data import sort_name, find_user
from static_text import RECORD
from utility import colored_print, change_background_color

DEFAULT_JSON_FORMAT = {
    "users": [

    ],
    "isLocked": False
}
DEFAULT_BET = 10
DEFAULT_BALANCE = 100
DEFAULT_DATA_FILE = "data.json"


class User:
    # TODO add recent login log to control the number of login trial
    def __init__(self, name="", balance=DEFAULT_BALANCE):
        self.name = name
        self.balance = balance
        self.record = []  # DateTime/Username/Game/Win or Lose/balance

    def is_online(self) -> bool:
        return self.name != ""

    def is_affordable(self) -> bool:
        return self.balance >= 10

    def display_record(self):
        print(RECORD)
        print("Username: ", end='')
        colored_print(self.name, (66, 245, 212))
        print(f"Balance: {self.balance}")

        display_list = []
        count_victory = 0
        count_defeat = 0

        with open(DEFAULT_DATA_FILE, "r") as f:
            data = json.load(f)
            index = find_user(data['users'], self.name)
            if index != -1:
                for i in data['users'][index]['record']:
                    display_list.append(i)
                    if i[2] == 'W':
                        count_victory += 1
                    elif i[2] == 'L':
                        count_defeat += 1

        for i in self.record:
            display_list.append(i)
            if i[2] == 'W':
                count_victory += 1
            elif i[2] == 'L':
                count_defeat += 1

        count_games = len(display_list)
        if count_games > 0:
            print(
                f"Total {count_games}G {count_victory}W {count_defeat}L ({round(count_victory / count_games * 100, 2)}%)")
            print("{:<26} {:<15} {:<10} {:<7}".format('Date', 'Game', 'Result', 'Balance'))
            for i in display_list:
                if i[2] == 'W':
                    change_background_color((31, 142, 205))
                elif i[2] == 'L':
                    change_background_color((238, 90, 82))
                print("{:<26} {:<15} {:<10} {:<7}\033[0m".format(i[0], i[1], i[2], i[3]))
        else:
            print("There are no results recorded.")
        input()


class Manager:
    def __init__(self, user=User()):
        self.user = user
        self.login_trial = 0
        self.locked = False
        self.agree = False


def init() -> Manager:
    manager = Manager()
    try:
        f = open(DEFAULT_DATA_FILE, "r")
        data = json.load(f)
        if 'isLocked' in data:
            manager.locked = data['isLocked']
    finally:
        return manager


def login(manager: Manager):
    # Login UI
    colored_print("? ", (0, 255, 0), end='')
    username = input("Username: ")
    colored_print("? ", (0, 255, 0), end='')
    password = input("Password: ")
    # Find User
    try:
        with open(DEFAULT_DATA_FILE, "r") as f:
            data = json.load(f)

            index = find_user(data['users'], username)
            if index != -1 and data['users'][index]['password'] == password:
                colored_print(f"Welcome, {username}", (66, 245, 212))
                manager.user = User(username, data['users'][index]['balance'])
                manager.login_trial = 0
            else:
                manager.login_trial += 1
                if manager.login_trial > 2:
                    colored_print("[MACHINE LOCKED] Please contact an administrator to unlock the machine.",
                                  (255, 0, 0))
                    lock_machine(manager)
                else:
                    colored_print(f"Username or Password is incorrect.\n"
                                  f"You can try {3 - manager.login_trial} time(s) more.", (66, 245, 212))
    except FileNotFoundError:
        colored_print("There is no registered user. Please sign up first.", (255, 0, 0))
    except json.JSONDecodeError:
        colored_print("ERROR(login-file is unstable)", (255, 0, 0))


def logout(manager: Manager):
    save(manager)
    manager.agree = False
    del manager.user
    manager.user = User()


def signup(manager: Manager):
    # Sign Up UI
    colored_print("? ", (0, 255, 0), end='')
    username = input("Username: ")
    try:
        with open(DEFAULT_DATA_FILE, "r") as f:
            data = json.load(f)
            if find_user(data['users'], username) != -1:
                colored_print("[The name is already taken]", (255, 0, 0))
                colored_print("? ", (0, 255, 0), end='')
                username = input("Username: ")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    colored_print("? ", (0, 255, 0), end='')
    password1 = input("Password: ")
    colored_print("? ", (0, 255, 0), end='')
    password2 = input("Confirm Password: ")
    while password1 != password2:
        colored_print("? ", (0, 255, 0), end='')
        password2 = input("[Doesn't Match] Confirm Password: ")

    # Load data file and append information of the newcomer.
    try:
        with open(DEFAULT_DATA_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = DEFAULT_JSON_FORMAT

    info = {
        "name": username,
        "password": password1,
        "balance": DEFAULT_BALANCE,
        "record": []
    }
    data['users'].append(info)

    sort_name(data['users'])

    with open(DEFAULT_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    colored_print(f"Welcome to the Roulette World, {username}!", (66, 245, 212))


def update_balance(manager: Manager, multiplier: int) -> int:
    manager.user.balance += DEFAULT_BET * multiplier
    return manager.user.balance


def save(manager: Manager):
    with open(DEFAULT_DATA_FILE, "r") as f:
        data = json.load(f)

    index = find_user(data['users'], manager.user.name)
    if index != -1:
        data['users'][index]['balance'] = manager.user.balance
        if manager.user.record:
            for i in manager.user.record:
                data['users'][index]['record'].append(i)
    data['isLocked'] = manager.locked
    with open(DEFAULT_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def lock_machine(manager: Manager):
    with open(DEFAULT_DATA_FILE, "r") as f:
        data = json.load(f)
    manager.locked = data['isLocked'] = True
    with open(DEFAULT_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def unlock_machine(manager: Manager):
    with open(DEFAULT_DATA_FILE, "r") as f:
        data = json.load(f)
    manager.locked = data['isLocked'] = False
    manager.login_trial = 0
    with open(DEFAULT_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def log(user: User, game: str, outcome: str):
    current_time = datetime.now()
    user.record.append([current_time.strftime("%c"), game, outcome, user.balance])
