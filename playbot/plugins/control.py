class Disconnect(object):
    def __call__(self, bot, e, cmd, *arg):
        bot.disconnect()


class Die(object):
    def __call__(self, bot, e, cmd, *arg):
        bot.die()
