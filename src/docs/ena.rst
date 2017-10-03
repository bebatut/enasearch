Interacting with ENA Database
=============================

Data
----

Data in ENA are organzed into 11 domains (or type): 

+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Domain     | Description                                                                                                                                                                  |
+============+==============================================================================================================================================================================+
| Assembly   | Information describing the construction of reads and sequence contigs into higher order scaffolds and chromosomes                                                            |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Sequence   | Assembled and, optionally, annotated assembled reads                                                                                                                         |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Coding     | A virtual domain comprising sequence regions reported by data providers as being protein-coding regions                                                                      |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Non-coding | A virtual domain comprising sequence regions reported by data providers as representing non-protein-coding (RNA)  genes                                                      |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Marker     | A virtual domain comprising information relating to phylogenetic, identification and molecular ecology marker  data                                                          |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Analysis   | Derived data forms, such as recalibrated aligned reads and metabarcoding identifications                                                                                     |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Read       | Raw sequencing reads from next generation platforms                                                                                                                          |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Trace      | Raw sequencing data from capillary platforms                                                                                                                                 |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Taxon      | Information relating to the organism that was the source of the sequenced biological sample                                                                                  |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Sample     | Information relating to the biological sample studied in the sequencing experiment                                                                                           |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Study      | Information relating to the scope of the sequencing effort; also known as 'Project', the primary use of study is to unite content otherwise dispersed across the ENA domains |
+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Each domains are further subdivided in some cases into data classes. It is the results that can be accessed:

+---------------+-------------------+----------------------------------------------------------+
| Domain        | Result            | Description                                              |
+===============+===================+==========================================================+
| Assembly      | assembly          | Genome assemblies                                        |
+---------------+-------------------+----------------------------------------------------------+
| Sequence      | sequence_release  | Nucleotide sequences (Release)                           |
+               +-------------------+----------------------------------------------------------+
|               | sequence_update   | Nucleotide sequences (Update)                            |
+               +-------------------+----------------------------------------------------------+
|               | wgs_set           | Genome assembly contig sets (WGS)                        |
+               +-------------------+----------------------------------------------------------+
|               | tsa_set           | Transcriptome assembly contig sets (TSA)                 |
+---------------+-------------------+----------------------------------------------------------+
| Coding        | coding_release    | Protein coding sequences (Release)                       |
+               +-------------------+----------------------------------------------------------+
|               | coding_update     | Protein coding sequences (Update)                        |
+---------------+-------------------+----------------------------------------------------------+
| Non-coding    | noncoding_release | Non-coding sequences (Release)                           |
+               +-------------------+----------------------------------------------------------+
|               | noncoding_update  | Non-coding sequences (Update)                            | 
+---------------+-------------------+----------------------------------------------------------+
| Analysis      | analysis_study    | Studies used for nucleotide sequence analyses from reads |
+               +-------------------+----------------------------------------------------------+
|               | analysis          | Nucleotide sequence analyses from reads                  |
+---------------+-------------------+----------------------------------------------------------+
| Read          | read_experiment   | Experiments used for raw reads                           |
+               +-------------------+----------------------------------------------------------+
|               | read_run          | Raw reads                                                |
+               +-------------------+----------------------------------------------------------+
|               | read_study        | Studies used for raw reads                               |
+---------------+-------------------+----------------------------------------------------------+
| Sample        | sample            | Samples                                                  |
+---------------+-------------------+----------------------------------------------------------+
| Taxon         | taxon             | Taxonomic classfication                                  |
+---------------+-------------------+----------------------------------------------------------+
| Environmental | environmental     | Environmental samples                                    |
+---------------+-------------------+----------------------------------------------------------+
| Study         | Study             | Studies                                                  |
+---------------+-------------------+----------------------------------------------------------+

This list can be accessed with `get_results`.

Each "result" can be searched, the outputs can be formatted and sorted given different fields. These fields are accessible via the commands:

- `get_filter_fields` to obtain the fields to build a query or filter (more information about the type of these filters with `get_filter_types`)
- `get_returnable_fields` to obtain the fields extractable for a result
- `get_sortable_fields` to obtain the fields usable to sort the outputs

Programmatic access
-------------------

The data on ENA can be accessed programmatically, in ENASearch:

- ENA database can be queried via `search_data`
- Data with an accession id can be retrieved via `retrieve_data`

    This function can not be used to

    - Retrieve taxonomic data

        It must be done via the taxon portal with `retrieve_taxons`. The taxonomy results can be accessed via `get_taxonomy_results`

    - Retrieve a run file report via a study accession (ERP, SRP, DRP, PRJ prefixes), experiment accession (ERX, SRX, DRX prefixes), sample accessions (ERS, SRS, DRS, SAM prefixes) or a run accessions (ERR, SRR, DRR prefixes)

        `retrieve_run_report` is used then. The fields accessible for the run report can be obtained with `get_run_fields`

    - Retrieve an analysis report via a study accession (ERP, SRP, DRP, PRJ prefixes), sample accession (ERS, SRS, DRS, SAM prefixes) or analysis accession (ERZ, SRZ, DRZ prefixes)

        `retrieve_analysis_report` is used then. The fields accessible for the run report can be obtained with `get_analysis_fields`
