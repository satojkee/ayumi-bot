import click

from ayumi import *


@click.command()
@click.option(
    '--init',
    '-i',
    is_flag=True,
    help='Use it to re/create database schemas.'
)
def main(init: bool) -> None:
    if init:
        init_schemas()
    else:
        start_ayumi()


if __name__ == '__main__':
    main()
