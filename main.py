import click

from ayumi import start_ayumi, init_schemas


@click.command()
@click.option(
    '--reinit',
    '-r',
    is_flag=True,
    help='Use it to recreate database schemas.'
)
def main(reinit: bool) -> None:
    init_schemas(drop=reinit)
    # start ayumi after `init_schemas`
    start_ayumi()


if __name__ == '__main__':
    main()
