# coding=utf-8
import pytest
from phlorest import Phlorest, Repos

@pytest.fixture(scope="module")
def repos():
    return Repos('tests')


@pytest.fixture(scope="module")
def g2015():
    return Phlorest('tests/testdata')
