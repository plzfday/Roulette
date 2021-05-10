import json

from static_data import DEFAULT_BALANCE, DEFAULT_DATA_FILE, RECORD
from utility import colored_print, change_background_color


class User:
    def __init__(self, name="", balance=DEFAULT_BALANCE, index=-1):
        self.name = name
        self.balance = balance
        self.record = []  # DateTime/Username/Game/Win or Lose/balance
        self.data_index = index

    def is_online(self) -> bool:
        return self.name != ""

    def is_affordable(self) -> bool:
        return self.balance >= 10

    def is_valid_index(self) -> bool:
        return self.data_index != -1

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
            if self.is_valid_index():
                for i in data['users'][self.data_index]['record']:
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
            print(f"Total {count_games}G {count_victory}W {count_defeat}L \
                    ({round(count_victory / count_games * 100, 2)}%)")
            print("{:<26} {:<15} {:<10} {:<7}".format('Date', 'Game', 'Result', 'Balance'))
            for i in display_list[::-1]:
                if i[2] == 'W':
                    change_background_color((31, 142, 205))
                elif i[2] == 'L':
                    change_background_color((238, 90, 82))
                print("{:<26} {:<15} {:<10} {:<7}\033[0m".format(i[0], i[1], i[2], i[3]))
        else:
            print("There are no results recorded.")
        input()
