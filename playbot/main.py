
from __future__ import absolute_import

from playbot import bot
from playbot.plugins import card
from playbot.plugins import control
from playbot.plugins import CvH
from playbot.plugins import dice
from playbot.plugins import fortune
from playbot.plugins import say
from playbot.plugins import link_peek

import logging

name = "PlayBot"
server = "irc.afternet.org"
chans = ["""#testroom""", ]
port = 6697


def setup_logging():
    logging.basicConfig(level=logging.INFO)


def main():
    setup_logging()
    b = bot.PlayBot(chans, name, None, server, port)
    b.register_command("disconnect", control.Disconnect())
    b.register_command("die", control.Die())

    cvh = CvH.App.CvH()
    cvh.setup('./cvh.db')
    b.register_command("cvh", cvh)

    ftn = fortune.fortune.Fortune('./fortune.db')
    b.register_command('fortune', ftn)

    why = fortune.fortune.Fortune("./bofh.db")
    b.register_command('why', why)

    roll = dice.Dice()
    b.register_command('roll', roll)

    sayer = say.Say()
    b.register_command('say', sayer)

    #cardGame = card.Card(b)
    #b.register_command('card', cardGame)

    b.register_listner(link_peek.peek)

    b.start()

if __name__ == "__main__":
    main()
