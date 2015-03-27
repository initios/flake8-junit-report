import click
from . import _convert


@click.command()
@click.argument('source')
@click.argument('destination')
def conversion(source, destination):
    """
    Converts a flake8 file to junit
    """
    _convert(source, destination)
    click.echo(click.style('Conversion done', fg='green'))
