import irc.bot
import logging
import ssl
import time
import re

class PlayBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channels, nickname, password, server, port=6667,
                 force_ssl=False, server_password=None):
        if force_ssl or port == 6697:
            factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
            super(PlayBot, self).__init__([(server, port, server_password)],
                                            nickname, nickname,
                                            connect_factory=factory)
        else:
            super(PlayBot, self).__init__([(server, port, server_password)],
                                            nickname, nickname)
        self.commands = {}
        self.channel_list = channels
        self.nickname = nickname
        self.password = password
        self.log = logging.getLogger('playbot')

    def register_command(self, name, obj):
        self.commands[name] = obj

    def on_nicknameinuse(self, c, e):
        self.log.info('Nick previously in use, recovering.')
        c.nick(c.get_nickname() + "_")
        time.sleep(1)
        self.log.info('Nick previously in use, recovered.')

    def on_welcome(self, c, e):
        for channel in self.channel_list:
            c.join(channel)
            self.log.info('Joined channel %s' % channel)
            time.sleep(0.5)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0], *e.arguments[1:])

    def on_pubmsg(self, c, e):
        msg = e.arguments[0]
        msg = msg.replace(':', ' ', 1)
        msg = re.sub("[ \t]+", " ", msg).split(" ")
        nick = msg[0]
        if nick.lower() == self.connection.get_nickname().lower():
            self.do_command(e, msg[1], *msg[2:])
        return

    def on_dccmsg(self, c, e):
        c.privmsg("You said: " + e.arguments[0])

    def do_command(self, e, cmd, *arg):
        if cmd == 'help':
            cmdStr = "commands: help " + " ".join(self.commands.keys())
            self.do_send(e.target, cmdStr)

        elif cmd in self.commands:
            c = self.commands[cmd]
            try:
                c(self, e, cmd, *arg)
            except Exception as err:
                self.log.warn('Exception thrown from command: %s %s', str(cmd), err)
                self.do_send(e.target, "Huh?")
        else:
            nick = e.source
            c = self.connection
            c.notice(nick, "Not understood: " + cmd)

    def do_send(self, channel, msg):
        self.log.info('Sending "%s" to %s' % (msg, channel))
        try:
            self.connection.privmsg(channel, msg)
            time.sleep(0.5)
        except Exception:
            self.log.exception('Exception sending message:')
            self.reconnect()


