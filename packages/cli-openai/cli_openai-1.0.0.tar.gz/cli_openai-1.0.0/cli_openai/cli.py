from volunor import Cli

from cli_openai.commands.greet import GreetCommand

descriptor = {
    "greet": GreetCommand
}

cli = Cli(descriptor, prog="openai")

def entry_point():
    cli.big_bang()

if __name__ == '__main__':
    entry_point()

