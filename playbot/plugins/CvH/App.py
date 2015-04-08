import os
import random

import DataSource


class Phrase(object):
    def __init__(self, data):
        self.title = data[0]
        self.text = data[1]
        self.numSlots = int(data[2])
        self.slots = []

    def fillSlot(self, data):
        self.slots.append(data[1])

    def __str__(self):
        string = self.text
        if self.numSlots:
            for slot in self.slots:
                string = string.replace("__________", slot, 1)
        else:
            string += " ... " + self.slots[0]
        return string


class CvH(object):
    def __init__(self):
        self.dataSource = DataSource.DataSource()

    def setup(self, path):
        if os.path.isfile(path):
            self.dataSource.openDB(path)
        else:
            self.dataSource.buildDB(path)

        self.blacks = self.dataSource.getBlackCards()
        self.whites = self.dataSource.getWhiteCards()

    def __call__(self, bot, e, cmd, *args):
        idx = random.randint(0, len(self.blacks))
        phrase = Phrase(self.dataSource.getBlackCard(self.blacks[idx][0]))
        for x in range(0, max(phrase.numSlots, 1)):
            idx = random.randint(0, len(self.whites))
            phrase.fillSlot(self.dataSource.getWhiteCard(self.whites[idx][0]))

        bot.do_send(e.target, str(phrase))
