import logging
import re

from fuzzywuzzy import fuzz, process
import readline

from assistant_ostap.handlers import commands
from assistant_ostap.ui import ConsoleInterface


def completer(text, state):
    if not text.isalpha():
        return None
    options = [cmd for cmd in commands.keys() if cmd.startswith(text.lower())]
    if not options:
        return None
    if state < len(options):
        return options[state]
    return None


def parse_command(user_input: str):
    match = re.search(
        r"^show\s|^good\s|^del\s|^sort\s|^change\s|^add\s", user_input.lower())
    try:
        if match:
            user_command = " ".join(user_input.split()[:2]).lower()
            command_arguments = user_input.split()[2:]
        else:
            user_command = user_input.split()[0].lower()
            command_arguments = user_input.split()[1:]
    except IndexError:
        return "Please enter a command name."

    if user_command not in commands.keys():
        logging.basicConfig(level=logging.ERROR)
        best_match, match_ratio = process.extractOne(user_command,
                                                     commands.keys(),
                                                     scorer=fuzz.ratio)
        if match_ratio >= 60:
            return f"Command not found.\nPerhaps you meant '{best_match}'."
        else:
            return "Command not found.\nTo view all available commands, enter 'help'."
    else:
        return commands[user_command](*command_arguments)


def main():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    while True:
        ui = ConsoleInterface()
        user_input = input("Enter command: ")
        if "help" in user_input:
            ui.show_commands()
        else:
            result = parse_command(user_input)
            ui.show_contacts(result)


if __name__ == "__main__":
    main()
