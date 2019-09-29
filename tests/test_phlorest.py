from phlorest import Phlorest, read_details, read_taxa
from phlorest.create import create

EXPECTED_DETAILS = {
    'id': 'greenhill2015',
    'name': 'Huon Peninsula (Greenhill 2015)',
    'author': 'Greenhill',
    'year': '2015',
    'scaling': 'change',
    'reference': 'Greenhill, S. J. (2015). TransNewGuinea.org: An Online ...',
    'url': 'https://dx.doi.org/10.1371/journal.pone.0141563',
    'cldf': 'http://...',
}

EXPECTED_TAXA = {
    'borong': {'taxon': 'borong', 'isocode': 'ksr', 'glottocode': 'Kosorong', 'xd_ids': 'boro1279', 'soc_ids': ''},
    'burum': {'taxon': 'burum', 'isocode': 'bmu', 'glottocode': 'Burum', 'xd_ids': 'buru1306', 'soc_ids': ''},
    'dedua': {'taxon': 'dedua', 'isocode': 'ded', 'glottocode': 'Dedua', 'xd_ids': 'dedu1240', 'soc_ids': ''},
    'kate': {'taxon': 'kate', 'isocode': 'kmg', 'glottocode': 'Kâte', 'xd_ids': 'kate1253', 'soc_ids': ''},
    'komba': {'taxon': 'komba', 'isocode': 'kpf', 'glottocode': 'Komba', 'xd_ids': 'komb1273', 'soc_ids': ''},
    'kube': {'taxon': 'kube', 'isocode': 'kgf', 'glottocode': 'Hube', 'xd_ids': 'kube1244', 'soc_ids': ''},
    'mape': {'taxon': 'mape', 'isocode': 'mlh', 'glottocode': 'Mape', 'xd_ids': 'mape1249', 'soc_ids': ''},
    'mesem': {'taxon': 'mesem', 'isocode': 'mci', 'glottocode': 'Mese', 'xd_ids': 'mese1244', 'soc_ids': ''},
    'mindik': {'taxon': 'mindik', 'isocode': 'bmu', 'glottocode': 'Mindik', 'xd_ids': 'buru1306', 'soc_ids': ''},
    'nabak': {'taxon': 'nabak', 'isocode': 'naf', 'glottocode': 'Nabak', 'xd_ids': 'naba1256', 'soc_ids': ''},
    'ono': {'taxon': 'ono', 'isocode': 'ons', 'glottocode': 'Ono', 'xd_ids': 'onoo1246', 'soc_ids': ''},
    'selepet': {'taxon': 'selepet', 'isocode': 'spl', 'glottocode': 'Selepet', 'xd_ids': 'sele1250', 'soc_ids': ''},
    'timbe': {'taxon': 'timbe', 'isocode': 'tim', 'glottocode': 'Timbe', 'xd_ids': 'timb1251', 'soc_ids': ''},
    'tobo': {'taxon': 'tobo', 'isocode': 'kgf', 'glottocode': 'Tobo', 'xd_ids': 'tobo1251', 'soc_ids': ''},
}

def test_repr(g2015):
    assert repr(g2015) == '<Phlorest Dataset greenhill2015>'


def test_read_details(g2015):
    for e in EXPECTED_DETAILS:
        assert e in g2015.details
        assert g2015.details[e] == EXPECTED_DETAILS[e]


def test_read_taxa(g2015):
    for e in EXPECTED_TAXA:
        assert e in g2015.taxa
        assert g2015.taxa[e] == EXPECTED_TAXA[e]
    

def test_phlorest_get(g2015):
    # missing files should get None
    assert g2015._get('detali.stxt') is None
    # single files should be paths
    assert g2015._get('details.txt') == g2015.dirname / 'details.txt'
    # ...and dirs should be a list
    assert g2015._get('paper') == [g2015.dirname / 'paper' / 'Greenhill2015.pdf']
    

def test_phlorest(g2015):
    assert len(g2015.details) == len(EXPECTED_DETAILS)  # full test in test_read_details
    assert len(g2015.taxa) == len(EXPECTED_TAXA)  # full test in test_read_taxa
    
    # files
    assert g2015.makefile.startswith('all: summary.trees posterior.trees')
    assert g2015.source.startswith('@article{Greenhill2015,')
    assert g2015.notes.startswith('# Notes')
    
    # dirs...
    assert len(g2015.original) == 4
    assert g2015.paper == [g2015.dirname / 'paper' / 'Greenhill2015.pdf']
    assert g2015.nexus == [g2015.dirname / 'nexus' / 'mcelhanon-1967.nex']
    assert g2015.data == [g2015.dirname / 'data' / 'mcelhanon-1967.dat']
    
    # trees
    assert g2015.treefiles['summary'] == g2015.dirname / 'summary.trees'
    assert g2015.treefiles['posterior'] == g2015.dirname / 'posterior.trees'
    
    # defined in data:
    assert g2015.cldf == 'http://...'
    

def test_check(g2015, tmp_path):
    assert g2015.check() == True
    create(tmp_path, 'test_check')
    expected = [
        'makefile', 'source', 'original', 'paper', 'nexus', 'data', 'cldf',
        'summary.trees', 'posterior.trees', 'details.txt', 'taxa.csv'
    ]
    errors = Phlorest(tmp_path / 'test_check').check()
    for e in expected:
        assert e in errors, 'should have failed on %s' % e
