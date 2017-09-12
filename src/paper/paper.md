---
title: "ENASearch: A Python library for interacting with ENA's API"
tags:
  - European Nucleotide Archive
  - Python
  - API
  - REST
  - Galaxy
authors:
 - name: Bérénice Batut
   orcid: 0000-0001-9852-1987
   affiliation: 1
 - name: Björn Grüning
   orcid: 0000-0002-3079-6586
   affiliation: 1
affiliations:
 - name: Bioinformatics group, Freiburg, Germany
   index: 1
date: 11 September 2017
bibliography: paper.bib
---

# Summary

The European Nucleotide Archive (ENA) [@leinonen2010european] is a database with a comprehensive record of nucleotide sequencing information (raw sequencing data, sequence assembly information and functional annotation). The data contained in ENA can be accessed manually or programmatically via REST URLs. However, building HTTP-based REST requests is not always straightforward - a user friendly, high-level access is needed to make it easier to interact with ENA programmatically.

We developed ENASearch, a Python library to search and retrieve data from ENA database. It also allows for rich querying support by accessing different fields, filters or functions offered by ENA. ENASearch can be used as a Python package, through a command-line interface or inside Galaxy [@afgan2016galaxy].

# References