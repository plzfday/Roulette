def colored_print(text: str, rgb: (int, int, int), end='\n'):
    change_color(rgb)
    print(text, end=end)
    reset_color()


def change_color(rgb: (int, int, int)):
    print(f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m", end='')


def change_background_color(rgb: (int, int, int)):
    print(f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m", end='')


def reset_color():
    print("\033[0m", end='')


def colored_input(rgb: (int, int, int)) -> str:
    change_color(rgb)
    ret = input("> ")
    reset_color()
    return ret
