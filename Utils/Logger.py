from colorama import Fore
import json

class Logger:
    config = json.loads(open("logging.json", "r").read())
    yellow = Fore.YELLOW
    blue = Fore.BLUE
    lightblue = Fore.LIGHTBLUE_EX
    red = Fore.RED
    green = Fore.GREEN
    white = Fore.WHITE
    magenta = Fore.MAGENTA
    lightgreen = Fore.LIGHTGREEN_EX
    lightmagenta = Fore.LIGHTMAGENTA_EX
    cyan = Fore.CYAN

    @staticmethod
    def log(logType, text, dryRun = False):
        logType = logType.upper()
        # print(f"{Fore.RED}{logType} {text} {Logger.config.get(logType, True)}") # logging
        if (Logger.config.get(logType, True)) == "True" or logType == "*":
            color = Fore.RESET
            match logType:
                case "SERVER": color = Logger.magenta
                case "CLIENT": color =  Logger.lightblue
                case "ERROR": color = Logger.red
                case "TRANSACTION": color = Logger.green
                case "DEBUG": color = Logger.blue
                case "WARNING": color = Logger.yellow
                case "NETWORK CLIENT": color = Logger.lightgreen
                case "NETWORK SERVER": color = Logger.lightmagenta
                case "CONSOLECOMMAND": color = Logger.cyan
            msg = f"[{logType}] {text}"
            if not dryRun: print(f"{Fore.RESET}{color}{msg}", flush=True)
            return msg