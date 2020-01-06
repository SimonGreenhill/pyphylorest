# coding=utf-8
import pytest

import phlorest
from phlorest import __main__

from clldutils.clilib import ParserError


def test_listdatasets(repos, mocker, capsys):
    phlorest.commands.listdatasets(mocker.Mock(repos=repos, args=[]))
    captured = capsys.readouterr()
    assert 'Dataset' in captured.out
    assert 'testdata' in captured.out
    assert '🌿' in captured.out


def test_check(repos, mocker, capsys):
    phlorest.commands.check(mocker.Mock(repos=repos, args=[]))
    captured = capsys.readouterr()
    assert 'Dataset' in captured.out
    assert 'testdata' in captured.out
    assert '✅' in captured.out


def test_new(repos, mocker):
    with pytest.raises(ParserError) as e:
        phlorest.commands.new(mocker.Mock(repos=repos.path, args=[]))
    
    mocker.patch("phlorest.create.create")
    phlorest.commands.new(mocker.Mock(repos=repos, args=['xx']))
    phlorest.create.create.assert_called_once_with(repos.path, 'xx')


def test_dplace(repos, mocker, capsys):
    with pytest.raises(ParserError) as e:
        phlorest.commands.dplace(mocker.Mock(repos=repos, args=[]))

    phlorest.commands.dplace(mocker.Mock(repos=repos, args=['testdata']))
    captured = capsys.readouterr()
    assert 'greenhill2015,Huon Peninsula (Greenhill 2015),' in captured.out


def test_readme(repos, mocker, capsys):
    with pytest.raises(ParserError) as e:
        phlorest.commands.readme(mocker.Mock(repos=repos, args=[]))

    phlorest.commands.readme(mocker.Mock(repos=repos, args=['testdata']))
    captured = capsys.readouterr()
    assert captured.out.startswith('# Huon Peninsula (Greenhill 2015):')
    assert '[summary.trees](summary.trees)' in captured.out
    assert '14 taxa' in captured.out
    assert '2 characters'


def test_itemise(repos, mocker, capsys):
    with pytest.raises(ParserError) as e:
        phlorest.commands.itemise(mocker.Mock(repos=repos, args=[]))

    phlorest.commands.itemise(mocker.Mock(repos=repos, args=['scaling']))
    captured = capsys.readouterr()
    assert 'change' in captured.out

