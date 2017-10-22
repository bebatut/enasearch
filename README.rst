ENASearch
=========

.. image:: https://travis-ci.org/bebatut/enasearch.svg?branch=master
    :target: https://travis-ci.org/bebatut/enasearch
.. image:: https://badge.fury.io/py/enasearch.svg
    :target: https://badge.fury.io/py/enasearch
.. image:: https://anaconda.org/bioconda/enasearch/badges/installer/conda.svg
    :target: https://anaconda.org/bioconda/enasearch
.. image:: https://codecov.io/gh/bebatut/enasearch/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bebatut/enasearch
.. image:: https://landscape.io/github/bebatut/enasearch/improve_code_health/landscape.svg?style=flat
    :target: https://landscape.io/github/bebatut/enasearch/improve_code_health
    :alt: Code Health

ENASearch is a Python library for interacting with `ENA <http://www.ebi.ac.uk/ena/browse/programmatic-access>`_'s API.

Context
-------

The `European Nucleotide Archive (ENA) <https://www.ebi.ac.uk/ena>`_ is a database with a comprehensive record of nucleotide sequencing information (raw sequencing data, sequence assembly information and functional annotation). The data contained in ENA can be accessed manually or programmatically via `REST URLs <http://www.ebi.ac.uk/ena/browse/programmatic-access>`_. However, building HTTP-based REST requests is not always straightforward - a user friendly, high-level access is needed to make it easier to interact with ENA programmatically.

We developed ENASearch, a Python library to search and retrieve data from ENA database. It also allows for rich querying support by accessing different fields, filters or functions offered by ENA. ENASearch can be used as a Python package, through a command-line interface or inside Galaxy.


Usage
-----

ENASearch can be used via command-line:

.. code-block:: bash

    $ enasearch --help
    Usage: enasearch [OPTIONS] COMMAND [ARGS]...

      The Python library for interacting with ENA's API

    Options:
      --version   Show the version and exit.
      -h, --help  Show this message and exit.

    Commands:
      get_analysis_fields       Get the fields extractable for an analysis.
      get_display_options       Get the list of possible formats to display...
      get_download_options      Get the options for download of data from...
      get_filter_fields         Get the filter fields of a result to build a...
      get_filter_types          Return the filters usable for the different...
      get_results               Get the possible results (type of data).
      get_returnable_fields     Get the fields extractable for a result.
      get_run_fields            Get the fields extractable for a run.
      get_sortable_fields       Get the fields of a result that can sorted.
      get_taxonomy_results      Get list of taxonomy results.
      retrieve_analysis_report  Retrieve analysis report from ENA.
      retrieve_data             Retrieve ENA data (other than taxon).
      retrieve_run_report       Retrieve run report from ENA.
      retrieve_taxons           Retrieve data from the ENA Taxon Portal.
      search_data               Search data given a query.

    $ enasearch search_data --help
    Usage: enasearch search_data [OPTIONS]

      Search data given a query.

      This function

      - Extracts the number of possible results for the query - Extracts the all
      the results of the query (by potentially running several times the search
      function)

      The output can be redirected to a file and directly display to the
      standard output given the display chosen.

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
                              display value) [multiple or comma-separated]
      --sortfields TEXT       Fields to sort the results (accessible with
                              get_sortable_fields, used only for report as display
                              value) [multiple or comma-separated]
      --offset INTEGER RANGE  First record to get (used only for display different
                              of fasta and fastq
      --length INTEGER RANGE  Number of records to retrieve (used only for display
                              different of fasta and fastq
      -h, --help              Show this message and exit.

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

ENASearch can be installed with pip:

.. code-block:: bash

    $ pip install enasearch

or with conda:

.. code-block:: bash

    $ conda install -c bioconda enasearch

Tests
-----

ENASearch comes with tests:

.. code-block:: bash

    $ make test

These tests are automatically run on `TravisCI <https://travis-ci.org/bebatut/enasearch>`_ for each Pull Request.

Documentation
-------------

Documentation about ENASearch is available online at `http://bebatut.fr/enasearch <http://bebatut.fr/enasearch>`_

To update it:

1. Make the changes in `src/docs`
2. Generate the doc with 

  .. code-block:: bash

    $ make doc

3. Check it by opening the `docs/index.html <docs/index.html>`_ file in a web browser
4. Propose the changes via a Pull Request

Generate the data descriptions
------------------------------

To run, ENASearch needs some data from ENA to describe how to query ENA. 
Currently, such information is manually extracted into CSV files in the `data` directory. Python objects are generated from these CSV files with

.. code-block:: bash

    $ python src/serialize_ena_data_descriptors.py

