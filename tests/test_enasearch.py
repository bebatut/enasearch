#!/usr/bin/env python
from pprint import pprint
import enasearch


def cmp(la, lb):
    """Compare two lists"""
    return all(s in lb for s in la) and all(s in la for s in lb)


def test_get_results():
    """Test get_results function"""
    results = enasearch.get_results(verbose=False)
    exp_results = [
        'wgs_set', 'analysis_study', 'study', 'read_run', 'coding_release',
        'coding_update', 'analysis', 'environmental', 'tsa_set',
        'sequence_update', 'noncoding_update', 'noncoding_release', 'sample',
        'read_experiment', 'read_study', 'assembly', 'taxon',
        'sequence_release']
    assert len(results) == 18 and cmp(results.keys(), exp_results)


def test_get_taxonomy_results():
    """Test get_taxonomy_results function"""
    results = enasearch.get_taxonomy_results(verbose=False)
    exp_taxo_results = [
        'sequence_release', 'sequence_update', 'coding_release',
        'coding_update', 'noncoding_release', 'noncoding_update',
        'sample', 'study', 'analysis', 'analysis_study', 'read_run',
        'read_experiment', 'read_study', 'read_trace']
    assert cmp(results.keys(), exp_taxo_results)


def test_get_search_result_number():
    """Test get_search_result_number function"""
    nb = enasearch.get_search_result_number(
        free_text_search=False,
        query="tax_eq(10090)",
        result="assembly",
        need_check_result=True)
    assert nb == 19

    nb = enasearch.get_search_result_number(
        free_text_search=False,
        query="tax_tree(7147) AND dataclass=STD",
        result="coding_update",
        need_check_result=True)
    assert nb >= 17123

    nb = enasearch.get_search_result_number(
        free_text_search=True,
        query="kinase+homo+sapiens",
        result="sequence_update",
        need_check_result=True)
    assert nb >= 15


def test_get_filter_types():
    """Test get_filter_types function"""
    filter_types = enasearch.get_filter_types(verbose=False)
    assert "Boolean" in filter_types
    assert "geo_box1" in filter_types["Geospatial"]


def test_get_display_options():
    """Test get_display_options function"""
    display_options = enasearch.get_display_options(verbose=False)
    assert "html" in display_options
    assert "fasta" in display_options


def test_get_download_options():
    """Test get_download_options function"""
    download_options = enasearch.get_download_options(verbose=False)
    assert "gzip" in download_options
    assert "txt" in download_options


def test_get_filter_fields():
    """Test get_filter_fields function"""
    filter_fields = enasearch.get_filter_fields(
        result="assembly",
        verbose=False)
    assert "accession" in filter_fields


def test_get_returnable_fields():
    """Test get_returnable_fields function"""
    returnable_fields = enasearch.get_returnable_fields(
        result="read_study",
        verbose=False)
    assert "secondary_study_accession" in returnable_fields


def test_get_sortable_fields():
    """Test get_sortable_fields function"""
    sortable_fields = enasearch.get_returnable_fields(
        result="sequence_update",
        verbose=False)
    assert "haplotype" in sortable_fields


def test_search_data():
    """Test search_data function"""
    search_data = enasearch.search_data(
        free_text_search=False,
        query="tax_tree(7147) AND dataclass=STD",
        result="coding_release",
        display="fasta",
        offset=0,
        length=20,
        download=None,
        file=None,
        fields=None,
        sortfields=None)
    assert len([seq.id for seq in search_data]) > 0


def test_search_all_data():
    """Test search_all_data function"""
    search_data = enasearch.search_all_data(
        free_text_search=True,
        query="kinase+homo+sapiens",
        result="sequence_update",
        display="fasta",
        download=None,
        file=None)
    nb = enasearch.get_search_result_number(
        free_text_search=True,
        query="kinase+homo+sapiens",
        result="sequence_update",
        need_check_result=True)
    assert len([seq.id for seq in search_data]) == nb


def test_retrieve_data():
    """Test retrieve_data function"""
    data = enasearch.retrieve_data(
        ids="ERA000010-ERA000020",
        display="xml",
        download=None,
        file=None,
        offset=None,
        length=None,
        subseq_range=None,
        expanded=None,
        header=None)
    assert "ROOT" in data
    data = enasearch.retrieve_data(
        ids="A00145",
        display="fasta",
        download=None,
        file=None,
        offset=0,
        length=100000,
        subseq_range="3-63",
        expanded=None,
        header=None)
    pprint([seq.id for seq in data])
    assert 'ENA|A00145|A00145.1' in [seq.id for seq in data]
    data = enasearch.retrieve_data(
        ids="AL513382",
        display="text",
        download=None,
        file=None,
        offset=0,
        length=100000,
        subseq_range=None,
        expanded="true",
        header=None)
    pprint(data)
    assert "AL513382" in data and len(data.split("\n")) >= 200000
    data = enasearch.retrieve_data(
        ids="AL513382",
        display="text",
        download=None,
        file=None,
        offset=0,
        length=100000,
        subseq_range=None,
        expanded=None,
        header="true")
    pprint(data)
    assert "AL513382" in data and len(data.split("\n")) >= 745
    data = enasearch.retrieve_data(
        ids="PRJEB2772",
        display="xml",
        download=None,
        file=None,
        offset=0,
        length=100000,
        subseq_range=None,
        expanded=None,
        header=None)
    pprint(data)
    assert "ROOT" in data


def test_retrieve_taxons():
    """Test retrieve_taxons function"""
    data = enasearch.retrieve_taxons(
        ids="6543",
        display="fasta",
        result="sequence_release",
        download=None,
        file=None,
        offset=0,
        length=100000,
        subseq_range=None,
        expanded=None,
        header=None)
    assert 'ENA|KT626607|KT626607.1' in [seq.id for seq in data]
    data = enasearch.retrieve_taxons(
        ids="Human,Cat,Mouse,Zebrafish",
        display="xml",
        result=None,
        download=None,
        file=None,
        offset=0,
        length=100000,
        subseq_range=None,
        expanded=None,
        header=None)
    assert "ROOT" in data


def test_retrieve_run_report():
    """Test retrieve_run_report function"""
    report = enasearch.retrieve_run_report(
        accession="SRX017289",
        fields=None,
        file=None)
    assert "small RNAs_wild type" in report
    exp_fields = ["run_accession", "fastq_ftp", "fastq_md5", "fastq_bytes"]
    report = enasearch.retrieve_run_report(
        accession="SRX017289",
        fields=",".join(exp_fields),
        file=None)
    assert cmp(report.split("\n")[0].split("\t"), exp_fields)


def test_retrieve_analysis_report():
    """Test retrieve_analysis_report function"""
    exp_fields = ["analysis_accession", "sample_accession", "scientific_name"]
    report = enasearch.retrieve_analysis_report(
        accession="PRJNA123835",
        fields=",".join(exp_fields),
        file=None)
    assert cmp(report.split("\n")[0].split("\t"), exp_fields)
