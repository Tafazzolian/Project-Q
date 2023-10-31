import datetime
import pytz



class Tools:

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

    @staticmethod
    def now() -> datetime.datetime:
        return datetime.datetime.now(pytz.timezone("Asia/Tehran"))
    
    @staticmethod
    def green(text, key=""):
        GREEN = '\033[32m'
        RESET = '\033[0m'
        return print(f'{GREEN}{key}{text}{RESET}')
    
    @staticmethod
    def red(text, key=""):
        RED = '\033[31m'
        RESET = '\033[0m'
        return print(f'{RED}{key}{text}{RESET}')
    
    @staticmethod
    def yellow(text, key=""):
        YELLOW = '\033[33m'
        RESET = '\033[0m'
        return print(f'{YELLOW}{key}{text}{RESET}')
    
    @staticmethod
    def blue(text, key=""):
        BLUE = '\033[34m'
        RESET = '\033[0m'
        return print(f'{BLUE}{key}{text}{RESET}')
    