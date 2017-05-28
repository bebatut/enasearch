#!/usr/bin/env python

import click
import enasearch
from pprint import pprint


lengthLimit = 100000


@click.group()
def main():
    pass


@click.command('get_results', short_help='Get list of results')
def get_results():
    """Return the list of results in ENA"""
    enasearch.get_results(verbose=True)


@click.command(
    'get_taxonomy_results',
    short_help='Get list of taxonomy results')
def get_taxonomy_results():
    """Return the list of taxonomy results in ENA"""
    enasearch.get_taxonomy_results(verbose=True)


@click.command('get_filter_fields', short_help='Get filter fields')
@click.option(
    '--result',
    help='Id of a result (accessible with get_results)')
def get_filter_fields(result):
    """Get the filter fields of a result to build a query"""
    enasearch.get_filter_fields(
        result=result,
        verbose=True)


@click.command('get_returnable_fields', short_help='Get returnable fields')
@click.option(
    '--result',
    help='Id of a result (accessible with get_results)')
def get_returnable_fields(result):
    """Get the fields of a result that can returned in a report"""
    enasearch.get_returnable_fields(
        result=result,
        verbose=True)


@click.command('get_run_fields', short_help='Get run fields')
def get_run_fields():
    """Get the fields for a run"""
    enasearch.get_returnable_fields(
        result="read_run",
        verbose=True)


@click.command('get_analysis_fields', short_help='Get analysis fields')
def get_analysis_fields():
    """Get the fields for an analysis"""
    enasearch.get_returnable_fields(
        result="analysis",
        verbose=True)


@click.command('get_sortable_fields', short_help='Get sortable fields')
@click.option(
    '--result',
    help='Id of a result (accessible with get_results)')
def get_sortable_fields(result):
    """Get the fields of a result that can sorted for a report"""
    enasearch.get_sortable_fields(
        result=result,
        verbose=True)


@click.command('get_filter_types', short_help='Get filter types')
def get_filter_types():
    """Get the types of filters usable to build a query"""
    enasearch.get_filter_types(verbose=True)


@click.command('get_display_options', short_help='Get display options')
def get_display_options():
    """Get the display options to specify the display format"""
    enasearch.get_display_options(verbose=True)


@click.command('get_download_options', short_help='Get download options')
def get_download_options():
    """Get the download options to specify that records are to be saved in a
    file
    """
    enasearch.get_download_options(verbose=True)


@click.command('search_data', short_help='Search data')
@click.option(
    '--free_text_search',
    type=click.Choice(['True', 'False']),
    help='Use free text search, otherwise the data warehouse is used')
@click.option(
    '--query',
    help='Query string, made up of filtering conditions, joined by logical ANDs\
    , ORs and NOTs and bound by double quotes; the filter fields for a query \
    are accessible with get_filter_fields and the type of filters with get_\
    filter_types')
@click.option(
    '--result',
    help='Id of a result (accessible with get_results)')
@click.option(
    '--display',
    help='Display option to specify the display format (accessible with get_\
    display_options)')
@click.option(
    '--download',
    required=False,
    help='(Optional) Download option to specify that records are to be saved \
    in a file (used with file option, list accessible with get_download_\
    options)')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='(Optional) File to save the content of the search (used with download\
    option)')
@click.option(
    '--fields',
    multiple=True,
    required=False,
    help='(Optional, Multiple) Fields to return (accessible with get_returnable\
    _fields, used only for report as display value)')
@click.option(
    '--sortfields',
    multiple=True,
    required=False,
    help='(Optional, Multiple) Fields to sort the results (accessible with get_\
    sortable_fields, used only for report as display value)')
@click.option(
    '--offset',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='(Optional) First record to get (used only for display different of \
    fasta and fastq')
@click.option(
    '--length',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='(Optional) Number of records to retrieve (used only for display \
    different of fasta and fastq')
def search_data(
    free_text_search, query, result, display, download, file, fields,
    sortfields, offset, length
):
    """Search data given a query
    """
    if not download:
        download = None
    if not file:
        file = None
    if not fields:
        fields = None
    else:
        fields = ",".join(fields)
    if not sortfields:
        sortfields = None
    else:
        sortfields = ",".join(sortfields)
    if not offset:
        offset = None
    if not length:
        length = None
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
        pprint(results)


@click.command('retrieve_data', short_help='Retrieve ENA data')
@click.option(
    '--ids',
    multiple=True,
    help='(Multiple) Ids for records to return (other than Taxon and Project)')
@click.option(
    '--display',
    help='Display option to specify the display format (accessible with get_\
    display_options)')
@click.option(
    '--download',
    required=False,
    help='(Optional) Download option to specify that records are to be saved \
    in a file (used with file option, list accessible with get_download_\
    options)')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='(Optional) File to save the content of the search (used with download\
    option)')
@click.option(
    '--offset',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='(Optional) First record to get (used only for display different of \
    fasta and fastq')
@click.option(
    '--length',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='(Optional) Number of records to retrieve (used only for display \
    different of fasta and fastq')
@click.option(
    '--range',
    required=False,
    help='(Optional) Range for subsequences (integer start and stop separated \
    by a -)')
@click.option(
    '--expanded',
    type=click.Choice(['True', 'False']),
    required=False,
    help='(Optional) Boolean to determine if a CON record is expanded')
@click.option(
    '--header',
    type=click.Choice(['True', 'False']),
    required=False,
    help='(Optional) Boolean to obtain only the header of a record')
def retrieve_data(
    ids, display, download, file, offset, length, subseq_range, expanded,
    header
):
    """Retrieve ENA data (other than taxon and project)
    """
    if not download:
        download = None
    if not file:
        file = None
    if not offset:
        offset = None
    if not length:
        length = None
    if not subseq_range:
        subseq_range = None
    if not expanded:
        expanded = None
    if not header:
        header = None
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
        pprint(data)


@click.command('retrieve_taxons', short_help='Retrieve ENA taxon data')
@click.option(
    '--ids',
    multiple=True,
    help='(Multiple) Ids for records to return (other than Taxon and Project)')
@click.option(
    '--display',
    help='Display option to specify the display format (accessible with get_\
    display_options)')
@click.option(
    '--result',
    required=False,
    help='(Optional) Id of a taxonomy result (accessible with get_taxonomy_\
    results)')
@click.option(
    '--download',
    required=False,
    help='(Optional) Download option to specify that records are to be saved \
    in a file (used with file option, list accessible with get_download_\
    options)')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='(Optional) File to save the content of the search (used with download\
    option)')
@click.option(
    '--offset',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='(Optional) First record to get (used only for display different of \
    fasta and fastq')
@click.option(
    '--length',
    type=click.IntRange(min=0, max=lengthLimit),
    required=False,
    help='(Optional) Number of records to retrieve (used only for display \
    different of fasta and fastq')
@click.option(
    '--range',
    required=False,
    help='(Optional) Range for subsequences (integer start and stop separated \
    by a -)')
@click.option(
    '--expanded',
    type=click.Choice(['True', 'False']),
    required=False,
    help='(Optional) Boolean to determine if a CON record is expanded')
@click.option(
    '--header',
    type=click.Choice(['True', 'False']),
    required=False,
    help='(Optional) Boolean to obtain only the header of a record')
def retrieve_taxons(
    ids, display, result, download, file, offset, length, subseq_range,
    expanded, header
):
    """Retrieve ENA taxon data (other than taxon and project)
    """
    if not result:
        result = None
    if not download:
        download = None
    if not file:
        file = None
    if not offset:
        offset = None
    if not length:
        length = None
    if not subseq_range:
        subseq_range = None
    if not expanded:
        expanded = None
    if not header:
        header = None

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
        pprint(data)


@click.command('retrieve_run_report', short_help='Retrieve run report')
@click.option(
    '--accession',
    help='Accession id (study accessions (ERP, SRP, DRP, PRJ prefixes), \
    experiment accessions (ERX, SRX, DRX prefixes), sample accessions (ERS, \
    SRS, DRS, SAM prefixes) and run accessions))')
@click.option(
    '--fields',
    multiple=True,
    required=False,
    help='(Optional, Multiple) Fields to return (accessible with get_run_\
    _fields)')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='(Optional) File to save the report')
def retrieve_run_report(accession, fields, file):
    """Retrieve run report
    """
    if not fields:
        fields = None
    else:
        fields = ",".join(fields)
    if not file:
        file = None
    report = enasearch.retrieve_run_report(
        accession=accession,
        fields=fields,
        file=file)
    if file is None:
        pprint(report)


@click.command(
    'retrieve_analysis_report',
    short_help='Retrieve analysis report')
@click.option(
    '--accession',
    help='Accession id (study accessions (ERP, SRP, DRP, PRJ prefixes), \
    experiment accessions (ERX, SRX, DRX prefixes), sample accessions (ERS, \
    SRS, DRS, SAM prefixes) and run accessions))')
@click.option(
    '--fields',
    multiple=True,
    required=False,
    help='(Optional, Multiple) Fields to return (accessible with get_analysis_\
    _fields)')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='(Optional) File to save the report')
def retrieve_analysis_report(accession, fields, file):
    """Retrieve analysis report
    """
    if not fields:
        fields = None
    else:
        fields = ",".join(fields)
    if not file:
        file = None
    report = enasearch.retrieve_analysis_report(
        accession=accession,
        fields=fields,
        file=file)
    if file is None:
        pprint(report)


main.add_command(get_results)
main.add_command(get_taxonomy_results)
main.add_command(get_filter_fields)
main.add_command(get_returnable_fields)
main.add_command(get_run_fields)
main.add_command(get_analysis_fields)
main.add_command(get_sortable_fields)
main.add_command(get_filter_types)
main.add_command(get_display_options)
main.add_command(get_download_options)
main.add_command(search_data)
main.add_command(retrieve_data)
main.add_command(retrieve_taxons)
main.add_command(retrieve_run_report)
main.add_command(retrieve_analysis_report)


if __name__ == "__main__":
    main()
