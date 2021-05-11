import json

from static_data import DEFAULT_BALANCE, DEFAULT_DATA_FILE, DEFAULT_BET, RECORD
from utility import colored_print, change_background_color


class User:
    """
    Maintain the current logged-in user's information

    These are variables controlled by the class:
        * name: username
        * balance: balance
        * record: a list of game record
        * data_index: an index value where the user is located at the 'data.json' file.
    """
    def __init__(self, name="", balance=DEFAULT_BALANCE, index=-1):
        self.name = name
        self.balance = balance
        self.record = []  # DateTime/Username/Game/Win or Lose/balance
        self.data_index = index

    def is_online(self) -> bool:
        """
        Check whether a user logged in or not
        Returns True or False based on the User instance's situation
        Because until a user log in, the User instance is an empty instance
        :return: True, if the user is online
                 False, otherwise
        """
        return self.name != ""

    def is_affordable(self) -> bool:
        """
        Check whether a user has enough balance
        Returns True or False based on the balance
        :return: True, if the balance is enough to afford a bet
                 False, otherwise
        """
        return self.balance >= DEFAULT_BET

    def is_valid_index(self) -> bool:
        """
        Check whether the 'data_index' is valid or not
        :return: True, if the 'data_index' is valid
                 False, otherwise
        """
        return self.data_index != -1

    def display_record(self):
        """
        Display a record and state of a user
        This prints:
            - Username
            - Balance
            - Statistics (Total Game, # of Wins, # of Loses)
            - Log (record)
        :return: None
        """
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
