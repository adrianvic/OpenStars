from Core.Networking.Server import Server
import json  # meh
from Utils.Logger import Logger

from Utils.Updater import Updater


class Main:
    def __init__(self):
        self.crashCount: int = 0
        self.configuration = json.loads(open("config.json", "r").read())
        self.useUpdater = self.configuration.get("UpgradesEnabled", False)
        self.main()
        self.updater: Updater = None

    def main(self):
        if self.useUpdater: self.updater = Updater()  # Execute deadly weapons

        if self.useUpdater and not self.updater.updateInstalled and self.crashCount >= 2:
            Logger.log("debug", "No fixes are available for the crashes. Shutting down server...")
            exit()

        try:
            print(Logger.yellow + r"""+---------+
|OpenStars|
|  *   *  | Version 1.0
|** *   * | By tenkuma
|    **  *| Under GPL-3.0 copyleft license
|      *  |
|    *   *|
|     *   |
|         |
|  **     |
|*        |
| *       |
|         |
|       * |
+---------+""")

            Server("0.0.0.0", 9339).start()
        except ImportError:
            Logger.log("error", "Some modules are missing, please run pip install -r requirements.txt on your terminal to install them.")

        except Exception as e:
            Logger.log("error", f"Encountered exception: {e}")
            Logger.log("error", f"Exception type:", type(e).__name__)
            if self.useUpdater:
                self.crashCount += 1

                if self.crashCount >= 2:
                    # TODO: Close all connections so that the server gets a bit faster on fixing stuff
                    req = "yes" in input("The server has crashed 2+ times."
                                         " Would you like to check for updates in case there's a fix? ").lower()
                    if req: self.main()

                updaterRollbackRequest: bool = "yes" in input(
                    f"The Updater has detected that the server is in a crashed state (error: {e}).\n"
                    "Would you like to roll-back the update? ").lower()

                if updaterRollbackRequest:
                    self.updater.performRollback()
                    Logger.log("debug", "The roll-back has been completed successfully!")
                    self.crashCount = 0
                else:
                    Logger.log("debug", "Request declined. Restarting server...\n")

                self.main()


if __name__ == '__main__':
    Main()
