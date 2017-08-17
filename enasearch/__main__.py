#!/usr/bin/env python

import click
import enasearch
from pprint import pprint

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

lengthLimit = 100000


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def main():
    pass


@click.command('get_results', short_help='Get list of results')
def get_results():
    """Return the list of results in ENA"""
    enasearch.get_results(verbose=True)


@click.command('get_taxonomy_results', short_help='Get list of taxonomy results')
def get_taxonomy_results():
    """Return the list of taxonomy results in ENA"""
    enasearch.get_taxonomy_results(verbose=True)


@click.command('get_filter_fields', short_help='Get filter fields')
@click.option(
    '--result',
    required=True,
    help='Id of a result (accessible with get_results)')
def get_filter_fields(result):
    """Get the filter fields of a result to build a query"""
    enasearch.get_filter_fields(
        result=result,
        verbose=True)


@click.command('get_returnable_fields', short_help='Get returnable fields')
@click.option(
    '--result',
    required=True,
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
    required=True,
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
    help='Fields to return (accessible with get_returnable_fields, used only for report as display value) [multiple]')
@click.option(
    '--sortfields',
    multiple=True,
    required=False,
    help='Fields to sort the results (accessible with get_sortable_fields, used only for report as display value) [multiple]')
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
        pprint(results)


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
        pprint(data)


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
        pprint(data)


@click.command('retrieve_run_report', short_help='Retrieve run report')
@click.option(
    '--accession',
    required=True,
    help='Accession id (study accessions (ERP, SRP, DRP, PRJ prefixes), experiment accessions (ERX, SRX, DRX prefixes), sample accessions (ERS, SRS, DRS, SAM prefixes) and run accessions))')
@click.option(
    '--fields',
    multiple=True,
    required=False,
    help='Fields to return (accessible with get_run_fields) [multiple]')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='File to save the report')
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
        pprint(report)


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
    help='Fields to return (accessible with get_analysis_fields)  [multiple]')
@click.option(
    '--file',
    required=False,
    type=click.Path(dir_okay=True, writable=True),
    help='File to save the report')
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
