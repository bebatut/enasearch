#!/usr/bin/env python

import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    import enasearch
except:
    raise


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


def test_get_search_result_number():
    """Test get_search_result_number function"""
    nb = enasearch.get_search_result_number(
        query="tax_eq(10090)",
        result="assembly",
        need_check_result=True)
    assert nb == 19


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
