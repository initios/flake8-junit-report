import click
from . import _convert


@click.command()
@click.argument('source')
@click.argument('destination')
@click.option('--allways-create', '-c', is_flag=True,
              help='Create a junit report file even if there are no errors.')
@click.option('--all-files', '-a', help='Output all python files in output '
                                        'file of given directory.')
def conversion(source, destination, allways_create, all_files):
    """
    Converts a flake8 file to junit
    """
    _convert(source, destination, allways_create=allways_create,
             all_files_path=all_files)
    click.echo(click.style('Conversion done', fg='green'))
