#!/usr/bin/env python

import csv
import pickle


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


def get_special_filters(filepath):
    """Extract the special (taxonomy or geospatial) filter description

    filepath: path with csv with filter description
    """
    filters = {}
    with open(filepath, "r") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            function = row["Function"]
            filters.setdefault(function, {})
            filters[function]["description"] = row["Description"]
            filters[function]["parameters"] = row["Parameters"].split(",")
            filters[function]["example"] = row["Example"]
    return filters


def get_filter_types():
    """Extract filter types
    """
    filter_types = {}
    filter_types["Boolean"] = {
        "operators": ["="],
        "values": ["yes", "true", "no", "false"]
    }
    filter_types["Controlled vocabulary"] = {
        "operators": ["=", "!="],
        "value": "A text value from the controlled vocabulary enclosed in \
        double quotes"
    }
    filter_types["Date"] = {
        "operators": ["=", "!=", "<", "<=", ">", ">="],
        "value": "A date in the format YYYY-MM-DD"
    }
    filter_types["Number"] = {
        "operators": ["=", "!=", "<", "<=", ">", ">="],
        "value": "Any integer"
    }
    filter_types["Text"] = {
        "operators": ["=", "!="],
        "value": "Any text value enclosed in double quotes. Wildcard (*) can \
        be used at the start and/or end of the text value."
    }
    filter_types["Geospatial"] = get_special_filters(
        "data/geospatial_filters.csv")
    filter_types["Taxonomy"] = get_special_filters(
        "data/taxonomy_filters.csv")
    return filter_types


def get_options(filepath):
    """Extract the option description

    filepath: path with csv with option description
    """
    options = {}
    with open(filepath, "r") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            function = row["Option"]
            options.setdefault(function, {})
            options[function]["description"] = row["Description"]
    return options


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

    filter_types = get_filter_types()
    save_object(filter_types, "data/filter_types")

    display_options = get_options("data/display_options.csv")
    save_object(display_options, "data/display_options")

    download_options = get_options("data/download_options.csv")
    save_object(download_options, "data/download_options")


if __name__ == "__main__":
    serialize_ena_data_descriptors()
