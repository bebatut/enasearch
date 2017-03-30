#!/usr/bin/env python

import click
import ebisearch


@click.group()
def main():
    pass


@click.command('get_results', short_help='Get list of results')
def get_results():
    """Return the list of domains in EBI"""
    ebisearch.get_results(verbose=True)


@click.command('get_filter_fields', short_help='Get filter fields')
@click.option(
    '--result',
    help='Id of a result (accessible with get_results)')
def get_filter_fields(result):
    """Get the filter fields of a result to build a query"""
    ebisearch.get_filter_fields(verbose=True)


@click.command('get_filter_types', short_help='Get filter types')
def get_filter_types():
    """Get the types of filters usable to build a query"""
    ebisearch.get_filter_types(verbose=True)


@click.command('get_display_options', short_help='Get display options')
def get_display_options():
    """Get the display options to specify the display format"""
    ebisearch.get_display_options(verbose=True)


@click.command('get_download_options', short_help='Get download options')
def get_download_options():
    """Get the download options to specify that records are to be saved in a
    file
    """
    ebisearch.get_download_options(verbose=True)


main.add_command(get_results)
main.add_command(get_filter_fields)
main.add_command(get_filter_types)
main.add_command(get_display_options)
main.add_command(get_download_options)


if __name__ == "__main__":
    main()
