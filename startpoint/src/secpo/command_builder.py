""" This module is created by Martin Vasko.
    CommandBuilder purpose is to easily concatenate commands in form of strings
    to write them inside files.
"""


class CommandBuilder:
    RUN = 'RUN'

    def __init__(self, *args):
        """ Initialize command to empty string or based on arguments given. """
        self._commands = ''
        for arg in args:
            if isinstance(arg, str):
                if len(args) > 1:
                    self._commands += arg + ' '
                else:
                    self._commands += arg

    def __add__(self, other):
        """
        Adds two CommandBuilder or CommandBuilder and string. Returns
        CommandBuilder.
        :param other: CommandBuilder or string that should be concatenated as
                      command that will be written inside file.
        :return: CommandBuilder that contains other commands.
        """
        # Add two command builder together
        if isinstance(other, CommandBuilder):
            if not other._commands:
                return CommandBuilder(self._commands)
            return CommandBuilder(self._commands + other._commands + '\n')
        if self.RUN in self._commands:
            return CommandBuilder(self._commands + other + ' ')
        return CommandBuilder(self._commands + other + '\n')

    def __str__(self):
        return self._commands
