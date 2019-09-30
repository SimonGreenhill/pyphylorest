# coding=utf-8
from phlorest import Phlorest

def test_repos(repos):
    assert "Phlorest Repository in tests" in str(repos)
    assert 'testdata' in repos.datasets
    assert isinstance(repos.datasets['testdata'], Phlorest)
