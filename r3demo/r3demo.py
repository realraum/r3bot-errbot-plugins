from errbot import BotPlugin, botcmd, arg_botcmd, webhook
from errbot.backends.irc import IRCRoom

class R3demo(BotPlugin):
    """
    plugin to demo errbot stuff
    """

    def activate(self):
        """
        Triggers on plugin activation

        You should delete it if you're not using it to override any default behaviour
        """
        super(R3demo, self).activate()

    def deactivate(self):
        """
        Triggers on plugin deactivation

        You should delete it if you're not using it to override any default behaviour
        """
        super(R3demo, self).deactivate()

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports

        You should delete it if your plugin doesn't use any configuration like this
        """
        return {'EXAMPLE_KEY_1': "Example value",
                'EXAMPLE_KEY_2': ["Example", "Value"]
                }

    def check_configuration(self, configuration):
        """
        Triggers when the configuration is checked, shortly before activation

        Raise a errbot.utils.ValidationException in case of an error

        You should delete it if you're not using it to override any default behaviour
        """
        super(R3demo, self).check_configuration(configuration)

    def callback_connect(self):
        """
        Triggers when bot is connected

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    def callback_message(self, message):
        """
        Triggered for every received message that isn't coming from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        # self.send(
        #         message.frm,
        #         "r3demo: callback_message",
        #     )
        pass

    def callback_botmessage(self, message):
        """
        Triggered for every message that comes from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        # self.send(
        #         message.frm,
        #         "r3demo: callback_botmessage",
        #     )
        pass

    @botcmd()
    def r3room(self, msg, args):
        room = msg.to
        if not isinstance(room, IRCRoom):
            return 'you are not in a room ...'
        people = map(lambda x: x.nick, room.occupants)
        return """room: {} ({})
        occupants: {}
        """.format(str(room), type(room), ', '.join(people))

    @botcmd()
    def r3me(self, msg, args):
        frm = msg.frm
        return """nick: {}
        user: {}
        host: {}
        client: {}
        fullname: {}
        """.format(frm.nick, frm.user, frm.host, frm.client, frm.fullname)

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def r3demo(self, message, args):
        """A command which simply returns 'Example'"""
        return "Example message from r3demo ..."

    @arg_botcmd('name', type=str)
    @arg_botcmd('--favorite-number', type=int, unpack_args=False)
    def r3hello(self, message, args):
        """
        A command which says hello to someone.

        If you include --favorite-number, it will also tell you their
        favorite number.
        """
        if args.favorite_number is None:
            return "Hello {name}".format(name=args.name)
        else:
            return "Hello {name}, I hear your favorite number is {number}".format(
                name=args.name, number=args.favorite_number, )
