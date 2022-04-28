"""
Copyright (C) 2022  Sam Wagenaar

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__all__ = ["InvalidCommandError", "Command", "CommandSet"]
__version__ = "1.0"
__author__ = "Sam Wagenaar"

import typing
import os
from ordered_set import OrderedSet
from colorama import Fore, Style
import helpers
from callbacks import TurtleCallbacks


class InvalidCommandError(AttributeError):
    pass


# Helpers
def arg_names(fun) -> typing.List[str]:
    return fun.__code__.co_varnames[:fun.__code__.co_argcount]


def stylize(string: str, style, reset):
    inside = False
    while "```" in string:
        string = string.replace("```", reset if inside else style, 1)
        inside = not inside
    return string


def get_command_name(string: str):
    return string.split(" ")[0]


arg_col = Fore.BLUE


class HistoryKeeper:
    def __init__(self):
        self.history = []

    def reset(self):
        self.history.clear()

    def remove_last(self):
        if len(self.history) > 0:
            return self.history.pop(-1)

    def add(self, command: str):
        if command == "reset" or get_command_name(command) == "load":
            self.reset()
        elif command != "undo" and get_command_name(command) != "help":
            self.history.append(command)

    def save(self, name: str):
        """Saves history to file

        :param name: File to save to
        :return: None
        """
        name = os.path.basename(name).split(".")[0]+".txt"
        file_path = helpers.external_path(os.path.join("saves", name))
        out = ""
        for command in self.history:
            out += command + "\n"
        f = open(file_path, "w")
        f.write(out)
        f.close()

    def load(self, name: str):
        """Loads history from file

        :param name: File to load from
        :return: None
        """
        name = os.path.basename(name).split(".")[0]+".txt"
        file_path = helpers.external_path(os.path.join("saves", name))
        if not os.path.exists(file_path):
            file_path = helpers.resource_path(os.path.join("assets", "builtin_saves", name))
        if not os.path.exists(file_path):  # Make sure the error is with the normal path if it fails to locate
            file_path = helpers.external_path(os.path.join("saves", name))
        file_path = os.path.abspath(file_path)
        contents = open(file_path).read().split("\n")
        # Don't reset until after file confirmed exists
        self.reset()
        for command in contents:
            if command != "" and command != "quit" and command != "exit":
                self.add(command)


# End Helpers


class Command:
    """Takes text input and calls function with typed arguments"""

    def __init__(self,
                 name: str,
                 help_msg: str,
                 num_args: int,
                 types: typing.List[type],
                 callback: typing.Callable[[...], typing.Any],
                 callback_args: typing.List = None):
        """Initialize a command

        :param name: name of command
        :param help_msg: help message to display
        :param num_args: number of arguments the user should give
        :param types: types the arguments will be converted to
        :param callback: function to run
        :param callback_args: preset arguments to give callback automatically
        """
        self.name = name
        self.help_msg = help_msg
        self.num_args = num_args
        self.types = types
        self.callback = callback
        if callback_args is None:
            callback_args = []
        self.callback_args = callback_args
        if len(self.types) != self.num_args:
            raise InvalidCommandError("Each argument needs a type")
        self.show_help = True  # True by default, require command set to modify if applicable

    def execute(self, string: str) -> typing.Any:
        """Execute the command based on user input.

        :param string: User input
        :return: Any
        """
        parts = string.split(" ")
        if parts[0] != self.name:
            raise InvalidCommandError(f"Called execute on command {self.name}, should call on {parts[0]}")
        parts = parts[1:]
        if len(parts) != self.num_args:
            raise InvalidCommandError(f"Wrong number of arguments, got {len(parts)}, expected {self.num_args}")
        args = []
        for i in range(self.num_args):
            args.append(self.types[i](parts[i]))
        return self.callback(*self.callback_args, *args)


class CommandSet:
    """Manage a set of commands.

    Intended use is to only use one CommandSet.
    However, this can be used to create sub-commands.
    """

    def __init__(self, output: typing.Callable[[str], None], callbacks: TurtleCallbacks):
        """Initialize an empty CommandSet"""
        self.commands = {}
        self.register(Command("help", "Display help for all commands", 0, [], self.help))
        self.register(Command("help", "Display help for specified ```command```", 1, [str], self.help))
        self.help_break()

        self.register(Command("save", "Save current drawing to ```file```", 1, [str], self.save))
        self.register(Command("load", "Load drawing from ```file```", 1, [str], self.load))
        self.help_break()

        self.register(Command("undo", "Undo previous command (does not work on reset)", 0, [], self.undo))
        self.output = output
        self.callbacks = callbacks
        self.history_keeper = HistoryKeeper()

    def run_history(self, show_out: bool = False):
        for command in self.history_keeper.history:
            try:
                if show_out:
                    self.output(f"{Fore.LIGHTBLACK_EX}>>{Fore.LIGHTWHITE_EX} {command}{Style.RESET_ALL}")
                self._execute(command)
            except Exception as e:  # noqa
                problem = f"Something went wrong while loading command [{command}]:\n\t"
                problem += helpers.error_string(e)
                self.output(helpers.error_format(problem))

    def undo(self):
        self.callbacks.reset()
        name = self.history_keeper.remove_last() or "NONE"
        self.run_history()
        self.output(f"Undid one command: {name}")

    def load(self, file: str):
        self.history_keeper.load(file)
        # Don't reset or clear until after load confirmed successful
        self.callbacks.clear()
        self.callbacks.reset()
        self.run_history(True)

    def save(self, file: str):
        self.history_keeper.remove_last()  # Don't save this command
        self.history_keeper.save(file)

    def help(self, command: str = None):
        if command is None:
            for name in self.commands:
                value = self.commands[name]
                # If a specific command is specified (even aliased), show full help
                # But, since we are listing all commands here, an aliased command should simply state its aliasing
                if type(value) == tuple:
                    if value[0] == "ALIAS":
                        help_msg = f"{Style.BRIGHT}{Fore.GREEN}"
                        help_msg += name
                        help_msg += f"{Fore.CYAN}{Style.NORMAL} -> {Fore.GREEN}{Style.BRIGHT}"
                        help_msg += value[1]
                        help_msg += Style.RESET_ALL
                        self.output(help_msg)
                    elif value[0] == "BREAK":
                        self.output("")
                    else:  # No idea what this is, maybe the specific help does?
                        self.help(name)
                else:
                    self.help(name)
        else:
            try:
                commands = self.commands[command]
                while type(commands) == tuple:
                    if commands[0] == "ALIAS":
                        commands = self.commands[commands[1]]
                    else:
                        return
                for com in commands:
                    if not com.show_help:
                        continue
                    arg_list = arg_names(com.callback)
                    if len(arg_list) > 0 and arg_list[0] == "self":
                        arg_list = arg_list[1:]
                    arg_list = arg_list[:com.num_args]
                    help_msg = Style.BRIGHT + Fore.GREEN + command + arg_col
                    for i in range(com.num_args):
                        help_msg += " " + arg_list[i]  # +":"+com.types[i].__name__
                    help_msg += Style.RESET_ALL
                    if com.help_msg != "":
                        help_msg += "\n\t" + Fore.CYAN + stylize(com.help_msg, arg_col + Style.BRIGHT,
                                                                 Fore.CYAN + Style.NORMAL)
                    help_msg += Style.RESET_ALL
                    self.output(help_msg)
            except KeyError:
                raise InvalidCommandError(f"Command not found: {command}")

    def register(self, command: Command, show_help: bool = True):
        """Register a command."""
        registry = self.commands.get(command.name, OrderedSet())
        registry.add(command)
        self.commands[command.name] = registry
        command.show_help = show_help

    def alias(self, original: str, aliased: str):
        """Create an alias for commands

        :param original: original name of commands
        :param aliased: aliased name of commands
        :return: None
        """
        self.commands[aliased] = ("ALIAS", original)

    def help_break(self):
        """Create a newline in the help message

        :return: None
        """
        self.commands[helpers.uuid()] = ("BREAK",)

    def execute(self, string: str) -> typing.Any:
        """Wrapper around self._execute to handle exceptions"""
        try:
            self.history_keeper.add(string)
            self._execute(string)
        except Exception as e:  # noqa
            self.history_keeper.remove_last()  # Something went wrong, don't put in history
            problem = "Something went wrong while executing that command:\n\t"
            problem += helpers.error_string(e)
            self.output(helpers.error_format(problem))

    def _execute(self, string: str) -> typing.Any:
        """Executes given command string.

        Uses name of command, number of arguments, and types of arguments to find correct command to execute.

        :param string: User input
        :return: Any
        """
        original_string = string
        parts = string.split(" ")
        name = parts[0]
        possibilities = self.commands.get(name, set())
        while type(possibilities) == tuple:  # `while` in case of chained aliasing
            if possibilities[0] == "ALIAS":
                name = possibilities[1]
                possibilities = self.commands.get(name, set())
                string = name
                if len(parts) > 1:
                    string += " " + " ".join(parts[1:])
            elif possibilities[0] == "BREAK":
                return
            else:
                raise InvalidCommandError(f"Broken registration for command {name}, user input {string}")
        if len(possibilities) == 0:
            raise InvalidCommandError(f"Command {name} not found")

        command = None
        for com in possibilities:
            if len(parts) - 1 == com.num_args:
                try:
                    args = []
                    for i in range(com.num_args):
                        args.append(com.types[i](parts[i + 1]))
                    command = com
                    break
                except TypeError:
                    pass
        if command is not None:
            return command.execute(string)
        else:
            raise InvalidCommandError(f"Command not found with parameters matching: {original_string}")
