# flake8: noqa

""" broken for now
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import random
import logging

class Card:
  def __init__(self,bot):
      self.log = logging.getLogger(__name__)
      self.currHands = {}
      self.dealer = bot.nickname
      self.handInProgress = False

  @staticmethod
  def getCardUnicode(card):
    uc = [[u"\U0001F0A1",u"\U0001F0A2",u"\U0001F0A3",u"\U0001F0A4",u"\U0001F0A5",u"\U0001F0A6",u"\U0001F0A7",u"\U0001F0A8",u"\U0001F0A9",u"\U0001F0AA",u"\U0001F0AB",u"\U0001F0AC",u"\U0001F0AD",u"\U0001F0AE"],
          [u"\U0001F0D1",u"\U0001F0D2",u"\U0001F0D3",u"\U0001F0D4",u"\U0001F0D5",u"\U0001F0D6",u"\U0001F0D7",u"\U0001F0D8",u"\U0001F0D9",u"\U0001F0DA",u"\U0001F0DB",u"\U0001F0DC",u"\U0001F0DD",u"\U0001F0DE"],
          [u"\U0001F0B1",u"\U0001F0B2",u"\U0001F0B3",u"\U0001F0B4",u"\U0001F0B5",u"\U0001F0B6",u"\U0001F0B7",u"\U0001F0B8",u"\U0001F0B9",u"\U0001F0BA",u"\U0001F0BB",u"\U0001F0BC",u"\U0001F0BD",u"\U0001F0BE"],
          [u"\U0001F0C1",u"\U0001F0C2",u"\U0001F0C3",u"\U0001F0C4",u"\U0001F0C5",u"\U0001F0C6",u"\U0001F0C7",u"\U0001F0C8",u"\U0001F0C9",u"\U0001F0CA",u"\U0001F0CB",u"\U0001F0CC",u"\U0001F0CD",u"\U0001F0CE"],
          [u"\U0001F0A0",u"\U0001F0BF",u"\U0001F0CF",u"\U0001F0DF"]]
    if card:
      return uc[card[0]][card[1]]
    return uc[4][0]

  @staticmethod
  def getCardAscii(card):
    s = [u"\u2660",u"\u2663",u"\u2665",u"\u2666"] # SCHD
    v = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    if card:
      if card[0] < 2:
        return u"\u00031,0[" + s[card[0]] + v[card[1]] + u"]\u000F"
      else:
        return u"\u00034,0[" + s[card[0]] + v[card[1]] + u"]\u000F"
    return "[#]"

  @staticmethod
  def getHand(h):
    return "".join(map(Card.getCardUnicode,h)) + " " + "".join(map(Card.getCardAscii,h))

  def newGame(self):
    self.deck = []
    self.hands = {}
    self.nicks = {}
    self.nicks[self.dealer] = "call"
    self.handInProgress = True
    for i in range(4):
      for d in range(13):
        self.deck.append([i,d])
    random.shuffle(self.deck)
    self.hands[self.dealer] = [self.deck.pop(), self.deck.pop()]

  def blackjackHandValue(self, hand):
    x = 0
    a = 0
    for c in hand:
      if c[1] == 0:
        x += 1
      else:
        a += 1
      x += min(c[1],10)

    if x <= 11 and a  > 0:
      return x+10
    return x

  def __call__(self, bot, e, cmd, *arg):
    if arg[0] == "new":
      self.newGame()
      bot.do_send(e.target, "New Game")
      bot.do_send(e.target, "Dealer: " + Card.getHand([self.hands[self.dealer][0],False]))
      return

    nick = re.sub("!.*","",e.source)
    if self.handInProgress is not True:
      return bot.do_send(nick, "Game not in progress")

    if arg[0] == "deal":
      if nick in self.hands:
        return bot.do_send(nick, "Already dealt in.")
      h = [self.deck.pop(), self.deck.pop()]
      x = self.blackjackHandValue(h)
      self.hands[nick] = h
      self.nicks[nick] = "dealt"
      bot.do_send(nick, "Hand: %s = %d" % (Card.getHand(h), x))
      return

    if nick not in self.hands:
      return bot.do_send(nick, "Not Dealt In")

    if self.nicks[nick] != "dealt":
      return bot.do_send(nick, "Already Called")

    if arg[0] == "hit":
      self.hands[self.dealer].append(self.deck.pop())
      h = self.hands[self.dealer]
      x = self.blackjackHandValue(h)
      if x > 21:
        self.nicks[nick] = "bust"
        return bot.do_send(nick, "BUST!")

      bot.do_send(nick, "Hand: %s = %d" % (Card.getHand(h), x))
      return

    if arg[0] == "call":
      self.nicks[nick] = "call"

      for p in self.nicks:
        if self.nicks[p] == "dealt":
          return

      result = []
      winner = ["Error",0]
      for p in self.nicks:
        v = self.blackjackHandValue(self.hands[p])
        if winner[1] < v:
          winner = [p, v]
        result.append("%s: %s = %d" % (p, Card.getHand(self.hands[p]), v))

      bot.do_send(e.target, "\t".join(result))
      bot.do_send(e.target, "%s is the winner with %d!" % (winner[0], winner[1]))
      return

    bot.do_send(e.target, "Don't know that command")
    #

# Quick Test
def test_all():
    class Bot:
      def __init__(self):
        self.x = 0
        self.nickname = "PlayBot"
      def do_send(self, tar, msg):
        print("(%s) %s" % (tar,msg))

    class E:
      def __init__(self, source):
        self.target = 0
        self.source = source

    b = Bot()
    c = Card(b)
    c.__call__(b, E("jo"), "card", "new")
    c.__call__(b, E("jo"), "card", "deal")
    c.__call__(b, E("jo"), "card", "hit")

    c.__call__(b, E("mi"), "card", "deal")

    c.__call__(b, E("slo"), "card", "deal")
    c.__call__(b, E("slo"), "card", "hit")
    c.__call__(b, E("slo"), "card", "hit")
    c.__call__(b, E("slo"), "card", "hit")
    c.__call__(b, E("slo"), "card", "hit")

    c.__call__(b, E("mi"), "card", "call")
    c.__call__(b, E("jo"), "card", "call")

if __name__ == "__main__":
    test_all()
"""
