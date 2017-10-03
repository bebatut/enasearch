Some example of usage
=====================

Original use case
-----------------

This project started with a simple problem. We had a list of thousands of ENA's run ids with possibly interesting metagenomic datasets. We needed to select some of these datasets based on several criteria (platform used for the sequencing, library preparation strategy, number of reads and bases sequenced, etc) and download them afterwards. 

The metadata are accessible via ENA. For example for the run "ERR1558694", the information can be accessed at `https://www.ebi.ac.uk/ena/data/view/ERR1558694 <https://www.ebi.ac.uk/ena/data/view/ERR1558694>`_ or programmatically via:

.. code-block:: bash

    $ curl "https://www.ebi.ac.uk/ena/data/warehouse/filereport?accession=ERR1558694&result=read_run"

We can also choose the fields to extract

.. code-block:: bash

    $ curl "https://www.ebi.ac.uk/ena/data/warehouse/filereport?accession=ERR1558694&result=read_run&fields=run_accession,instrument_platform,library_strategy,read_count,fastq_ftp"

    run_accession   instrument_platform library_strategy    read_count  fastq_ftp
    ERR1558694  ILLUMINA    WGS 1259641 ftp.sra.ebi.ac.uk/vol1/fastq/ERR155/004/ERR1558694/ERR1558694_1.fastq.gz;ftp.sra.ebi.ac.uk/vol1/fastq/ERR155/004/ERR1558694/ERR1558694_2.fastq.gz

We started to write these URLs with Python, but they are often difficult to build (without error, specially for the names of the fields). And the extracted information has to be integrated into downstream Python scripts. We thought that a Python library to interact with ENA's API could be useful. It could help to query ENA's database, give the list of possible fields for a type of data, download data from ENA, etc. This library could be used inside Python scripts but also through command-lines inside BASH scripts.

If we come back to our initial problem, we can now use ENASearch start inside Python:

.. code-block:: python

    >>> import enasearch

First, we would like to know the accessible metadata for a run ("read_run" type in ENA):

.. code-block:: python

    >>> enasearch.get_returnable_fields(result="read_run", verbose=False)

    ['study_accession', 'secondary_study_accession', 'sample_accession', 'secondary_sample_accession', 'experiment_accession', 'run_accession', 'submission_accession', 'tax_id', 'scientific_name', 'instrument_platform', 'instrument_model', 'library_name', 'nominal_length', 'library_layout', 'library_strategy', 'library_source', 'library_selection', 'read_count', 'base_count', 'center_name', 'first_public', 'last_updated', 'experiment_title', 'study_title', 'study_alias', 'experiment_alias', 'run_alias', 'fastq_bytes', 'fastq_md5', 'fastq_ftp', 'fastq_aspera', 'fastq_galaxy', 'submitted_bytes', 'submitted_md5', 'submitted_ftp', 'submitted_aspera', 'submitted_galaxy', 'submitted_format', 'sra_bytes', 'sra_md5', 'sra_ftp', 'sra_aspera', 'sra_galaxy', 'cram_index_ftp', 'cram_index_aspera', 'cram_index_galaxy', 'sample_alias', 'broker_name']

We now would like to access the instrument platform, the library strategy and the read_count for the run "ERR1558694"

.. code-block:: python

    >>> enasearch.retrieve_run_report(accession="ERR1558694", fields="run_accession,instrument_platform,library_strategy,read_count,fastq_ftp")

    'run_accession\tinstrument_platform\tlibrary_strategy\tread_count\tfastq_ftp\nERR1558694\tILLUMINA\tWGS\t1259641\tftp.sra.ebi.ac.uk/vol1/fastq/ERR155/004/ERR1558694/ERR1558694_1.fastq.gz;ftp.sra.ebi.ac.uk/vol1/fastq/ERR155/004/ERR1558694/ERR1558694_2.fastq.gz\n'

We could have put this information directly into a file (with `file=<filepath>` in the previous command). We can now parse this string to extract useful information and choose (or not) to conserve this run for downstream analyses, and for example download the files using the FTP link extracted.

Search and retrieve data
------------------------

We now would like to find the sequences related to the SMP1 gene in human. We will use the `search_all_data` function

.. code-block:: python

    >>> help(enasearch.search_data)

    Help on function search_data in module enasearch:

    search_data(free_text_search, query, result, display, offset=None, length=None, download=None, file=None, fields=None, sortfields=None)
        Search ENA data

        :param free_text_search: boolean to describe the type of query
        :param query: query string, made up of filtering conditions, joined by logical ANDs, ORs and NOTs and bound by double quotes
        :param result: id of the result (partition of ENA db), accessible with get_results
        :param display: display option to specify the display format (accessible with get_display_options)
        :param offset: first record to get
        :param length: number of records to retrieve
        :param download: download option to specify that records are to be saved in a file (used with file option)
        :param file: filepath to save the content of the search (used with download option)
        :param fields: comma-separated list of fields to return (only if display=report)
        :param sortfields: comma-separated list of fields to sort the results (only if display=report)

We would like to find ENA data related to human kinase, so

- `free_text_search` is "True" and `query` is "SMP1+homo" (terms joined with "+")

    In case of search without free text, requests are queried on the ENA data warehouse. The query can be made up of filtering conditions, joined by logical ANDs, ORs and NOTs and bound by double quotes. The use of parentheses is also supported. You can check the `documentation on ENA <https://www.ebi.ac.uk/ena/browse/search-rest>`_, and use functions as `get_filter_types` or `get_results` to help you building such query.

- `results`

    .. code-block:: python

        >>> res = enasearch.get_results()

        noncoding_update    Non-coding sequences (Update)
        wgs_set Genome assembly contig set
        taxon   Taxonomic classification
        read_study  Raw reads (grouped by study)
        analysis_study  Nucleotide sequence analyses from reads (grouped by study)
        tsa_set Transcriptome assembly contig set
        sequence_update Nucleotide sequences (Update)
        coding_release  Protein-coding sequences (Release)
        noncoding_release   Non-coding sequences (Release)
        assembly    Genome assemblies
        environmental   Environmental samples
        sample  Samples
        analysis    Nucleotide sequence analyses from reads
        study   Studies
        read_run    Raw reads
        read_experiment Raw reads (grouped by experiment)
        sequence_release    Nucleotide sequences (Release)
        coding_update   Protein-coding sequences (Update)

    We are interested in the sequence, we choose then "sequence_release"

- `offset` and `length` 

    By default the first 100,000 records are returned (`offset` = 0 and `length` = 10000). We would like to first know how many records are available for this query:

    .. code-block:: python

        >>> enasearch.get_search_result_number(
            free_text_search=True,
            query="SMP1+homo",
            result="sequence_release")

        12

    With the default values, all sequences will be extracted. To be sure to obtain all records, you can also use the `search_all_data` function.

- `display` to "fasta":

    .. code-block:: python

        >>> enasearch.get_display_options()

        {'xml': {'description': 'Results are displayed in XML format. Supported by all ENA data classes.'}, 'fasta': {'description': 'Results are displayed in fasta format. Supported by assembled and annotated sequence and Trace data classes.'}, 'fastq': {'description': 'Results are displayed in fastq format. Supported only by Trace data class.'}, 'text': {'description': 'Results are displayed in text format. Supported only by assembled and annotated sequence data classes.'}, 'report': {'description': 'Results are displayed as a tab separated report'}, 'html': {'description': 'Results are displayed in HTML format. Supported by all ENA data classes. HTML is the default display format if no other display option has been specified.'}}

- `download` will not be set here (we do not want to save the result in a file)
- `fields` and `sortfields` do not have to be set because `display` is not a "report"

The query is then

.. code-block:: python

    >>> data = enasearch.search_data(
        free_text_search=True,
        query="SMP1+homo",
        result="sequence_release",
        display="fasta")

    [SeqRecord(seq=Seq('TTGTTTTCTTGGCTAAAATCGGGGGAGTGAGGCGGGCCGGCGCGCGCACAACCG...AAA', SingleLetterAlphabet()), id='ENA|AF081282|AF081282.1', name='ENA|AF081282|AF081282.1', description='ENA|AF081282|AF081282.1 Homo sapiens small membrane protein 1 (SMP1) mRNA, complete cds.', dbxrefs=[]), SeqRecord(seq=Seq('ATTAGCCGGCCCAAAACCTCAGTAGTGCCCAGGCTGAGAAACCCTGCCTTAAAC...CCC', SingleLetterAlphabet()), id='ENA|AF458851|AF458851.1', name='ENA|AF458851|AF458851.1', description='ENA|AF458851|AF458851.1 Homo sapiens small membrane protein 1 (SMP1) gene, complete cds.', dbxrefs=[]), SeqRecord(seq=Seq('AAACGCTCATGACAGCAAAGTCTCCAATGTTCGCGCAGGCACTGGAGTCAGAGA...GGC', SingleLetterAlphabet()), id='ENA|AJ252312|AJ252312.1', name='ENA|AJ252312|AJ252312.1', description='ENA|AJ252312|AJ252312.1 Homo sapiens genomic downstream Rhesus box', dbxrefs=[]), SeqRecord(seq=Seq('CTAGAAAACACTTTGTCATTTTAGAGGTGTTATCCAATGTTCGCGCAGGCACTG...GGC', SingleLetterAlphabet()), id='ENA|AJ252313|AJ252313.1', name='ENA|AJ252313|AJ252313.1', description='ENA|AJ252313|AJ252313.1 Homo sapiens genomic hybrid Rhesus box', dbxrefs=[]), SeqRecord(seq=Seq('TTGTTGGCCTACTGGAAAATAAAAAAAAAAAGGGAAACTGCGCGACTGAGCCGG...TTA', SingleLetterAlphabet()), id='ENA|AU100113|AU100113.2', name='ENA|AU100113|AU100113.2', description='ENA|AU100113|AU100113.2 Homo sapiens cDNA clone:LNG08923, similar to Homo sapiens small membrane protein 1 (SMP1) mRNA, 5&apos;-EST.', dbxrefs=[]), SeqRecord(seq=Seq('CTGCTGCATCCGGGTGTCTGGAGGCTGTGGCCGTTTTGTTTTCTTGGCTAAAAT...CTG', SingleLetterAlphabet()), id='ENA|AY358650|AY358650.1', name='ENA|AY358650|AY358650.1', description='ENA|AY358650|AY358650.1 Homo sapiens clone DNA49647 SMP1 (UNQ386) mRNA, complete cds.', dbxrefs=[]), SeqRecord(seq=Seq('GATCAACGCAAAGGACTAAGCACTGCTGCCAAAAGCCACCAGCCCCAGAGACAA...ATC', SingleLetterAlphabet()), id='ENA|BN000065|BN000065.1', name='ENA|BN000065|BN000065.1', description='ENA|BN000065|BN000065.1 TPA: Homo sapiens SMP1 gene, RHD gene and RHCE gene', dbxrefs=[]), SeqRecord(seq=Seq('CCACGCGTCCGCGGACGCGTGGGCCGGCGGCCTGTGGCTGTTTTGCTTTCTTGG...TGC', SingleLetterAlphabet()), id='ENA|CX060942|CX060942.1', name='ENA|CX060942|CX060942.1', description='ENA|CX060942|CX060942.1 PDUts2051F04 Porcine testis cDNA library II Sus scrofa cDNA clone PDUts2051F04 5&apos; similar to homologue to ref|NM_014313.2| Homo sapiens small membrane protein 1 (SMP1), mRNA, mRNA sequence.', dbxrefs=[]), SeqRecord(seq=Seq('CCACGCGTCCGCCCACGCGTCCGATCCGGCGGCCTGTGGCTGTTTTGCTTTCTT...ACC', SingleLetterAlphabet()), id='ENA|CX062415|CX062415.1', name='ENA|CX062415|CX062415.1', description='ENA|CX062415|CX062415.1 PDUts2067F11 Porcine testis cDNA library II Sus scrofa cDNA clone PDUts2067F11 5&apos; similar to homologue to ref|NM_014313.2| Homo sapiens small membrane protein 1 (SMP1), mRNA, mRNA sequence.', dbxrefs=[]), SeqRecord(seq=Seq('GCACGAGGCGGAACCACTGCACGACGGGGCTGGACTGACCTGAAAAAAAGTCTG...AAA', SingleLetterAlphabet()), id='ENA|DN994344|DN994344.1', name='ENA|DN994344|DN994344.1', description='ENA|DN994344|DN994344.1 TC115076 Human adult whole brain, large insert, pCMV expression library Homo sapiens cDNA clone TC115076 5&apos; similar to Homo sapiens small membrane protein 1 (SMP1), mRNA sequence.', dbxrefs=[]), SeqRecord(seq=Seq('CCGTGTCCGCATGCGCGACTGAGCCGGGTGGATGGTACTGCTGCATCCGGGTGT...TAA', SingleLetterAlphabet()), id='ENA|JX644905|JX644905.1', name='ENA|JX644905|JX644905.1', description='ENA|JX644905|JX644905.1 Homo sapiens small membrane protein 1 (SMP1) mRNA, SMP1-RHC allele, complete cds.', dbxrefs=[]), SeqRecord(seq=Seq('CCGTGTCCGCATGCGCGACTGAGCCGGGTGGATGGTACTGCTGCATCCGGGTGT...TAA', SingleLetterAlphabet()), id='ENA|JX644906|JX644906.1', name='ENA|JX644906|JX644906.1', description='ENA|JX644906|JX644906.1 Homo sapiens small membrane protein 1 (SMP1) mRNA, SMP1-RHc allele, complete cds.', dbxrefs=[])]

The result (`data`) is a list of sequences, represented as SeqRecord object:

.. code-block:: python

    >>> print(data[0])

    ID: ENA|AF081282|AF081282.1
    Name: ENA|AF081282|AF081282.1
    Description: ENA|AF081282|AF081282.1 Homo sapiens small membrane protein 1 (SMP1) mRNA, complete cds.
    Number of features: 0
    Seq('TTGTTTTCTTGGCTAAAATCGGGGGAGTGAGGCGGGCCGGCGCGCGCACAACCG...AAA', SingleLetterAlphabet())

    >>> print(data[0].seq[:100])

    TTGTTTTCTTGGCTAAAATCGGGGGAGTGAGGCGGGCCGGCGCGCGCACAACCGGGCTCCGGAACCACTGCACGACGGGGCTGGACTGACCTGAAAAAAA

To learn more about these object, you can have a look at `BioPython documentation <http://biopython.org/wiki/SeqRecord>`_.
