from termcolor import colored


def putColor(text, color):
    return colored(text, color, attrs=['bold'])
