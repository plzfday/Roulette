import json
from datetime import datetime

from static_text import RECORD
from utility import colored_print

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
        print("Log:")
        print("{:<26} {:<15} {:<10} {:<10}".format('Date', 'Game', 'Result', 'Balance'))
        with open(DEFAULT_DATA_FILE, "r") as f:
            data = json.load(f)
            for user in data['users']:
                if user['name'] == self.name:
                    for i in user['record']:
                        print("{:<26} {:<15} {:<10} {:<10}".format(i[0], i[1], i[2], i[3]))
        for i in self.record:
            print("{:<26} {:<15} {:<10} {:<10}".format(i[0], i[1], i[2], i[3]))
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
            found_user = False
            for user in data['users']:
                if user['name'] == username and user['password'] == password:
                    colored_print(f"Welcome, {username}", (66, 245, 212))
                    manager.user = User(username, user['balance'])
                    found_user = True
                    manager.login_trial = 0
                    break
            if not found_user:
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


def signup() -> User:
    # Sign Up UI
    colored_print("? ", (0, 255, 0), end='')
    username = input("Username: ")
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

    with open(DEFAULT_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    colored_print(f"Welcome to the Roulette World, {username}!", (66, 245, 212))


def update_balance(manager: Manager, multiplier: int) -> int:
    manager.user.balance += DEFAULT_BET * multiplier
    # if manager.user.balance == 0:
    #     colored_print("Sorry. You don't have enough money. Please top up.", (255, 0, 0))
    #     input()
    return manager.user.balance


def save(manager: Manager):
    with open(DEFAULT_DATA_FILE, "r") as f:
        data = json.load(f)
    for user in data['users']:
        if user['name'] == manager.user.name:
            user['balance'] = manager.user.balance
            if manager.user.record:
                for i in manager.user.record:
                    user['record'].append(i)
            break
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
