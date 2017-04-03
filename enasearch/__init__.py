#!/usr/bin/env python

import requests
import pickle
from pprint import pprint
import gzip
import xmltodict
from Bio import SeqIO
import tempfile
import pkg_resources


baseUrl = 'http://www.ebi.ac.uk/ena/'
lengthLimit = 100000


def get_data(filename):
    return pkg_resources.resource_filename('enasearch_data', filename)


def load_object(filepath):
    """Load object from a pickle file

    filepath: path to pickle file with serialized data
    """
    with open(filepath, 'rb') as input:
        obj = pickle.load(input)
    return obj


results = load_object(get_data("result_description.p"))
filter_types = load_object(get_data("filter_types.p"))
download_options = load_object(get_data("download_options.p"))
display_options = load_object(get_data("display_options.p"))
taxonomy_results = load_object(get_data("taxonomy_results.p"))


def get_results(verbose=True):
    """Return the list of results in ENA as a dictionary with the key being the
    result id and the value the result description

    verbose: boolean to define the printing info
    """
    if verbose:
        for result in results:
            print("%s: %s" % (result, results[result]["description"]))
    return results


def get_taxonomy_results(verbose=False):
    """Return info about the taxonomy results

    verbose: boolean to define the printing info
    """
    if verbose:
        pprint(taxonomy_results)
    return taxonomy_results


def check_result(result):
    """Check if result is in the list of possible results in ENA

    result: id of result to check
    """
    possible_results = get_results(verbose=False)
    if result not in possible_results:
        err_str = "The result od (%s) does not correspond to a " % (result)
        err_str += "possible result id in ENA"
        raise ValueError(err_str)


def check_taxonomy_result(result):
    """Check if a result is in the list of possible taxonomz results in ENA

    result: id of result to check
    """
    taxonomy_results = get_taxonomy_results(verbose=False)
    if result not in taxonomy_results:
        err_str = "The result id (%s) does not correspond to a " % (result)
        err_str += "possible taxonomy result id in ENA"
        raise ValueError(err_str)


def get_result(result, verbose=False):
    """Return info about a result

    result: id of the result (partition of ENA db), accessible with get_results
    verbose: boolean to define the printing info
    """
    results = get_results(verbose=False)
    check_result(result)
    result_info = results[result]
    if verbose:
        pprint(result_info)
    return result_info


def get_filter_fields(result, verbose=False):
    """Get the filter fields of a result to build a query

    result: id of the result (partition of ENA db), accessible with get_results
    verbose: boolean to define the printing info
    """
    result_info = get_result(result)
    filter_fields = result_info["filter_fields"]
    if verbose:
        pprint(filter_fields)
    return filter_fields


def get_returnable_fields(result, verbose=False):
    """Get the returnable fields of a result

    result: id of the result (partition of ENA db), accessible with get_results
    verbose: boolean to define the printing info
    """
    check_result(result)
    result_info = get_result(result)
    returnable_fields = result_info["returnable_fields"]
    if verbose:
        pprint(returnable_fields)
    return returnable_fields


def check_returnable_fields(fields, result):
    """Check that some fields are returnable fields of a resut

    fields: list of fields to check
    result: id of the result (partition of ENA db), accessible with get_results
    """
    returnable_fields = get_returnable_fields(result, verbose=False)
    for field in fields:
        if field not in returnable_fields:
            err_str = "The field %s is not a returnable field for " % (field)
            err_str += "result %s" % (result)
            raise ValueError(err_str)


def get_sortable_fields(result, verbose=False):
    """Get the sortable fields of a result

    result: id of the result (partition of ENA db), accessible with get_results
    verbose: boolean to define the printing info
    """
    check_result(result)
    sortable_fields = get_filter_fields(result, verbose=False)
    if verbose:
        pprint(sortable_fields)
    return sortable_fields


def check_sortable_fields(fields, result):
    """Check that some fields are sortable fields of a resut

    fields: list of fields to check
    result: id of the result (partition of ENA db), accessible with get_results
    """
    sortable_fields = get_sortable_fields(result, verbose=False)
    for field in fields:
        if field not in sortable_fields:
            err_str = "The field %s is not a sortable field for " % (field)
            err_str += "result %s" % (result)
            raise ValueError(err_str)


def get_filter_types(verbose=False):
    """Get the types of filters usable to build a query

    result: id of the result (partition of ENA db), accessible with get_results
    verbose: boolean to define the printing info
    """
    if verbose:
        pprint(filter_types)
    return filter_types


def get_display_options(verbose=False):
    """Get the display options

    verbose: boolean to define the printing info
    """
    if verbose:
        pprint(display_options)
    return display_options


def check_display_option(display):
    """Check if display is in the list of display in ENA

    display: display to check
    """
    display_options = get_display_options(verbose=False)
    if display not in display_options:
        err_str = "The display value (%s) does not correspond to a possible \
        display value in ENA" % (display)
        raise ValueError(err_str)


def get_download_options(verbose=False):
    """Get the download options

    verbose: boolean to define the printing info
    """
    if verbose:
        pprint(download_options)
    return download_options


def check_download_option(download):
    """Check if download is in the list of download format in ENA

    download: download format to check
    """
    download_options = get_display_options(verbose=False)
    if download not in download_options:
        err_str = "The download value does not correspond to a possible "
        err_str += "display value in ENA"
        raise ValueError(err_str)


def check_length(length):
    """Check if length is below the maximum length

    length: length value to test
    """
    if length > lengthLimit:
        err_str = "The length value (%s) is higher than the " % (length)
        err_str += "limit length (%s)" % (lengthLimit)
        raise ValueError(err_str)


def get_graphical_image(ids, featureRange, sequenceRange):
    """Get graphical image

    ids:
    featureRange:
    sequenceRange:
    """
    url = baseUrl + "data/view/graphics/"
    print(url)


def check_download_file_options(download, file):
    """Check that download and file options are correctly defined

    download: download option to specify that records are to be saved in a file
    (used with file option, accessible with get_download_options)
    file: filepath to save the content of the data (used with download option)
    """
    if file is None:
        err_str = "download option should come along with a filepath"
        raise ValueError(err_str)
    if download is None:
        err_str = "file option should come along with a download option"
        raise ValueError(err_str)
    check_download_option(download)


def check_subseq_range(subseq_range):
    """Check that subseq_range is well defined

    download: range for subsequences (limit separated by a -)
    """
    subseq_range_content = subseq_range.split("-")
    if len(subseq_range_content) != 2:
        err_str = "A subseq_range must have two arguments (start and stop)"
        err_str += " separated by a -"
        raise ValueError(err_str)
    if int(subseq_range_content[0]) > int(subseq_range_content[1]):
        err_str = "Start for a subseq_range must be lower than the stop"
        raise ValueError(err_str)


def check_boolean(boolean):
    """Check a boolean value

    boolean: boolean to determine an option
    """
    if boolean not in ["true", "false"]:
        err_str = "A boolean value must be only 'true' or 'false'"
        raise ValueError(err_str)


def format_seq_content(seq_str, format):
    """Format a string with sequences into a BioPython sequence objects
    (SeqRecord)

    seq_str: string with sequences to format
    format: fasta or fastq
    """
    sequences = []
    with tempfile.TemporaryFile(mode='w+') as fp:
        fp.write(seq_str)
        fp.seek(0)
        for record in SeqIO.parse(fp, format):
            sequences.append(record)
    return sequences


def request_url(url, display, file=None):
    """Run the URL request and return content or status

    url: URL to request
    display: display option
    length: number of records to retrieve
    file: filepath to save the content of the search
    """
    if file is not None:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(file, "ab") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        return r.raise_for_status()
    else:
        r = requests.get(url)
        r.raise_for_status()
        if display == "xml":
            return xmltodict.parse(r.text)
        elif display == "fasta" or display == "fastq":
            return format_seq_content(r.text, display)
        else:
            return r.text


def build_retrieve_url(
    ids, display, result=None, download=None, file=None, offset=0,
    length=100000, subseq_range=None, expanded=None, header=None
):
    """Build the URL to retriva data or taxon

    ids: comma-separated identifiers for records other than Taxon
    display: display option to specify the display format (accessible with
    get_display_options)
    offset: first record to get
    length: number of records to retrieve
    download: download option to specify that records are to be saved in a file
    (used with file option, accessible with get_download_options)
    file: filepath to save the content of the search (used with download
    option)
    subseq_range: range for subsequences (limit separated by a -)
    expanded: boolean to determine if a CON record is expanded
    header: boolean to obtain only the header of a record
    """
    url = baseUrl + "data/view/"
    url += ids

    check_display_option(display)
    url += "&display=%s" % (display)

    if result is not None:
        url += "&result=%s" % (result)

    check_length(length)
    url += "&length=%s" % (length)
    url += "&offset=%s" % (offset)

    if subseq_range is not None:
        check_subseq_range(subseq_range)
        url += "&range=%s" % (subseq_range)

    if expanded is not None:
        check_boolean(expanded)
        url += "&expanded=%s" % (expanded)

    if header is not None:
        check_boolean(header)
        url += "&header=%s" % (header)

    if download is not None or file is not None:
        check_download_file_options(download, file)
        url += "&download=%s" % (download)
    return url


def retrieve_data(
    ids, display, download=None, file=None, offset=0, length=100000,
    subseq_range=None, expanded=None, header=None
):
    """Retrieve ENA data (other than taxon)

    ids: comma-separated identifiers for records other than Taxon
    display: display option to specify the display format (accessible with
    get_display_options)
    offset: first record to get
    length: number of records to retrieve
    download: download option to specify that records are to be saved in a file
    (used with file option, accessible with get_download_options)
    file: filepath to save the content of the search (used with download
    option)
    subseq_range: range for subsequences (limit separated by a -)
    expanded: boolean to determine if a CON record is expanded
    header: boolean to obtain only the header of a record
    """
    url = build_retrieve_url(
        ids=ids,
        display=display,
        result=None,
        download=download,
        file=file,
        offset=offset,
        length=length,
        subseq_range=subseq_range,
        expanded=expanded,
        header=header)
    return request_url(url, display, file)


def retrieve_taxons(
    ids, display, result=None, download=None, file=None, offset=0,
    length=100000, subseq_range=None, expanded=None, header=None
):
    """Retrieve taxons

    ids: comma-separated taxon identifiers
    display: display option to specify the display format (accessible with
    get_display_options)
    result: taxonomy result to display (accessible with result)
    offset: first record to get
    length: number of records to retrieve
    download: download option to specify that records are to be saved in a file
    (used with file option, accessible with get_download_options)
    file: filepath to save the content of the search (used with download
    option)
    subseq_range: range for subsequences (limit separated by a -)
    expanded: boolean to determine if a CON record is expanded
    header: boolean to obtain only the header of a record
    """
    id_list = ids.split(",")
    modified_ids = []
    for one_id in id_list:
        modified_ids.append("Taxon:%s" % (one_id))
    if result is not None:
        check_taxonomy_result(result)
    url = build_retrieve_url(
        ids=",".join(modified_ids),
        display=display,
        result=result,
        download=download,
        file=file,
        offset=offset,
        length=length,
        subseq_range=subseq_range,
        expanded=expanded,
        header=header)
    return request_url(url, display, file)


def get_search_result_number(query, result, need_check_result=True):
    """Get the number of results for a query on a result

    query: query string, made up of filtering conditions, joined by logical
    ANDs, ORs and NOTs and bound by double quotes - the filter fields for a
    query are accessible with get_filter_fields and the type of filters with
    get_filter_types
    result: id of the result (partition of ENA db), accessible with get_results
    """
    url = baseUrl + "data/warehouse/search?"
    url += "query=%s" % (query)

    if need_check_result:
        check_result(result)
    url += "&result=%s" % (result)

    url += "&resultcount"
    r = requests.get(
        url,
        headers={"accept": "application/json"})
    r.raise_for_status()
    nb = r.text.split("\n")[0].split(": ")[1].replace(",", "")
    return int(nb)


def search_data(
    query, result, display, offset=0, length=lengthLimit, download=None,
    file=None, fields=None, sortfields=None
):
    """Search ENA data

    query: query string, made up of filtering conditions, joined by logical
    ANDs, ORs and NOTs and bound by double quotes - the filter fields for a
    query are accessible with get_filter_fields and the type of filters with
    get_filter_types
    result: id of the result (partition of ENA db), accessible with get_results
    display: display option to specify the display format (accessible with
    get_display_options)
    offset: first record to get
    length: number of records to retrieve
    download: download option to specify that records are to be saved in a file
    (used with file option, accessible with get_download_options)
    file: filepath to save the content of the search (used with download
    option)
    fields: comma-separated list of fields to return (only if display=report,
    list of returnable fields accessible with get_returnable_fields)
    sortfields: comma-separated list of fields to sort the results (only if
    display=report, list of sortable fields accessible with
    get_sortable_fields)
    """
    url = baseUrl + "data/warehouse/search?"
    url += "query=%s" % (query)

    check_result(result)
    url += "&result=%s" % (result)

    check_display_option(display)
    url += "&display=%s" % (display)

    check_length(length)
    url += "&length=%s" % (length)
    result_nb = get_search_result_number(query, result)
    if offset > result_nb:
        err_str = "The offset value must be lower than the possible number of "
        err_str += "results for the query"
        raise ValueError(err_str)
    url += "&offset=%s" % (offset)

    if display == "report":
        if fields is None:
            err_str = "A list of comma-separated fields to return must be "
            err_str += "provided if display=report"
            raise ValueError(err_str)
        check_returnable_fields(fields.split(","), result)
        url += "&fields=%s" % (fields)
        if sortfields is not None:
            check_sortable_fields(fields)
            url += "&sortfields=%s" % (sortfields)

    if download is not None or file is not None:
        check_download_file_options(download, file)
        url += "&download=%s" % (download)
    return request_url(url, display, file)


def search_all_data(
    query, result, display, download=None, file=None, fields=None,
    sortfields=None
):
    """Search ENA data and get all results (not size limited)

    query: query string, made up of filtering conditions, joined by logical
    ANDs, ORs and NOTs and bound by double quotes - the filter fields for a
    query are accessible with get_filter_fields and the type of filters with
    get_filter_types
    result: id of the result (partition of ENA db), accessible with get_results
    display: display option to specify the display format (accessible with
    get_display_options)
    download: download option to specify that records are to be saved in a file
    (used with file option, accessible with get_download_options)
    file: filepath to save the content of the search (used with download
    option)
    fields: comma-separated list of fields to return (only if display=report,
    list of returnable fields accessible with get_returnable_fields)
    sortfields: comma-separated list of fields to sort the results (only if
    display=report, list of sortable fields accessible with
    get_sortable_fields)
    """
    if display not in ["fasta", "fastq"]:
        err_str = "This function is not possible for this display option"
        raise ValueError(err_str)

    if download is not None or file is not None:
        check_download_file_options(download, file)

    result_nb = get_search_result_number(query, result)
    quotient = int(result_nb / float(lengthLimit))
    start = 0
    all_results = []
    for i in range(quotient):
        start = lengthLimit * i
        all_results += search_data(
            query=query,
            result=result,
            display=display,
            offset=start,
            length=lengthLimit,
            fields=None,
            sortfields=None)
    if (result_nb % 100) > 0:
        start = lengthLimit * quotient
        remainder = result_nb - start
        all_results += search_data(
            query=query,
            result=result,
            display=display,
            offset=start,
            length=remainder,
            fields=None,
            sortfields=None)
    if file:
        if download == "gzip":
            with gzip.open(file, 'wb') as fd:
                fd.write(all_results)
        else:
            with open(file, "w") as fd:
                fd.write(all_results)
    else:
        return all_results


def retrieve_filereport(accession, result, fields=None, file=None):
    """Retrieve a filereport

    accession: accession id
    result: read_run for a run report or analysis for an analysis report
    fields: comma-separated list of fields to have in the report
    file: filepath to save the content of the report
    """
    url = baseUrl + "data/warehouse/filereport?"
    url += "accession=%s" % (accession)

    if result not in ["read_run", "analysis"]:
        err_str = "The result to retrieve a filereport must be either read_run"
        err_str += " or analysis"
        raise ValueError(err_str)
    url += "&result=%s" % (result)

    if fields is not None:
        check_returnable_fields(fields.split(","), result)
        url += "&fields=%s" % (fields)

    return request_url(url, "text", file)


def retrieve_run_report(accession, fields=None, file=None):
    """Retrieve run report

    accession: accession id (study accessions (ERP, SRP, DRP, PRJ prefixes),
    experiment accessions (ERX, SRX, DRX prefixes), sample accessions (ERS,
    SRS, DRS, SAM prefixes) and run accessions)
    fields: comma-separated list of fields to have in the report (accessible
    with get_returnable_fields with result=read_run)
    file: filepath to save the content of the report
    """
    return retrieve_filereport(
        accession=accession,
        result="read_run",
        fields=fields,
        file=file)


def retrieve_analysis_report(accession, fields=None, file=None):
    """Retrieve analysis report

    accession: accession id (study accessions (ERP, SRP, DRP, PRJ prefixes),
    sample accessions (ERS, SRS, DRS, SAM prefixes) and analysis accessions)
    fields: comma-separated list of fields to have in the report (accessible
    with get_returnable_fields with result=analysis)
    file: filepath to save the content of the report
    """
    return retrieve_filereport(
        accession=accession,
        result="analysis",
        fields=fields,
        file=file)
