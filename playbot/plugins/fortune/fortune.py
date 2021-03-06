
from __future__ import absolute_import

from playbot.plugins.fortune import data_source

import logging
import os
import random


class Fortune(object):
    def __init__(self, db, prefix=None):
        self.data = data_source.DataSource()
        if os.path.isfile(db):
            self.data.open_db(db)
        else:
            self.data.build_db(db)

        self.maxIdx = self.data.get_count()-1
        self.prefix = prefix

        self.log = logging.getLogger(__name__)
        self.log.info("Fortune loaded db: %s with %i entries.",
                      db, self.maxIdx)

    def __call__(self, bot, e, cmd, *args):
        idx = random.randint(0, self.maxIdx)
        msg = self.data.get_fortune(idx)
        if self.prefix is not None:
            bot.do_send(e.target, self.prefix + " " + msg)
        else:
            bot.do_send(e.target, msg)
