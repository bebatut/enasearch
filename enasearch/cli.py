#!/usr/bin/env python

import click
import enasearch
from dicttoxml import dicttoxml

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

lengthLimit = 100000


def exception_handler(function):
    """Handle the exceptions raised by the commands"""
    def handle_exception(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            raise click.ClickException(e)
    return handle_exception


def print_list(l):
    """Print list"""
    for e in l:
        click.echo(e)


def print_simple_dict(d):
    """Print a dictionary with fields as key and description as value"""
    for res, des in d.items():
        click.echo("%s\t%s" % (res, des['description']))


def print_complex_field_dict(d):
    """Print a dictionary with fields as key and dictionary with description,
    results and type"""
    click.echo("field\tdescription\ttype\tresults")
    for f, des in d.items():
        click.echo("%s\t%s\t%s\t%s" % (f, des['description'], des['type'], ', '.join(des['results'])))


def print_display(results, display):
    """Print the results given the choosen display"""
    if display == 'xml':
        print(dicttoxml(results))
    elif display == 'fasta' or display == 'fastq':
        for record in results:
            print(record.format(display))
    else:
        print(results)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cli():
    pass


@click.command('get_results', short_help='Get list of results')
@exception_handler
def get_results():
    """Return the list of results in ENA"""
    enasearch.get_results(verbose=True)


@click.command('get_taxonomy_results', short_help='Get list of taxonomy results')
@exception_handler
def get_taxonomy_results():
    """Return the list of taxonomy results in ENA"""
    taxo_results = enasearch.get_taxonomy_results(verbose=False)
    print_simple_dict(taxo_results)


@click.command('get_filter_fields', short_help='Get filter fields')
@click.option(
    '--result',
    required=True,
    help='Id of a result (accessible with get_results)')
@exception_handler
def get_filter_fields(result):
    """Get the filter fields of a result to build a query"""
    fields = enasearch.get_filter_fields(result=result, verbose=False)
    print_complex_field_dict(fields)


@click.command('get_returnable_fields', short_help='Get returnable fields')
@click.option(
    '--result',
    required=True,
    help='Id of a result (accessible with get_results)')
@exception_handler
def get_returnable_fields(result):
    """Get the fields of a result that can returned in a report"""
    fields = enasearch.get_returnable_fields(result=result, verbose=False)
    print_list(fields)


@click.command('get_run_fields', short_help='Get run fields')
@exception_handler
def get_run_fields():
    """Get the fields for a run"""
    fields = enasearch.get_returnable_fields(result="read_run", verbose=False)
    print_list(fields)


@click.command('get_analysis_fields', short_help='Get analysis fields')
@exception_handler
def get_analysis_fields():
    """Get the fields for an analysis"""
    fields = enasearch.get_returnable_fields(result="analysis", verbose=True)
    print_list(fields)


@click.command('get_sortable_fields', short_help='Get sortable fields')
@click.option(
    '--result',
    required=True,
    help='Id of a result (accessible with get_results)')
@exception_handler
def get_sortable_fields(result):
    """Get the fields of a result that can sorted for a report"""
    fields = enasearch.get_sortable_fields(result=result, verbose=False)
    print_complex_field_dict(fields)


@click.command('get_filter_types', short_help='Get filter types')
@exception_handler
def get_filter_types():
    """Get the types of filters usable to build a query"""
    types = enasearch.get_filter_types(verbose=False)
    click.echo("type\toperators/parameters\tvalues/description")
    for f, d in types.items():
        if f != 'Geospatial' and f != 'Taxonomy' and f != 'Boolean':
            click.echo("%s\t%s\t%s" % (f, ', '.join(d['operators']), d['value'] if type(d['value']) == str else ', '.join(d['value'])))
        elif f == 'Boolean':
            click.echo("%s\t%s\t%s" % (f, ', '.join(d['operators']), ', '.join(d['values'])))
        else:
            for ff, dd in d.items():
                click.echo("%s\t%s\t%s" % (ff, ', '.join(dd['parameters']), dd['description']))


@click.command('get_display_options', short_help='Get display options')
@exception_handler
def get_display_options():
    """Get the display options to specify the display format"""
    options = enasearch.get_display_options(verbose=False)
    print_simple_dict(options)


@click.command('get_download_options', short_help='Get download options')
@exception_handler
def get_download_options():
    """Get the download options to specify that records are to be saved in a
    file
    """
    options = enasearch.get_download_options(verbose=False)
    print_simple_dict(options)


@click.command('search_data', short_help='Search data')
@click.option(
    '--free_text_search',
    is_flag=True,
    help='Use free text search, otherwise the data warehouse is used')
@click.option(
    '--query',
    required=True,
    help='Query string, made up of filtering conditions, joined by logical ANDs, ORs and NOTs and bound by double quotes; the filter fields for a query are accessible with get_filter_fields and the type of filters with get_filter_types')
@click.option(
    '--result',
    required=True,
    help='Id of a result (accessible with get_results)')
@click.option(
    '--display',
    required=True,
    help='Display option to specify the display format (accessible with get_display_options)')
@click.option(
    '--download',
    required=False,
    help='Download option to specify that records are to be saved in a file (used with file option, list accessible with get_download_options)')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='File to save the content of the search (used with download option)')
@click.option(
    '--fields',
    multiple=True,
    required=False,
    help='Fields to return (accessible with get_returnable_fields, used only for report as display value) [multiple or comma-separated]')
@click.option(
    '--sortfields',
    multiple=True,
    required=False,
    help='Fields to sort the results (accessible with get_sortable_fields, used only for report as display value) [multiple or comma-separated]')
@click.option(
    '--offset',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='First record to get (used only for display different of fasta and fastq')
@click.option(
    '--length',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='Number of records to retrieve (used only for display different of fasta and fastq')
@exception_handler
def search_data(
    free_text_search, query, result, display, download, file, fields,
    sortfields, offset, length
):
    """Search data given a query
    """
    free_text_search = True if free_text_search else False
    download = None if not download else download
    file = None if not file else file
    fields = None if not fields else ",".join(fields)
    sortfields = None if not sortfields else ",".join(sortfields)
    offset = None if not offset else offset
    length = None if not length else length
    if display in ["fasta", "fastq"]:
        results = enasearch.search_all_data(
            free_text_search=free_text_search,
            query=query,
            result=result,
            display=display,
            download=download,
            file=file,
            fields=fields,
            sortfields=sortfields)
    else:
        results = enasearch.search_data(
            free_text_search=free_text_search,
            query=query,
            result=result,
            display=display,
            download=download,
            file=file,
            fields=fields,
            sortfields=sortfields,
            offset=offset,
            length=length)

    if file is None:
        print_display(results, display)


@click.command('retrieve_data', short_help='Retrieve ENA data')
@click.option(
    '--ids',
    required=True,
    multiple=True,
    help='Ids for records to return (other than Taxon and Project) [multiple]')
@click.option(
    '--display',
    required=True,
    help='Display option to specify the display format (accessible with get_display_options)')
@click.option(
    '--download',
    required=False,
    help='Download option to specify that records are to be saved in a file (used with file option, list accessible with get_download_options)')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='File to save the content of the search (used with download option)')
@click.option(
    '--offset',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='First record to get (used only for display different of  fasta and fastq')
@click.option(
    '--length',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='Number of records to retrieve (used only for display  different of fasta and fastq')
@click.option(
    '--subseq_range',
    required=False,
    help='Range for subsequences (integer start and stop separated  by a -)')
@click.option(
    '--expanded',
    is_flag=True,
    help='Determine if a CON record is expanded')
@click.option(
    '--header',
    is_flag=True,
    help='To obtain only the header of a record')
@exception_handler
def retrieve_data(
    ids, display, download, file, offset, length, subseq_range, expanded,
    header
):
    """Retrieve ENA data (other than taxon and project)
    """
    download = None if not download else download
    file = None if not file else file
    offset = None if not offset else offset
    length = None if not length else length
    subseq_range = None if not subseq_range else subseq_range
    expanded = True if expanded else False
    header = True if header else False
    data = enasearch.retrieve_data(
        ids=",".join(ids),
        display=display,
        download=download,
        file=file,
        offset=offset,
        length=length,
        subseq_range=subseq_range,
        expanded=expanded,
        header=header)
    if file is None:
        print_display(data, display)


@click.command('retrieve_taxons', short_help='Retrieve ENA taxon data')
@click.option(
    '--ids',
    required=True,
    multiple=True,
    help='Ids for taxon to return [multiple]')
@click.option(
    '--display',
    required=True,
    help='Display option to specify the display format (accessible with get_display_options)')
@click.option(
    '--result',
    required=False,
    help='Id of a taxonomy result (accessible with get_taxonomy_results)')
@click.option(
    '--download',
    required=False,
    help='Download option to specify that records are to be saved in a file (used with file option, list accessible with get_download_options)')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='File to save the content of the search (used with download option)')
@click.option(
    '--offset',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='First record to get (used only for display different of fasta and fastq')
@click.option(
    '--length',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='Number of records to retrieve (used only for display different of fasta and fastq')
@click.option(
    '--subseq_range',
    required=False,
    help='Range for subsequences (integer start and stop separated by a -)')
@click.option(
    '--expanded',
    is_flag=True,
    help='Determine if a CON record is expanded')
@click.option(
    '--header',
    is_flag=True,
    help='To obtain only the header of a record')
@exception_handler
def retrieve_taxons(
    ids, display, result, download, file, offset, length, subseq_range,
    expanded, header
):
    """Retrieve ENA taxon data (other than taxon and project)
    """
    result = None if not result else result
    download = None if not download else download
    file = None if not file else file
    offset = None if not offset else offset
    length = None if not length else length
    subseq_range = None if not subseq_range else subseq_range
    expanded = True if expanded else False
    header = True if header else False
    data = enasearch.retrieve_taxons(
        ids=",".join(ids),
        display=display,
        result=result,
        download=download,
        file=file,
        offset=offset,
        length=length,
        subseq_range=subseq_range,
        expanded=expanded,
        header=header)
    if file is None:
        print_display(data, display)


@click.command('retrieve_run_report', short_help='Retrieve run report')
@click.option(
    '--accession',
    required=True,
    help='Accession id (study accessions (ERP, SRP, DRP, PRJ prefixes), experiment accessions (ERX, SRX, DRX prefixes), sample accessions (ERS, SRS, DRS, SAM prefixes) and run accessions))')
@click.option(
    '--fields',
    multiple=True,
    required=False,
    help='Fields to return (accessible with get_run_fields) [multiple or comma-separated]')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='File to save the report')
@exception_handler
def retrieve_run_report(accession, fields, file):
    """Retrieve run report
    """
    fields = None if not fields else ",".join(fields)
    file = None if not file else file
    report = enasearch.retrieve_run_report(
        accession=accession,
        fields=fields,
        file=file)
    if file is None:
        print_display(report, 'report')


@click.command(
    'retrieve_analysis_report',
    short_help='Retrieve analysis report')
@click.option(
    '--accession',
    required=True,
    help='Accession id (study accessions (ERP, SRP, DRP, PRJ prefixes), experiment accessions (ERX, SRX, DRX prefixes), sample accessions (ERS, SRS, DRS, SAM prefixes) and run accessions))')
@click.option(
    '--fields',
    multiple=True,
    required=False,
    help='Fields to return (accessible with get_analysis_fields) [multiple or comma-separated]')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='File to save the report')
@exception_handler
def retrieve_analysis_report(accession, fields, file):
    """Retrieve analysis report
    """
    fields = None if not fields else ",".join(fields)
    file = None if not file else file
    report = enasearch.retrieve_analysis_report(
        accession=accession,
        fields=fields,
        file=file)
    if file is None:
        print_display(report, 'report')


cli.add_command(get_results)
cli.add_command(get_taxonomy_results)
cli.add_command(get_filter_fields)
cli.add_command(get_returnable_fields)
cli.add_command(get_run_fields)
cli.add_command(get_analysis_fields)
cli.add_command(get_sortable_fields)
cli.add_command(get_filter_types)
cli.add_command(get_display_options)
cli.add_command(get_download_options)
cli.add_command(search_data)
cli.add_command(retrieve_data)
cli.add_command(retrieve_taxons)
cli.add_command(retrieve_run_report)
cli.add_command(retrieve_analysis_report)
