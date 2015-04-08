import logging


class Say(object):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def __call__(self, bot, e, cmd, *arg):
        msg = ""
        if len(arg) == 0:
            msg = "say what?"
        else:
            msg = " ".join(arg)

        self.log.info("Saying: '%s'", msg)
        bot.do_send(e.target, msg)
