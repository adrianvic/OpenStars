# OpenStars
Fork of Classic Brawl, a simple Brawl Stars v26.184 server emulator written in Python with support for commands via websocet.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/bc94c258-de76-4245-a722-aa8382585c32" />

## Setting things up
### Requirements:
- Python 3.7 or higher
- pymongo
- pymysql
- dnspython
- colorama

### Database configuration
OpenStars supports SQL and MongoDB, pick one and put your database connection parameters in `config.json`.
```
"DBBackend": "sql or mongodb",
```

### Running the server
In a terminal, type __`pip install -r requirements.txt`__ then __`python Main.py`__.

### Configuring the client app
To connect to your server, a **patched client** is required. We will never provide you a patched client since we are not allowed to. If you're allowed to do so, you can patch it manually, if not, this server is merely a proof of concept of how the server would work.

### OpenStars Web Interface
You can host files from www/OpenStars in any webserver, everything runs locally using JavaScript's websocket capabilities.

### Need help?
Go through this list by order:
1. [Discord](https://discord.gg/bSNvjcee) and GitHub Issues (always create an issue, even when looking for help elsewhere, it helps us to keep track of what we need to fix)
2. [E-mail](mailto:adrianvictor+openstars@disroot.org)
3. Anywhere else you can find me

### Credits
- [PhoenixFire](https://github.com/PhoenixFire6934) - the creator of Classic Brawl.
- [CrazorTheCat](https://github.com/CrazorTheCat) - Contributor and other versions developer.
- [8-bitHacc](https://github.com/8-bitHacc) - Contributor & Developer of new features of Classic Brawl.
- [tenkuma](https://adrianvictor.rf.gd) - Contributor and creator of OpenStars.