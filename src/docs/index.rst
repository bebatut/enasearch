Welcome to ENASearch's documentation!
=====================================

The `European Nucleotide Archive (ENA) <https://www.ebi.ac.uk/ena>`_ is a database with a comprehensive record of nucleotide sequencing information (raw sequencing data, sequence assembly information and functional annotation). The data contained in ENA can be accessed manually or programmatically via `REST URLs <http://www.ebi.ac.uk/ena/browse/programmatic-access>`_. However, building HTTP-based REST requests is not always straightforward - a user friendly, high-level access is needed to make it easier to interact with ENA programmatically.

We developed ENASearch, a Python library to search and retrieve data from ENA database. It also allows for rich querying support by accessing different fields, filters or functions offered by ENA. ENASearch can be used as a Python package, through a command-line interface or inside Galaxy.


.. toctree::
  :caption: ENASearch documentation
  :maxdepth: 4

  installation
  use_case
  ena
  cli_usage
  api_usage
  contributing
  Source code on GitHub <https://github.com/bebatut/enasearch>