#!/usr/bin/env python

import csv
import pickle
from pprint import pprint


def get_filters(filepath):
    """Extract the filters from the file with description of filters in ENA as 
    a dictionary with the key being the filter id and the value a dictionary 
    with related results, type of filter, filter description

    filepath: path with csv with filter description
    """
    filters = {}
    with open(filepath, "r") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            filter_id = row["Filter Column"]
            filters.setdefault(filter_id, {})
            filters[filter_id]["results"] = row["Result"].split(", ")
            filters[filter_id]["type"] = row["Type"]
            filters[filter_id]["description"] = ''.join(row["Description"])
    return filters


def get_return_fields(filepath):
    """Extract the returnable fields for results from the file with 
    description of filters in ENA as a dictionary with the key being the field 
    id and the value a list of returnable fields

    filepath: path with csv with filter description
    """
    returnable_fields = {}
    with open(filepath, "r") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            field_id = row["Result"]
            returnable_fields.setdefault(
                row["Result"],
                row["Returnable fields"].split(", "))
    return returnable_fields


def get_results(filepath, filters, return_fields):
    """Format the file with description of results in ENA as a dictionary with 
    the key being the result id and the value a dictionary with the result 
    description, the filter fields, the returnable fields

    filepath: path with csv with result description
    filters: field filters description
    """
    results = {}
    with open(filepath, "r") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            result_id = row["Result"]
            results.setdefault(result_id, {})
            results[result_id]["description"] = row["Description"]
            results[result_id]["filter_fields"] = {}

            if result_id not in return_fields:
                err_str = "The result %s is not found for the " % (result_id)
                err_str += "returnable fields in ENA"
                raise ValueError(err_str)

            results[result_id]["returnable_fields"] = return_fields[result_id]

    for filt in filters:
        if filters[filt]["results"][0] == '':
            continue
        for result in filters[filt]["results"]:
            if result not in results:
                err_str = "The result %s is not a general result " % (result)
                err_str += "in ENA"
                raise ValueError(err_str)
            results[result]["filter_fields"].setdefault(
                filt,
                filters[filt])

    return results


def save_object(obj, filename):
    """Serialize a Python object into a file

    objects: list of Python object to serialize
    filepath: path to a file
    """
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, -1)


def serialize_ena_data_descriptors():
    """Serialize the ENA data descriptors
    """
    filter_fields = get_filters("data/ena_filter_columns.csv")
    return_fields = get_return_fields("data/ena_result_returnable_fields.csv")
    results = get_results(
        "data/ena_domain_results.csv",
        filter_fields,
        return_fields)
    save_object(results, "data/result_description")


if __name__ == "__main__":
    serialize_ena_data_descriptors()
    
