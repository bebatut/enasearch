Usage with command-line
=======================

ENASearch can be used via command-line with:

.. code-block:: bash

    $ enasearch --help
    Usage: enasearch [OPTIONS] COMMAND [ARGS]...

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

Commands
--------

.. click:: enasearch.cli:cli
   :prog: enasearch
   :show-nested: