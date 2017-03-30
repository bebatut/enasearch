#!/usr/bin/env python

import requests
import pickle
from pprint import pprint


baseUrl = 'http://www.ebi.ac.uk/ena/'
lengthLimit = 100000


def load_object(filepath):
    """Load object from a pickle file

    filepath: path to pickle file with serialized data
    """
    with open(filepath, 'rb') as input:
        obj = pickle.load(input)
    return obj


results = load_object("data/result_description")
filter_types = load_object("data/filter_types")
download_options = load_object("data/download_options")
display_options = load_object("data/display_options")


def get_results(verbose=True):
    """Return the list of results in ENA as a dictionary with the key being the
    result id and the value the result description

    verbose: boolean to define the printing info
    """
    if verbose:
        for result in results:
            print("%s: %s" % (result, results[result]["description"]))
    return results


def check_result(result):
    """Check if result is in the list of possible results in ENA

    result: id of result to check
    """
    possible_results = get_results(verbose=False)
    if result not in possible_results:
        err_str = "The result value (%s) does not correspond to a " % (result)
        err_str += "possible result value in ENA"
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
        err_str = "The display value does not correspond to a possible display"
        err_str += "value in ENA"
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
    if length >= lengthLimit:
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


def retrieve_data(
    ids, display, download=None, file=None, offset=0, length=100000,
    range=None, expanded=None, res_range=None, header=None
):
    """Retrieve ENA data

    ids:
    display:
    download:
    file:
    offset:
    length:
    range:
    expanded:
    res_range:
    header:
    """
    url = baseUrl + "data/view/"
    check_display(display)
    print(url)


def retrieve_taxon(domain):
    """Retrieve taxon

    domain:
    """
    url = baseUrl + "data/view/Taxon"
    print(url)


def retrieve_marker(domain):
    """Retrieve marker

    domain:
    """
    url = baseUrl + "data/warehouse/search?"
    print(url)


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
    return int(r.text.split("\n")[0].split(": ")[1])


def search_data(
    query, result, display, download=None, file=None, offset=0, length=100000
):
    """Search ENA data

    query: query string, made up of filtering conditions, joined by logical
    ANDs, ORs and NOTs and bound by double quotes - the filter fields for a
    query are accessible with get_filter_fields and the type of filters with
    get_filter_types
    result: id of the result (partition of ENA db), accessible with get_results
    display:
    download:
    file:
    offset:
    length:
    """
    url = baseUrl + "data/warehouse/search?"
    url += "query=%s" + query

    check_result(result)
    url += "&result=%s" + result

    check_display(display)
    url += "&display=%s" + display

    if download is not None:
        check_download(download)
        url += "download=%s" + download

    check_length(length)


def retrieve_filereport(accession, result, fields=None):
    url = baseUrl + "data/warehouse/filereport"
    print(url)
