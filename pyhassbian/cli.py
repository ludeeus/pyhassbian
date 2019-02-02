"""Enable CLI."""
import asyncio
import click


@click.command()
@click.option('--port', '-P', default=9999, help='port number.')
def cli(port):
    """CLI for this package."""
    loop = asyncio.get_event_loop()
    from pyhassbian.server import run_server
    loop.run_until_complete(run_server(port))


cli()  # pylint: disable=E1120
