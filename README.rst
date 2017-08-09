ENASearch
=========

.. image:: https://travis-ci.org/bebatut/enasearch.svg?branch=master
    :target: https://travis-ci.org/bebatut/enasearch
.. image:: https://badge.fury.io/py/enasearch.svg
    :target: https://badge.fury.io/py/enasearch
.. image:: https://anaconda.org/bioconda/enasearch/badges/installer/conda.svg
    :target: https://anaconda.org/bioconda/enasearch

ENASearch is a Python library for interacting with `ENA <http://www.ebi.ac.uk/ena/browse/programmatic-access>`_'s API.


Usage
-----

ENASearch is easy to use

.. code-block:: bash

    $ enasearch --help
    Usage: enasearch [OPTIONS] COMMAND [ARGS]...
    
    
    Options:
    
      --help  Show this message and exit.
    
    Commands:
      get_analysis_fields       Get analysis fields
      get_display_options       Get display options
      get_download_options      Get download options
      get_filter_fields         Get filter fields
      get_filter_types          Get filter types
      get_results               Get list of results
      get_returnable_fields     Get returnable fields
      get_run_fields            Get run fields
      get_sortable_fields       Get sortable fields
      get_taxonomy_results      Get list of taxonomy results
      retrieve_analysis_report  Retrieve analysis report
      retrieve_data             Retrieve ENA data
      retrieve_run_report       Retrieve run report
      retrieve_taxons           Retrieve ENA taxon data
      search_data               Search data

    $ enasearch search_data --help
    Usage: enasearch search_data [OPTIONS]

      Search data given a query

    Options:
        --free_text_search      Use free text search, otherwise the data warehouse
                                is used
        --query TEXT            Query string, made up of filtering conditions,
                                joined by logical ANDs, ORs and NOTs and bound by
                                double quotes; the filter fields for a query are
                                accessible with get_filter_fields and the type of
                                filters with get_filter_types  [required]
        --result TEXT           Id of a result (accessible with get_results)
                                [required]
        --display TEXT          Display option to specify the display format
                                (accessible with get_display_options)  [required]
        --download TEXT         Download option to specify that records are to be
                                saved in a file (used with file option, list
                                accessible with get_download_options)
        --file PATH             File to save the content of the search (used with
                                download option)
        --fields TEXT           Fields to return (accessible with
                                get_returnable_fields, used only for report as
                                display value) [multiple]
        --sortfields TEXT       Fields to sort the results (accessible with
                                get_sortable_fields, used only for report as display
                                value) [multiple]
        --offset INTEGER RANGE  First record to get (used only for display different
                                of fasta and fastq
        --length INTEGER RANGE  Number of records to retrieve (used only for display
                                different of fasta and fastq
        --help                  Show this message and exit.

It can also be used as a Python library:

.. code-block:: python

    >>> import enasearch
    >>> enasearch.retrieve_data(
            ids="A00145",
            display="fasta",
            download=None,
            file=None,
            offset=0,
            length=100000,
            subseq_range="3-63",
            expanded=None,
            header=None)
    [SeqRecord(seq=Seq('GAAGGAAGGTCTTCAGAGAACCTAGAGAGCAGGTTCACAGAGTCACCCACCTCA...GCC', SingleLetterAlphabet()), id='ENA|A00145|A00145.1', name='ENA|A00145|A00145.1', description='ENA|A00145|A00145.1 B.taurus BoIFN-alpha A mRNA : Location:3..63', dbxrefs=[])]

The information extracted from ENA can be in several formats: HTML, Text, XML, FASTA, FASTQ, ... XML outputs are transformed in a Python dictionary using xmltodict and the FASTA and FASTQ into SeqRecord objects using `BioPython <http://biopython.org/wiki/Biopython>`_.


Installation
------------

To install ENASearch, simply:

.. code-block:: bash

    $ pip install enasearch


Tests
-----

ENASearch comes with tests:

.. code-block:: bash

    $ make test


Generate the data descriptions
------------------------------

To run, ENASearch needs some data from ENA to describe how to query ENA. 
Currently, such information is manually extracted into CSV files in the `data` directory. Python objects are generated from these CSV files with

.. code-block:: bash

    $ python src/serialize_ena_data_descriptors.py

