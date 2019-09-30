# coding=utf-8
import pytest

from phlorest.create import create, dirs_to_create, files_to_create


def test_create_file(tmp_path):
    create(tmp_path, 'testcreate')
    
    for d in dirs_to_create:
        assert (tmp_path / 'testcreate' / d).exists()
    
    for f in files_to_create:
        path = tmp_path / 'testcreate' / f
        assert path.exists()
        assert path.read_text(encoding="utf8") == files_to_create[f]

    # test IOError on path exists
    (tmp_path / "testcreate2").mkdir()
    with pytest.raises(IOError) as e:
        create(tmp_path, 'testcreate2')
    