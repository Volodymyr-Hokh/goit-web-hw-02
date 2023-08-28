from abc import ABC, abstractmethod

from rich.console import Console
from rich.table import Table

from assistant_ostap.classes import AddressBook
from assistant_ostap.handlers import commands
from assistant_ostap.notes import NoteBook


class UserInterface(ABC):

    @abstractmethod
    def show_contacts(self, parsed_command):
        pass

    @abstractmethod
    def show_notes(self, parsed_command):
        pass
    
    @abstractmethod
    def show_commands(self):
        pass


class ConsoleInterface(UserInterface):
    def show_contacts(self, parsed_command):
        if parsed_command:
            if isinstance(parsed_command, AddressBook) or isinstance(parsed_command, NoteBook):
                for page in parsed_command:
                    commands["clear"]()
                    print("\n".join([str(i) for i in page]))
                    user_input = input(
                        "Press 'q' to quit. Press any key to see the next page: ")
                    if user_input.lower() == "q":
                        break
            else:
                print(parsed_command)

    def show_notes(self, parsed_command):
        pass

    def show_commands(self):
        table = Table(title="Commands",style="magenta",show_lines=True)
        table.add_column('Command')
        table.add_column('Description')
        for command, func in commands.items():
            table.add_row(command, func.__doc__)
        console = Console()
        console.print(table)