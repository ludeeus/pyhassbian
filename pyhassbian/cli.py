"""Enable CLI."""
import click


@click.command()
@click.option('--port', '-p', default=9999, help='Port number.')
@click.option('--username', '-U', default='pi', help='Username.')
@click.option('--password', '-P', default='raspberry', help='Password.')
@click.option('--nu_auth', is_flag=True, help='Disable auth.')
def cli(port, username, password, no_auth):
    """CLI for this package."""
    from pyhassbian.server import run_server
    run_server(port, username, password, no_auth)


cli()  # pylint: disable=E1120
