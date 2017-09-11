---
title: "ENASearch: A Python library for interacting with ENA's API"
tags:
  - European Nucleotide Archive
  - Python
  - API
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

The European Nucleotide Archive (ENA) [@leinonen2010european] is a database providing acces to a comprehensive record of nucleotide sequencing information (raw sequencing data, sequence assembly information and functional annotation). ENA provides a programmatic access to the database via REST URLs via 5 main portals (Data, Taxon, Marker, Search and File reports).

ENASearch is a Python library to search and retrieve data from ENA database. It allows also to access the different fields or possible options to build a request on ENA, with many different functions. ENASearch can also be used through a command-line interface or inside Galaxy [@afgan2016galaxy].

# References