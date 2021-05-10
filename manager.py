import json
from datetime import datetime
from getpass import getpass

from data_manipulation import sort_name, find_user
from hash import check_hash, hash_password
from static_data import DEFAULT_DATA_FILE, DEFAULT_BALANCE, DEFAULT_BET, DEFAULT_JSON_FORMAT
from user import User
from utility import system_notification


def signup():
    # Sign Up UI
    username = input("Username: ")
    try:
        with open(DEFAULT_DATA_FILE, "r") as f:
            data = json.load(f)
            if find_user(data['users'], username) != -1:
                system_notification("[The name is already taken]", (255, 0, 0))
                username = input("Username: ")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    password1 = getpass("Password: ")
    password2 = getpass("Confirm Password: ")
    while password1 != password2:
        password2 = input("[Doesn't Match] Confirm Password: ")

    password = hash_password(password1)

    # Load data file and append information of the newcomer.
    try:
        with open(DEFAULT_DATA_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = DEFAULT_JSON_FORMAT

    info = {
        "name": username,
        "password": password,
        "balance": DEFAULT_BALANCE,
        "record": []
    }
    data['users'].append(info)

    sort_name(data['users'])

    with open(DEFAULT_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    system_notification(f"Welcome to the Roulette World, {username}!", (66, 245, 212))


class Manager:
    def __init__(self, user=User()):
        self.user = user
        self.login_trial = 0
        self.agree = False
        try:
            with open(DEFAULT_DATA_FILE, "r") as f:
                data = json.load(f)
                if 'isLocked' in data:
                    self.locked = data['isLocked']
        except:
            self.locked = False

    def login(self):
        # Login UI
        username = input("Username: ")
        password = getpass()
        # Find User
        try:
            with open(DEFAULT_DATA_FILE, "r") as f:
                data = json.load(f)
                index = find_user(data['users'], username)
                if index != -1 and check_hash(data['users'][index]['password'], password):
                    system_notification(f"Welcome, {username}", (66, 245, 212))
                    self.user = User(username, data['users'][index]['balance'], index)
                    self.login_trial = 0
                else:
                    self.login_trial += 1
                    if self.login_trial > 2:
                        system_notification("[MACHINE LOCKED] Please contact an administrator to unlock the machine.",
                                            (255, 0, 0))
                        self.lock_machine()
                    else:
                        system_notification(f"Username or Password is incorrect.\n"
                                            f"You can try {3 - self.login_trial} time(s) more.", (66, 245, 212))
        except FileNotFoundError:
            system_notification("There is no registered user. Please sign up first.", (255, 0, 0))
        except json.JSONDecodeError:
            system_notification("ERROR(login-file is unstable)", (255, 0, 0))

    def logout(self):
        self.save()
        self.agree = False
        del self.user
        self.user = User()

    def update_balance(self, multiplier: int) -> int:
        self.user.balance += DEFAULT_BET * multiplier
        return self.user.balance

    def save(self):
        with open(DEFAULT_DATA_FILE, "r") as f:
            data = json.load(f)

        if self.user.is_valid_index():
            data['users'][self.user.data_index]['balance'] = self.user.balance
            if self.user.record:
                for i in self.user.record:
                    data['users'][self.user.data_index]['record'].append(i)
        data['isLocked'] = self.locked
        with open(DEFAULT_DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def lock_machine(self):
        with open(DEFAULT_DATA_FILE, "r") as f:
            data = json.load(f)
        self.locked = data['isLocked'] = True
        with open(DEFAULT_DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def unlock_machine(self):
        with open(DEFAULT_DATA_FILE, "r") as f:
            data = json.load(f)
        self.locked = data['isLocked'] = False
        self.login_trial = 0
        with open(DEFAULT_DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def log(self, manager: str, outcome: str):
        current_time = datetime.now()
        self.user.record.append([current_time.strftime("%c"), manager, outcome, self.user.balance])
