import random
import logging

class Dice:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def __call__(self, bot, e, cmd, *arg):
        msg = ""
        if len(arg) == 0:
            msg = "roll some dice, e.g. 'roll 2d6-2'"
        else:
            num, max = arg[0].lower().split('d')
            mod = 0
            val = []

            if '-' in max:
                max, mod = max.split('-')
                mod = -int(mod)
            elif '+' in max:
                max, mod = max.split('+')
                mod = int(mod)

            for i in range(0,int(num)):
                r = random.randint(1,int(max))
                val.append(r)

            val.sort()
            msg = "%s = %i [%s]" % (
                arg[0], 
                sum(val)+mod, 
                " ".join([str(v) for v in val]))

        bot.do_send(e.target, msg)
