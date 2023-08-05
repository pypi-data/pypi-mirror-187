import argparse

from .. import __version__
from .predict import PredictAutoXGBCommand
from .serve import ServeAutoXGBCommand
from .train import TrainAutoXGBCommand


def main():
    parser = argparse.ArgumentParser(
        "AutoXGB CLI",
        usage="xgbauto <command> [<args>]",
        epilog="For more information about a command, run: `autoxgb <command> --help`",
    )
    parser.add_argument("--version", "-v", help="Display AutoXGB version", action="store_true")

    commands_parser = parser.add_subparsers(help="commands")
    TrainAutoXGBCommand.register_subcommand(commands_parser)
    PredictAutoXGBCommand.register_subcommand(commands_parser)
    ServeAutoXGBCommand.register_subcommand(commands_parser)

    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit(0)

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    command = args.func(args)
    command.execute()


if __name__ == "__main__":
    main()
