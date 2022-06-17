import daemon
from discord_bot import bot_start

with daemon.DaemonContext():
    bot_start()
