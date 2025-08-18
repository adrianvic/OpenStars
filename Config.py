import json
from Utils.Logger import Logger

config = {}

asciiart = r"""+---------+
|OpenStars|
|  *   *  | Version 1.0
|** *   * | fork by tenkuma
|    **  *| Under GPL-3.0 license
|      *  | Originally by PhoenixFire6934
|    *   *|
|     *   | Special thanks to:
|         | athemm
|  **     | CrazorTheCat
|*        | 8-bitHacc
| *       |
|         |
|       * |
+---------+"""

def load_config():
    global config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        Logger.log('error', 'config.json file not found')
    except json.JSONDecodeError:
        Logger.log('error', 'config.json file is not valid JSON')