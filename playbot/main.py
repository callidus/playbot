import bot
from plugins import dice
from plugins import say
from plugins import control
from plugins import CvH
from plugins import fortune
from plugins import card

import logging

name = "Bot_KimDev"
server = "irc.afternet.org"
chans = ["""#pixelpit""",]
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
    
    cardGame = card.Card(b)
    b.register_command('card', cardGame)
    
    b.start()

if __name__ == "__main__":
    main()
