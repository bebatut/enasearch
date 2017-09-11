Usage with command-line
=======================

ENASearch is easy to use

.. code-block:: bash

    $ enasearch --help
    Usage: enasearch [OPTIONS] COMMAND [ARGS]...

    Options:
      --version   Show the version and exit.
      -h, --help  Show this message and exit.

    Commands:
      get_analysis_fields       Get list of fields for an analysis
      get_display_options       Get list of options for display
      get_download_options      Get list of options for download
      get_filter_fields         Get filter fields
      get_filter_types          Get the types of filters usable to build a query
      get_results               Get list of possible results
      get_returnable_fields     Get list of returnable fields
      get_run_fields            Get list of fields for a run
      get_sortable_fields       Get the sortable fields for a result
      get_taxonomy_results      Get list of taxonomy results
      retrieve_analysis_report  Retrieve analysis report
      retrieve_data             Retrieve ENA data (other than taxon and project)
      retrieve_run_report       Retrieve run report
      retrieve_taxons           Retrieve ENA taxonomic data
      search_data               Search data given a query

Commands
--------

.. click:: enasearch.cli:cli
   :prog: enasearch
   :show-nested: