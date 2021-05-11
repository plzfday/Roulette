def colored_print(text: str, rgb: (int, int, int), end='\n'):
    """
    Print a text with font colouring
    Only affect a given text
    :param text: Source text to be printed out
    :param rgb: RGB color code
    :param end: end character
    :return: None
    """
    change_color(rgb)
    print(text, end=end)
    reset_color()


def change_color(rgb: (int, int, int)):
    """
    Change font colour
    :param rgb: RGB color code
    :return:
    """
    print(f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m", end='')


def change_background_color(rgb: (int, int, int)):
    """
    Change font's background colour
    :param rgb: RGB color code
    :return:
    """
    print(f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m", end='')


def reset_color():
    """
    Reset the current colouring
    :return: None
    """
    print("\033[0m", end='')


def colored_input(rgb: (int, int, int)) -> str:
    """
    Get input with '> ' character front
    :param rgb: RGB color code
    :return: Entered input string
    """
    change_color(rgb)
    ret = input("> ")
    reset_color()
    return ret


def system_notification(text: str, rgb: (int, int, int)):
    """
    Print a text with font colouring but also wait user's typing so that a user won't miss notification
    :param text: Source text
    :param rgb: RGB color code
    :return: None
    """
    colored_print(text, rgb)
    input()
