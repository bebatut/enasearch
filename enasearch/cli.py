#!/usr/bin/env python

import click
import enasearch
from dicttoxml import dicttoxml
from functools import wraps

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

lengthLimit = 100000


def exception_handler(function):
    """Handle the exceptions raised by the commands"""
    @wraps(function)
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
@click.version_option(version="0.2.0")
def cli():
    """The Python library for interacting with ENA's API"""
    pass


@click.command('get_results')
@exception_handler
def get_results():
    """Get the possible results (type of data).

    This function return the possible results (or type of data) accessible with
    ENA with their ids and a short description
    """
    enasearch.get_results(verbose=True)


@click.command('get_taxonomy_results')
@exception_handler
def get_taxonomy_results():
    """Get list of taxonomy results.

    This function returns the  description about the possible results
    accessible via the taxon portal. Each taxonomy result is described with a
    short description"""
    taxo_results = enasearch.get_taxonomy_results(verbose=False)
    print_simple_dict(taxo_results)


@click.command('get_filter_fields')
@click.option(
    '--result',
    required=True,
    help='Id of a result (accessible with get_results)')
@exception_handler
def get_filter_fields(result):
    """Get the filter fields of a result to build a query.

    This function returns the fields that can be used to build a query on
    a result on ENA. Each field is described on a line with field id, its
    description, its type and to which results it is related
    """
    fields = enasearch.get_filter_fields(result=result, verbose=False)
    print_complex_field_dict(fields)


@click.command('get_returnable_fields')
@click.option(
    '--result',
    required=True,
    help='Id of a result (accessible with get_results)')
@exception_handler
def get_returnable_fields(result):
    """Get the fields extractable for a result.

    This function returns the fields as a list."""
    fields = enasearch.get_returnable_fields(result=result, verbose=False)
    print_list(fields)


@click.command('get_run_fields')
@exception_handler
def get_run_fields():
    """Get the fields extractable for a run.

    This function returns the fields as a list."""
    fields = enasearch.get_returnable_fields(result="read_run", verbose=False)
    print_list(fields)


@click.command('get_analysis_fields')
@exception_handler
def get_analysis_fields():
    """Get the fields extractable for an analysis.

    This function returns the fields as a list."""
    fields = enasearch.get_returnable_fields(result="analysis", verbose=True)
    print_list(fields)


@click.command('get_sortable_fields')
@click.option(
    '--result',
    required=True,
    help='Id of a result (accessible with get_results)')
@exception_handler
def get_sortable_fields(result):
    """Get the fields of a result that can sorted.

    This function returns the fields that can be used to sort the output of a
    query for a result on ENA. Each field is described on a line with field id,
    its description, its type and to which results it is related
    """
    fields = enasearch.get_sortable_fields(result=result, verbose=False)
    print_complex_field_dict(fields)


@click.command('get_filter_types')
@exception_handler
def get_filter_types():
    """Return the filters usable for the different type of data.

    This function returns the filters that can be used for the different type of
    data (information available with the information on the filter fileds). Each
    filter is described with its name, the possible operators or paramters, a
    description of the expected values
    """
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


@click.command('get_display_options')
@exception_handler
def get_display_options():
    """Get the list of possible formats to display the result.

    This function returns the possible formats to display the result of a query on ENA. Each format is described.
    """
    options = enasearch.get_display_options(verbose=False)
    print_simple_dict(options)


@click.command('get_download_options')
@exception_handler
def get_download_options():
    """Get the options for download of data from ENA.

    Each option is described.
    """
    options = enasearch.get_download_options(verbose=False)
    print_simple_dict(options)


@click.command('search_data')
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
    """Search data given a query.

    This function

    - Extracts the number of possible results for the query
    - Extracts the all the results of the query (by potentially running several times the search function)

    The output can be redirected to a file and directly display to the standard
    output given the display chosen.
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
            file=file)
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


@click.command('retrieve_data')
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
    """Retrieve ENA data (other than taxon).

    This function retrieves data (other than taxon) from ENA by:

    - Building the URL based on the ids to retrieve and some parameters to format the results
    - Requesting the URL to extract the data

    The output can be redirected to a file and directly display to the standard
    output given the display chosen.
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


@click.command('retrieve_taxons')
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
    """Retrieve data from the ENA Taxon Portal.

    This function retrieves data (other than taxon) from ENA by:

    - Formatting the ids to query then on the Taxon Portal
    - Building the URL based on the ids to retrieve and some parameters to format the results
    - Requesting the URL to extract the data

    The output can be redirected to a file and directly display to the standard
    output given the display chosen.
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


@click.command('retrieve_run_report')
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
    """Retrieve run report from ENA.

    The output can be redirected to a file and directly display to the standard
    output given the display chosen.
    """
    fields = None if not fields else ",".join(fields)
    file = None if not file else file
    report = enasearch.retrieve_run_report(
        accession=accession,
        fields=fields,
        file=file)
    if file is None:
        print_display(report, 'report')


@click.command('retrieve_analysis_report')
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
    """Retrieve analysis report from ENA.

    The output can be redirected to a file and directly display to the standard
    output given the display chosen.
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
