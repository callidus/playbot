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
  
  @staticmethod    
  def getCardUnicode(card):
    uc = [["\U0001F0A1","\U0001F0A2","\U0001F0A3","\U0001F0A4","\U0001F0A5","\U0001F0A6","\U0001F0A7","\U0001F0A8","\U0001F0A9","\U0001F0AA","\U0001F0AB","\U0001F0AC","\U0001F0AD","\U0001F0AE"],
          ["\U0001F0D1","\U0001F0D2","\U0001F0D3","\U0001F0D4","\U0001F0D5","\U0001F0D6","\U0001F0D7","\U0001F0D8","\U0001F0D9","\U0001F0DA","\U0001F0DB","\U0001F0DC","\U0001F0DD","\U0001F0DE"],
          ["\U0001F0B1","\U0001F0B2","\U0001F0B3","\U0001F0B4","\U0001F0B5","\U0001F0B6","\U0001F0B7","\U0001F0B8","\U0001F0B9","\U0001F0BA","\U0001F0BB","\U0001F0BC","\U0001F0BD","\U0001F0BE"],
          ["\U0001F0C1","\U0001F0C2","\U0001F0C3","\U0001F0C4","\U0001F0C5","\U0001F0C6","\U0001F0C7","\U0001F0C8","\U0001F0C9","\U0001F0CA","\U0001F0CB","\U0001F0CC","\U0001F0CD","\U0001F0CE"],
          ["\U0001F0A0","\U0001F0BF","\U0001F0CF","\U0001F0DF"]]
    if card:
      return uc[card[0]][card[1]]
    return uc[4][0]

  @staticmethod
  def getCardAscii(card):
    s = ["\u2660","\u2663","\u2665","\u2666"] # SCHD
    v = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    if card:
      if s < card[0]:
        return "\u00031,0[" + s[card[0]] + v[card[1]] + "]\u000F"
      else:
        return "\u00034,0[" + s[card[0]] + v[card[1]] + "]\u000F"
    return "[#]"
  
  @staticmethod
  def getHand(h):
    return "".join(map(Card.getCardUnicode,h)) + " " + "".join(map(Card.getCardAscii,h))
    
  def newGame(self):
    self.deck = []
    self.hands = {}
    self.nicks = {}
    self.handInProgress = True
    for i in range(4):
      for d in range(13):
        self.deck.append([i,d]);
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
    if cmd == "new":
      self.newGame()
      bot.do_send(e.target, "New Game")
      bot.do_send(e.target, "Dealer: " + Card.getHand([self.hands[self.dealer][0],False]))
      return

    nick = re.sub("!.*","",e.source)
    if self.handInProgress is not True:
      return bot.do_send(nick, "Game not in progress")

    if cmd == "deal":
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

    if cmd == "hit":
      self.hands[self.dealer].append(self.deck.pop())
      h = self.hands[self.dealer]
      x = self.blackjackHandValue(h)
      if x > 21:
        self.nicks[nick] = "bust"
        return bot.do_send(nick, "BUST!")

      bot.do_send(nick, "Hand: %s = %d" % (Card.getHand(h), x))
      return

    if cmd == "call":
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
    c.__call__(b, E("jo"), "new")
    c.__call__(b, E("jo"), "deal")
    c.__call__(b, E("jo"), "hit")

    c.__call__(b, E("mi"), "deal")

    c.__call__(b, E("slo"), "deal")
    c.__call__(b, E("slo"), "hit")
    c.__call__(b, E("slo"), "hit")
    c.__call__(b, E("slo"), "hit")
    c.__call__(b, E("slo"), "hit")

    c.__call__(b, E("mi"), "call")
    c.__call__(b, E("jo"), "call")

if __name__ == "__main__":
    test_all()
