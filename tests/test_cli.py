#!/usr/bin/env python
from click.testing import CliRunner
from enasearch.cli import cli


def test_get_results():
    """Test get_results command of enasearch"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get_results'])
    assert result.exit_code == 0
    assert result.output.find('tsa_set') != -1


def test_get_taxonomy_results():
    """Test get_taxonomy_results command of enasearch"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get_taxonomy_results'])
    assert result.exit_code == 0
    assert result.output.find('sequence_update') != -1


def test_get_filter_fields():
    """Test get_filter_fields command of enasearch"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get_filter_fields', '--result', 'assembly'])
    assert result.exit_code == 0
    assert result.output.find('assembly_name') != -1


def test_get_returnable_fields():
    """Test get_returnable_fields command of enasearch"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get_returnable_fields', '--result', 'read_study'])
    assert result.exit_code == 0
    assert result.output.find('study_alias') != -1


def test_get_run_fields():
    """Test get_run_fields command of enasearch"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get_run_fields'])
    assert result.exit_code == 0
    assert result.output.find('library_selection') != -1


def test_get_analysis_fields():
    """Test get_analysis_fields command of enasearch"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get_analysis_fields'])
    assert result.exit_code == 0
    assert result.output.find('submitted_md5') != -1


def test_get_sortable_fields():
    """Test get_sortable_fields command of enasearch"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get_sortable_fields', '--result', 'sequence_update'])
    assert result.exit_code == 0
    assert result.output.find('tissue_lib') != -1


def test_get_filter_types():
    """Test get_filter_types command of enasearch"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get_filter_types'])
    assert result.exit_code == 0
    assert result.output.find('geo_south') != -1


def test_get_display_options():
    """Test get_display_options command of enasearch"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get_display_options'])
    assert result.exit_code == 0
    assert result.output.find('report') != -1


def test_get_download_options():
    """Test get_download_options command of enasearch"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get_download_options'])
    assert result.exit_code == 0
    assert result.output.find('gzip') != -1


def test_search_data():
    """Test search_data command of enasearch"""
    runner = CliRunner()
    # 1st test
    result = runner.invoke(cli, [
        'search_data',
        '--query',
        'tissue_lib="lambda gt11" AND dataclass=STD',
        '--result',
        'coding_release',
        '--display',
        'xml'])
    assert result.exit_code == 0
    assert result.output.find('glutathione S-transferase subunit gYc') != -1
    # 2nd test
    result = runner.invoke(cli, [
        'search_data',
        '--free_text_search',
        '--query',
        'kinase+homo+sapiens',
        '--result',
        'sequence_update',
        '--display',
        'fasta'])
    assert result.exit_code == 0
    assert result.output.find('ENA|MS943646|MS943646.1') != -1
    # 3rd test
    result = runner.invoke(cli, [
        'search_data',
        '--free_text_search',
        '--query',
        'kinase+homo+sapiens',
        '--result',
        'wgs_set',
        '--display',
        'report',
        '--fields',
        'accession,environmental_sample'])
    assert result.exit_code == 0
    assert result.output.find('query=kinase homo sapiens') != -1


def test_retrieve_data():
    """Test retrieve_data command of enasearch"""
    runner = CliRunner()
    # 1st test
    result = runner.invoke(cli, [
        'retrieve_data',
        '--ids',
        'ERA000010-ERA000020',
        '--display',
        'xml'])
    assert result.exit_code == 0
    assert result.output.find('g1k-bgi-20080814-2') != -1
    # 2nd test
    result = runner.invoke(cli, [
        'retrieve_data',
        '--ids',
        'PRJEB2772,AL513382',
        '--display',
        'html'])
    assert result.exit_code == 0
    assert result.output.find('BN000065') != -1
    # 3rd test
    result = runner.invoke(cli, [
        'retrieve_data',
        '--ids',
        'A00145',
        '--display',
        'fasta',
        '--subseq_range',
        '3-63'])
    assert result.exit_code == 0
    assert result.output.find('ENA|A00145|A00145.1') != -1
    # 4th test
    result = runner.invoke(cli, [
        'retrieve_data',
        '--ids',
        'AL513382',
        '--display',
        'text',
        '--offset',
        '0',
        '--length',
        '100',
        '--expanded'])
    assert result.exit_code == 0
    assert result.output.find('taatttttaa') != -1
    # 5th test
    result = runner.invoke(cli, [
        'retrieve_data',
        '--ids',
        'AL513382',
        '--display',
        'text',
        '--header'])
    assert result.exit_code == 0
    assert result.output.find('UniProtKB/Swiss-Prot; Q08456; FIMI_SALTI') != -1
    # 6th test
    result = runner.invoke(cli, [
        'retrieve_data',
        '--ids',
        'PRJEB2772',
        '--display',
        'xml'])
    assert result.exit_code == 0
    assert result.output.find('ERP001030') != -1


def test_retrieve_taxons():
    """Test retrieve_taxons command of enasearch"""
    runner = CliRunner()
    # 1st test
    result = runner.invoke(cli, [
        'retrieve_taxons',
        '--ids',
        '6543',
        '--display',
        'fasta',
        '--result',
        'sequence_release'])
    assert result.exit_code == 0
    assert result.output.find('ENA|KX834745|KX834745.1') != -1
    # 2nd test
    result = runner.invoke(cli, [
        'retrieve_taxons',
        '--ids',
        'Human,Cat,Mouse,Zebrafish',
        '--display',
        'xml'])
    assert result.exit_code == 0
    assert result.output.find('Danio frankei') != -1


def test_retrieve_run_report():
    """Test retrieve_run_report command of enasearch"""
    runner = CliRunner()
    # 1st test
    result = runner.invoke(cli, [
        'retrieve_run_report',
        '--accession',
        'SRX017289'])
    assert result.exit_code == 0
    assert result.output.find('SAMN00009557') != -1
    # 2nd test
    result = runner.invoke(cli, [
        'retrieve_run_report',
        '--accession',
        'SRX017289',
        '--fields',
        'study_accession,study_title,sra_aspera'])
    assert result.exit_code == 0
    assert result.output.find('PRJNA123835') != -1
    # 3rd test
    result = runner.invoke(cli, [
        'retrieve_run_report',
        '--accession',
        'SRX017289',
        '--fields',
        'study_accession',
        '--fields',
        'study_title',
        '--fields',
        'sra_aspera'])
    assert result.exit_code == 0
    assert result.output.find('PRJNA123835') != -1


def test_retrieve_analysis_report():
    """Test retrieve_analysis_report command of enasearch"""
    runner = CliRunner()
    # 1st test
    result = runner.invoke(cli, [
        'retrieve_analysis_report',
        '--accession',
        'ERZ009929'])
    assert result.exit_code == 0
    assert result.output.find('PRJEB1970') != -1
    # 2nd test
    result = runner.invoke(cli, [
        'retrieve_analysis_report',
        '--accession',
        'ERZ009929',
        '--fields',
        'analysis_accession'])
    assert result.exit_code == 0
    assert result.output.find('PRJEB1970') == -1
    # 3rd test
    result = runner.invoke(cli, [
        'retrieve_analysis_report',
        '--accession',
        'ERZ009929',
        '--fields',
        'analysis_accession,sample_accession,scientific_name'])
    assert result.exit_code == 0
    assert result.output.find('PRJEB1970') == -1
    assert result.output.find('SAMEA2072680') != -1
