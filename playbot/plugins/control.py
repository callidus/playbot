class Disconnect:
    def __call__(self, bot, e, cmd, *arg):
        bot.disconnect()

class Die:
    def __call__(self, bot, e, cmd, *arg):
        bot.die()

