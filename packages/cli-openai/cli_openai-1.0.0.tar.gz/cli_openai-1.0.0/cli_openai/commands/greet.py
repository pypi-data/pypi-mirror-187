import argparse
import sys

import volunor

from cli_openai.core.greet import greet


class GreetCommand(volunor.Command):
    """
    Simple greet command
    """
    def volunor_args(self, required_args: argparse.ArgumentParser, optional_args: argparse.ArgumentParser):
        required_args.add_argument("name", help="Name to greet")
        optional_args.add_argument("-c", '--count', type=int, help="Number of greet", default=1)

    def __call__(self, *args, **kwargs):
        greet(name=kwargs.get('name'), count=kwargs.get('count'))
        sys.exit(0)
