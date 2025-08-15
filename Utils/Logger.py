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

    @staticmethod
    def log(logType, text):
        logType = logType.upper()
        # print(f"{Fore.RED}{logType} {text} {Logger.config.get(logType, True)}") # logging
        if Logger.config.get(logType, True):
            color = Logger.white # resets the color
            match logType:
                case "SERVER": color = Logger.yellow
                case "CLIENT": color =  Logger.lightblue
                case "ERROR": color = Logger.red
                case "TRANSACTION": color = Logger.green
                case "DEBUG": color = Logger.blue
            print(f"{color}[{logType}] {text}")
                