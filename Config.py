import json

config = {}

def load_config():
    global config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("Loaded configuration:", config)
    except FileNotFoundError:
        print("Error: config.json file not found.")
    except json.JSONDecodeError:
        print("Error: config.json file is not valid JSON.")