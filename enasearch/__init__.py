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


def get_results(verbose=True):
    """Return the list of results in ENA as a dictionary with the key being the
    result id and the value the result description

    verbose: boolean to define the printing info
    """
    results = load_object("data/result_description")
    if verbose:
        for result in results:
            print("%s: %s" % (result, results[result]["description"]))
    return results


def check_display(display):
    """Check if display is in the list of display in ENA

    display: display to check
    """
    expectedDisplay = ["html", "xml", "text", "fasta", "fastq", "dwc"]
    if display not in expect_display:
        err_str = "The display value does not correspond to a possible display"
        err_str += "value in ENA"
        raise ValueError(err_str)


def check_download(download):
    """Check if download is in the list of download format in ENA

    download: download format to check
    """
    expectedDownload = ["gzip", "txt"]
    if download not in expectedDownload:
        err_str = "The download value does not correspond to a possible "
        err_str += "display value in ENA"
        raise ValueError(err_str)


def check_result(result):
    """Check if result is in the list of possible results in ENA

    result: id of result to check
    """
    possible_results = get_results(verbose=False)
    if result not in possible_results:
        err_str = "The result value (%s) does not correspond to a " % (result)
        err_str += "possible result value in ENA"
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
    url = baseUrl + "data/view/graphics/" 


def retrieve_data(
    ids, display, download = None, file = None, offset = 0, length = 100000, 
    range = None, expanded = None, res_range = None, header = None):
    url = baseUrl + "data/view/"

    check_display(display)
    

def retrieve_taxon(domain):
    url = baseUrl + "data/view/Taxon"

def retrieve_marker(domain):
    url = baseUrl + "data/warehouse/search?"


def get_search_result_number(query, result, need_check_result = True):
    """Get the number of results for a query on a result

    query: query string, made up of filtering conditions, joined by logical 
    ANDs, ORs and NOTs and bound by double quotes
    result: id of the result (partition of ENA db)
    """
    url = baseUrl + "data/warehouse/search?"
    url += "query=%s" + query

    if need_check_result:
        check_result(result)
    url += "&result=%s" + result

    url += "&resultcount"
    r = requests.get(
        url,
        headers={"accept": "application/json"})
    r.raise_for_status()
    return r.json()


def search_data(
    query, result, display, download = None, file = None, offset = 0, 
    length = 100000):
    """Search ENA data

    query: domain id in EBI
    result: 
    display: 
    download: 
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

def retrieve_filereport(accession, result, fields = None):
    url = baseUrl + "data/warehouse/filereport"