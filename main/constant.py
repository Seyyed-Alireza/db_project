from enum import IntEnum
from colorama import Fore, Style

class EventType(IntEnum):
    WINDOW_BLUR = 0
    WINDOW_FOCUS = 1
    FIRST_RESOLUTION = 2
    WINDOW_HIDDEN = 3
    WINDOW_VISIBLE = 4
    QUESTION_DESCRIPTIVE = 5
    QUESTION_MULTIPLE_CHOICE = 6

class Colors:
    INFO = Fore.CYAN
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    DEBUG = Fore.MAGENTA
    
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT