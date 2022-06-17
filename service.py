import daemon
from discord_bot import bot_start

from spam import do_main_program

with daemon.DaemonContext():
    bot_start()
