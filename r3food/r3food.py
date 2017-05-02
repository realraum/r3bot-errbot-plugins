from errbot import BotPlugin, botcmd, arg_botcmd, webhook


class R3food(BotPlugin):
    """
    realraum collaborative food ordering system
    """

    def callback_connect(self):
        if 'listeners' not in self:
            self['listeners'] = []
        if 'emails' not in self:
            self['emails'] = dict()

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports

        You should delete it if your plugin doesn't use any configuration like this
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
        with self.mutable('listeners') as l:
            if nickname not in l:
                l.append(nickname)
                return 'added {} to !food listeners!'.format(nickname)
            else:
                return '{} already a !food listener!'.format(nickname)

    @arg_botcmd('nickname', type=str, unpack_args=False, nargs='?')
    def listeners_remove(self, msg, args):
        nickname = args.nickname if args.nickname else msg.frm
        with self.mutable('listeners') as l:
            if nickname in l:
                l.remove(nickname)
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
        with self.mutable('emails') as l:
            if nickname not in l:
                l[nickname] = args.email
                return 'added {} to !food email listeners!'.format(args.email)
            else:
                return '{} already a !food email listener!'.format(nickname)

    @arg_botcmd('email', type=str, unpack_args=False)
    def emails_remove(self, msg, args):
        nickname = str(msg.frm)
        with self.mutable('emails') as l:
            if nickname in l:
                del l[nickname]
                return 'removed {} from !food email listeners!'.format(
                    nickname)
            else:
                return '{} not a !food email listener!'.format(nickname)

    @arg_botcmd('url', type=str, unpack_args=False, nargs='?')
    @arg_botcmd('--later', type=bool, default=False, unpack_args=False)
    def food(self, message, args):
        """Let food happen."""

        if 'cnt' in self:
            self['cnt'] += 1
        else:
            self['cnt'] = 0

        return args, self['cnt']
