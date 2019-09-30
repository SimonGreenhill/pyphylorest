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

