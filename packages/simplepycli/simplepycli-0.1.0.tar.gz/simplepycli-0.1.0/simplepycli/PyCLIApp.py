# Declares our main CLI app class, which has functions
# that can be used as decorators for custom client code.
import sys
import subprocess

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import (
    FuzzyWordCompleter,
)


class PyCLIApp:
    def __init__(self, promptTitle="> "):
        # This dict stores tuples of (commandFunction, helpText),
        # with the key being the command name.
        self.commands = {}

        # Manually register some commands
        self.commands["exit"] = (
            self.exit,
            "Exit the current CLI session and close the program.",
        )
        self.commands["help"] = (
            self.help,
            "List available commands and their help messages.",
        )
        self.commands["clear"] = (
            self.clear,
            "Clear the current command line.",
        )

        self.promptTitle = promptTitle

    def command(self, commandName, helpText):
        """
        Function decorator for registering a command with the CLI.
        :param commandName: The name of the command to register.
        :param helpText: The help text to display for the command.

        :return None
        """
        # This is what command(...) evaluates to, and takes the
        # function we're wrapping around as a paramater.
        # This needs to return a function, which can then be
        # called by client code
        def firstInner(f):
            # Before doing anything else, register the given function
            # with self
            self.commands[commandName] = (f, helpText)

            # This is the function that will be called by client
            # code, and is responsible for calling the wrapped function
            def toCall(*args, **kwargs):
                f(*args, **kwargs)

            return toCall

        return firstInner

    # A default command to exit from the CLI
    def exit(self, params):
        sys.exit(0)

    # A default command to ask for command help
    def help(self, params):
        for command in self.commands:
            print(f"{command} : {self.commands[command][1]}")
    
    # A defult command to clear the current command line
    def clear(self, params):
        subprocess.run("clear", shell=True)

    def run(self):
        """
        Starts the CLI session with all custom commands available.
        """

        # Get a word completer for all supported commands
        commandWordCompleter = FuzzyWordCompleter(list(self.commands.keys()))

        # Construct our prompt session
        cliPromptSession = PromptSession(
            message=self.promptTitle, completer=commandWordCompleter
        )

        # Contructor for an error message we'll print if anything goes wrong
        errorMsg = (
            lambda cmdName: f"'{cmdName}' is not a valid command.\n"
            + "Please try agian, or type 'help' for assistance. "
        )

        while True:
            # When we run our prompt, the first word is our command
            # name, and the rest are the params we are going to
            # give to the command function
            userInput = cliPromptSession.prompt()

            # If input is empty, ignore
            if userInput.strip() == "":
                print(errorMsg(""))
                continue

            commandName = userInput.split()[0]
            params = userInput.replace(f"{commandName} ", "")

            # If that isn't a valid command name, print an error
            # message and ask for a retry
            if commandName not in self.commands:
                print(errorMsg(commandName))
            else:
                self.commands[commandName][0](params)
