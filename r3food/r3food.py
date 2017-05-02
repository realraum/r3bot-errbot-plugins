from errbot import BotPlugin, botcmd, arg_botcmd
from common import mail


class R3food(BotPlugin):
    """
    r3food: realraum collaborative food ordering system
    """

    def callback_connect(self):
        if 'listeners' not in self:
            self['listeners'] = []
        if 'emails' not in self:
            self['emails'] = dict()
        self.mail = None

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports
        """
        return {'stmp-sender': 'r3bot@realraum.at',
                'smtp-server': "changeme",
                'stmp-user': 'changeme',
                'stmp-password': 'changeme'}

    @botcmd
    def listeners_show(self, msg, args):
        listeners = self['listeners']
        # listeners = map(str, listeners)
        yield 'our !food listeners: {}'.format(', '.join(listeners))

    @arg_botcmd('nickname', type=str, unpack_args=False, nargs='?')
    def listeners_add(self, msg, args):
        nickname = args.nickname if args.nickname else str(msg.frm.nick)
        with self.mutable('listeners') as listeners:
            if nickname not in listeners:
                listeners.append(nickname)
                return 'added {} to !food listeners!'.format(nickname)
            else:
                return '{} already a !food listener!'.format(nickname)

    @arg_botcmd('nickname', type=str, unpack_args=False, nargs='?')
    def listeners_remove(self, msg, args):
        nickname = args.nickname if args.nickname else str(msg.frm.nick)
        with self.mutable('listeners') as listeners:
            if nickname in listeners:
                listeners.remove(nickname)
                return 'removed {} from !food listeners!'.format(nickname)
            else:
                return '{} not a !food listener!'.format(nickname)

    @botcmd(admin_only=True)
    def listeners_clear(self, msg, args):
        self['listeners'] = []
        return 'listeners cleared!'

    @botcmd(admin_only=True)
    def emails_clear(self, msg, args):
        self['emails'] = []
        return 'emails cleared!'

    @botcmd
    def emails_show(self, msg, args):
        emails = self['emails']
        emails_text = ', '.join(
            nick + ':' + mail for nick,
            mail in emails.items())
        yield 'we have {} !food emails: {}'.format(len(emails), emails_text)

    @arg_botcmd('email', type=str, unpack_args=False)
    def emails_add(self, msg, args):
        nickname = str(msg.frm)
        with self.mutable('emails') as listeners:
            if nickname not in listeners:
                listeners[nickname] = args.email
                return 'added {} to !food email listeners!'.format(args.email)
            else:
                return '{} already a !food email listener!'.format(nickname)

    @arg_botcmd('email', type=str, unpack_args=False)
    def emails_remove(self, msg, args):
        nickname = str(msg.frm)
        with self.mutable('emails') as listeners:
            if nickname in listeners:
                del listeners[nickname]
                return 'removed {} from !food email listeners!'.format(
                    nickname)
            else:
                return '{} not a !food email listener!'.format(nickname)

    def get_room_occupants(self, msg):
        room = msg.to
        try:
            return list(map(lambda x: str(x.nick), room.occupants))
        except Exception:
            return None

    def notify_listeners(self, sender, url, when, occupants):
        when = when if when else 'NOW'
        url = url if url else ''

        listeners = self['listeners']
        if sender in listeners:
            listeners.remove(sender)

        listeners = filter(lambda user: user in occupants, listeners)

        listeners = map(str, listeners)
        listeners = ', '.join(listeners)
        return 'Hey {} - want some food {}? {}'.format(listeners, when, url)

    def notify_email(self, sender, url, when):
        pass

    @arg_botcmd('url', type=str, unpack_args=False, nargs='?')
    @arg_botcmd('--when', type=str, default=False, unpack_args=False)
    def food(self, message, args):
        """Let food happen."""
        sender = str(message.frm.nick)
        occupants = self.get_room_occupants(message)
        if not occupants:
            yield 'You are not in a #room, right?'
            return

        yield 'Thanks for the hint, {}! Please give people some time to reply ...'.format(sender)

        self.notify_email(sender, args.url, args.when)
        yield self.notify_listeners(sender, args.url, args.when, occupants)
