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
        yield 'we have {} !food listeners: {}'.format(len(listeners), ', '.join(listeners))

    @arg_botcmd('nickname', type=str, unpack_args=False, nargs='?')
    def listeners_add(self, msg, args):
        nickname = args.nickname if args.nickname else msg.frm
        with self.mutable('listeners') as listeners:
            if nickname not in listeners:
                listeners.append(nickname)
                return 'added {} to !food listeners!'.format(nickname)
            else:
                return '{} already a !food listener!'.format(nickname)

    @arg_botcmd('nickname', type=str, unpack_args=False, nargs='?')
    def listeners_remove(self, msg, args):
        nickname = args.nickname if args.nickname else msg.frm
        with self.mutable('listeners') as listeners:
            if nickname in listeners:
                listeners.remove(nickname)
                return 'removed {} from !food listeners!'.format(nickname)
            else:
                return '{} not a !food listener!'.format(nickname)

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

    def notify_listeners(self, sender, url, when):
        when = when if when else 'NOW'
        url = url if url else ''
        listeners = self['listeners']
        # TODO: filter offline users?
        listeners = map(str, listeners)
        listeners = ', '.join(listeners)
        return 'Hey {}, want some food {}? {}'.format(listeners, when, url)

    def notify_email(self, sender, url, when):
        pass

    @arg_botcmd('url', type=str, unpack_args=False, nargs='?')
    @arg_botcmd('--when', type=str, default=False, unpack_args=False)
    def food(self, message, args):
        """Let food happen."""
        sender = str(message.frm)

        yield 'Thanks for the hint! Please give people some time to reply ...'

        self.notify_email(sender, args.url, args.when)
        yield self.notify_listeners(sender, args.url, args.when)




