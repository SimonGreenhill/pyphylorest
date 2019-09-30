# coding=utf-8
from pathlib import Path
from .phlorest import Phlorest


class Repos:
    def __init__(self, path):
        self.path = Path(path)
        self._datasets = None

    def __repr__(self):
        return "<Phlorest Repository in %s>" % self.path
    
    @property
    def datasets(self):
        if not self._datasets:
            self._datasets = {k: v for k, v in self.load(self.path)}
        return self._datasets

    def load(self, path):
        for dirname in path.iterdir():
            if dirname.is_dir() and (dirname / 'details.txt').exists():
                yield (dirname.name, Phlorest(dirname))
